#!/usr/bin/env python3
"""
PDF Table Extraction using Claude 3.5 Sonnet Vision
"""
import json
import base64
from pathlib import Path
from typing import List, Dict, Any
import time
import os

try:
    from anthropic import Anthropic
    from pdf2image import convert_from_path
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class ClaudeVisionExtractor:
    """Extract tables from PDF using Claude Vision API"""
    
    def __init__(self, api_key: str = None, verbose: bool = True, 
                 model: str = "claude-3-5-sonnet-20241022"):
        self.verbose = verbose
        self.extraction_time = 0
        self.model = model
        self.total_cost = 0
        
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic not installed. Run: uv pip install anthropic pdf2image")
        
        # Get API key from environment or parameter
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY env var")
        
        self.client = Anthropic(api_key=self.api_key)
    
    def pdf_to_image(self, pdf_path: str, page_num: int = 1) -> bytes:
        """Convert PDF page to image bytes"""
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=200)
        
        if not images:
            raise ValueError(f"Could not convert page {page_num}")
        
        # Save to temp and read bytes
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            images[0].save(tmp.name, 'PNG')
            with open(tmp.name, 'rb') as f:
                image_bytes = f.read()
            os.unlink(tmp.name)
        
        return image_bytes
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using Claude Vision
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process ('all' or page numbers)
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        if self.verbose:
            print(f"Processing {Path(pdf_path).name} with Claude Vision ({self.model})")
        
        try:
            # Process first page
            page_num = 1
            
            if self.verbose:
                print(f"  Converting page {page_num} to image...")
            
            image_bytes = self.pdf_to_image(pdf_path, page_num)
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
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
                print(f"  Sending request to {self.model}...")
            
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_b64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            # Parse response
            content = response.content[0].text
            
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
                    'model': self.model
                }
                tables.append(table_info)
                
                if self.verbose:
                    print(f"  Table {idx}: {table_info['num_rows']}x{table_info['num_cols']}")
            
            # Calculate cost
            # Claude 3.5 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = (input_tokens * 3 / 1_000_000) + (output_tokens * 15 / 1_000_000)
            self.total_cost += cost
            
            if self.verbose:
                print(f"  Tokens: {input_tokens} input, {output_tokens} output")
                print(f"  Cost: ${cost:.4f}")
        
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
                'method': 'claude_vision',
                'model': self.model,
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
        print("Usage: python claude_vision_extractor.py <pdf_file> [output.json]")
        print("\nRequires ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_claude.json"
    
    extractor = ClaudeVisionExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
