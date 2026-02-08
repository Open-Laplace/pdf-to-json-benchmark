#!/usr/bin/env python3
"""
PDF Table Extraction using Docling (IBM Research)
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import time

try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False

class DoclingExtractor:
    """Extract tables from PDF using Docling"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.extraction_time = 0
        
        if not DOCLING_AVAILABLE:
            raise ImportError("Docling not installed. Run: uv pip install docling")
        
        if self.verbose:
            print("Initializing Docling converter...")
        
        # Initialize converter
        self.converter = DocumentConverter()
        
        if self.verbose:
            print("Docling ready!")
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using Docling
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process ('all' or page numbers)
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        if self.verbose:
            print(f"Processing {Path(pdf_path).name} with Docling")
        
        try:
            # Convert document
            if self.verbose:
                print(f"  Converting document...")
            
            result = self.converter.convert(pdf_path)
            
            # Extract tables from document
            if self.verbose:
                print(f"  Extracting tables...")
            
            for table_idx, table in enumerate(result.document.tables):
                # Convert table to 2D array
                table_data = []
                
                # Get table dimensions
                if hasattr(table, 'data') and table.data:
                    # Table has structured data
                    for row in table.data:
                        row_data = [str(cell) for cell in row]
                        table_data.append(row_data)
                else:
                    # Try to extract from text representation
                    if hasattr(table, 'text'):
                        # Parse text representation (simplified)
                        lines = table.text.strip().split('\n')
                        for line in lines:
                            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                            if cells:
                                table_data.append(cells)
                
                if table_data:
                    table_info = {
                        'page': getattr(table, 'page_no', -1),
                        'table_index': table_idx,
                        'data': table_data,
                        'num_rows': len(table_data),
                        'num_cols': len(table_data[0]) if table_data else 0
                    }
                    tables.append(table_info)
                    
                    if self.verbose:
                        print(f"  Table {table_idx}: {table_info['num_rows']}x{table_info['num_cols']}")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return []
        
        self.extraction_time = time.time() - start_time
        
        if self.verbose:
            print(f"Extracted {len(tables)} tables in {self.extraction_time:.2f}s\n")
        
        return tables
    
    def tables_to_json(self, tables: List[Dict[str, Any]], 
                       include_metadata: bool = True) -> str:
        """Convert extracted tables to JSON format"""
        if include_metadata:
            output = {
                'num_tables': len(tables),
                'extraction_time': self.extraction_time,
                'method': 'docling',
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
        print("Usage: python docling_extractor.py <pdf_file> [output.json]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_docling.json"
    
    extractor = DoclingExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
