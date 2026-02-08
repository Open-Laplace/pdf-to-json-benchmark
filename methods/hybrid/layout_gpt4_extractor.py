#!/usr/bin/env python3
"""
Hybrid PDF Table Extraction: Layout Detection + GPT-4 Vision
Uses fast layout detection then GPT-4 for content extraction
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import time
import os

try:
    from openai import OpenAI
    from pdf2image import convert_from_path
    from PIL import Image, ImageDraw
    import base64
    import tempfile
    HYBRID_AVAILABLE = True
except ImportError:
    HYBRID_AVAILABLE = False

class LayoutGPT4Extractor:
    """Hybrid extractor: Fast layout detection + GPT-4 content extraction"""
    
    def __init__(self, api_key: str = None, verbose: bool = True):
        self.verbose = verbose
        self.extraction_time = 0
        self.total_cost = 0
        
        if not HYBRID_AVAILABLE:
            raise ImportError("Dependencies not installed. Run: uv pip install openai pdf2image pillow")
        
        # Get API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def pdf_to_image(self, pdf_path: str, page_num: int = 1) -> Image.Image:
        """Convert PDF page to PIL Image"""
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=200)
        if not images:
            raise ValueError(f"Could not convert page {page_num}")
        return images[0]
    
    def detect_table_regions(self, image: Image.Image) -> List[Dict]:
        """
        Fast table region detection using heuristics
        (In production, would use YOLO/Faster R-CNN)
        For now, returns whole page as one region
        """
        width, height = image.size
        
        # Simplified: treat entire page as potential table region
        # In practice, you'd use a proper detection model here
        return [{
            'bbox': [0, 0, width, height],
            'confidence': 1.0
        }]
    
    def crop_and_encode(self, image: Image.Image, bbox: List[float]) -> str:
        """Crop image to bbox and encode as base64"""
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        cropped = image.crop((x1, y1, x2, y2))
        
        # Save to temp and encode
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            cropped.save(tmp.name, 'PNG')
            with open(tmp.name, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            os.unlink(tmp.name)
        
        return image_data
    
    def extract_table_content(self, image_b64: str) -> Dict:
        """Use GPT-4 to extract table content from cropped region"""
        prompt = """Extract the table from this image in JSON format.

Return ONLY valid JSON:
{
  "data": [
    ["Header1", "Header2", "Header3"],
    ["Row1Col1", "Row1Col2", "Row1Col3"],
    ...
  ]
}

Be precise with numbers and text."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
            temperature=0
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = (input_tokens * 2.5 / 1_000_000) + (output_tokens * 10 / 1_000_000)
        
        return {
            'data': result.get('data', []),
            'tokens': {'input': input_tokens, 'output': output_tokens},
            'cost': cost
        }
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract tables using hybrid approach
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process
            
        Returns:
            List of extracted tables
        """
        start_time = time.time()
        tables = []
        
        if self.verbose:
            print(f"Processing {Path(pdf_path).name} with Hybrid (Layout + GPT-4)")
        
        try:
            # Process first page
            page_num = 1
            
            if self.verbose:
                print(f"  Converting page to image...")
            
            image = self.pdf_to_image(pdf_path, page_num)
            
            # Step 1: Fast layout detection
            if self.verbose:
                print(f"  Detecting table regions...")
            
            regions = self.detect_table_regions(image)
            
            if self.verbose:
                print(f"  Found {len(regions)} regions")
            
            # Step 2: Extract content with GPT-4
            for idx, region in enumerate(regions):
                if self.verbose:
                    print(f"  Extracting content from region {idx} with GPT-4...")
                
                # Crop and encode
                image_b64 = self.crop_and_encode(image, region['bbox'])
                
                # Extract with GPT-4
                result = self.extract_table_content(image_b64)
                
                table_data = result['data']
                
                table_info = {
                    'page': page_num,
                    'table_index': idx,
                    'data': table_data,
                    'num_rows': len(table_data),
                    'num_cols': len(table_data[0]) if table_data else 0,
                    'detection_confidence': region['confidence'],
                    'tokens': result['tokens'],
                    'cost': result['cost']
                }
                tables.append(table_info)
                
                self.total_cost += result['cost']
                
                if self.verbose:
                    print(f"    Extracted: {table_info['num_rows']}x{table_info['num_cols']}")
                    print(f"    Cost: ${result['cost']:.4f}")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return []
        
        self.extraction_time = time.time() - start_time
        
        if self.verbose:
            print(f"Extracted {len(tables)} tables in {self.extraction_time:.2f}s")
            print(f"Total cost: ${self.total_cost:.4f}\n")
        
        return tables
    
    def tables_to_json(self, tables: List[Dict[str, Any]], 
                       include_metadata: bool = True) -> str:
        """Convert extracted tables to JSON format"""
        if include_metadata:
            output = {
                'num_tables': len(tables),
                'extraction_time': self.extraction_time,
                'method': 'hybrid_layout_gpt4',
                'cost': self.total_cost,
                'tables': tables
            }
        else:
            output = {'tables': [t['data'] for t in tables]}
        
        return json.dumps(output, indent=2)
    
    def extract_to_file(self, pdf_path: str, output_path: str):
        """Extract tables and save to JSON file"""
        tables = self.extract_tables(pdf_path)
        json_output = self.tables_to_json(tables)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(json_output)
        
        if self.verbose:
            print(f"Saved to {output_file}")

def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python layout_gpt4_extractor.py <pdf_file> [output.json]")
        print("\nRequires OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_hybrid.json"
    
    extractor = LayoutGPT4Extractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
