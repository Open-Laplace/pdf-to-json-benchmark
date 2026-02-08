#!/usr/bin/env python3
"""
PDF Table Extraction using Gemini 1.5 Flash Vision
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import time
import os

try:
    import google.generativeai as genai
    from pdf2image import convert_from_path
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class GeminiVisionExtractor:
    """Extract tables from PDF using Gemini Vision API"""
    
    def __init__(self, api_key: str = None, verbose: bool = True, 
                 model: str = "gemini-1.5-flash"):
        self.verbose = verbose
        self.extraction_time = 0
        self.model_name = model
        self.total_cost = 0
        
        if not GEMINI_AVAILABLE:
            raise ImportError("Google AI not installed. Run: uv pip install google-generativeai pdf2image")
        
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key required. Set GOOGLE_API_KEY env var")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
    
    def pdf_to_image(self, pdf_path: str, page_num: int = 1) -> Image.Image:
        """Convert PDF page to PIL Image"""
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=200)
        
        if not images:
            raise ValueError(f"Could not convert page {page_num}")
        
        return images[0]
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using Gemini Vision
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process ('all' or page numbers)
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        if self.verbose:
            print(f"Processing {Path(pdf_path).name} with Gemini Vision ({self.model_name})")
        
        try:
            # Process first page
            page_num = 1
            
            if self.verbose:
                print(f"  Converting page {page_num} to image...")
            
            image = self.pdf_to_image(pdf_path, page_num)
            
            # Prepare prompt
            prompt = """Extract all tables from this image in JSON format.

For each table, provide:
1. The table data as a 2D array (rows and columns)
2. Identify headers if present

Return ONLY valid JSON in this format:
{
  "tables": [
    {
      "data": [
        ["Header1", "Header2", "Header3"],
        ["Row1Col1", "Row1Col2", "Row1Col3"],
        ...
      ]
    }
  ]
}

Be precise with numbers and text. Preserve formatting exactly."""

            if self.verbose:
                print(f"  Sending request to {self.model_name}...")
            
            # Call Gemini API
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            content = response.text
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            # Convert to our format
            for idx, table in enumerate(result.get('tables', [])):
                table_data = table.get('data', [])
                
                table_info = {
                    'page': page_num,
                    'table_index': idx,
                    'data': table_data,
                    'num_rows': len(table_data),
                    'num_cols': len(table_data[0]) if table_data else 0,
                    'model': self.model_name
                }
                tables.append(table_info)
                
                if self.verbose:
                    print(f"  Table {idx}: {table_info['num_rows']}x{table_info['num_cols']}")
            
            # Calculate cost (approximate)
            # Gemini 1.5 Flash: Very cheap - ~$0.001 per 1K input tokens
            # Rough estimate based on image size
            cost = 0.0005  # Approximate per image
            self.total_cost += cost
            
            if self.verbose:
                print(f"  Cost: ${cost:.4f} (estimated)")
        
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
                'method': 'gemini_vision',
                'model': self.model_name,
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
        print("Usage: python gemini_vision_extractor.py <pdf_file> [output.json]")
        print("\nRequires GOOGLE_API_KEY environment variable")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_gemini.json"
    
    extractor = GeminiVisionExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
