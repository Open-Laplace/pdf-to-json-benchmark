#!/usr/bin/env python3
"""
PDF Table Extraction using pdfplumber
"""
import pdfplumber
import json
from pathlib import Path
from typing import List, Dict, Any
import time

class PDFPlumberExtractor:
    """Extract tables from PDF using pdfplumber"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.extraction_time = 0
    
    def extract_tables(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract all tables from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if self.verbose:
                    print(f"Processing {Path(pdf_path).name} ({len(pdf.pages)} pages)")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract tables from page
                    page_tables = page.extract_tables()
                    
                    for table_idx, table_data in enumerate(page_tables):
                        if table_data:  # Skip empty tables
                            table_info = {
                                'page': page_num,
                                'table_index': table_idx,
                                'data': table_data,
                                'num_rows': len(table_data),
                                'num_cols': len(table_data[0]) if table_data else 0,
                            }
                            tables.append(table_info)
                            
                            if self.verbose:
                                print(f"  Page {page_num}, Table {table_idx}: "
                                      f"{table_info['num_rows']}x{table_info['num_cols']}")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []
        
        self.extraction_time = time.time() - start_time
        
        if self.verbose:
            print(f"Extracted {len(tables)} tables in {self.extraction_time:.2f}s\n")
        
        return tables
    
    def tables_to_json(self, tables: List[Dict[str, Any]], 
                       include_metadata: bool = True) -> str:
        """
        Convert extracted tables to JSON format
        
        Args:
            tables: List of table dictionaries
            include_metadata: Include page/index metadata
            
        Returns:
            JSON string
        """
        if include_metadata:
            output = {
                'num_tables': len(tables),
                'extraction_time': self.extraction_time,
                'tables': tables
            }
        else:
            output = {'tables': [t['data'] for t in tables]}
        
        return json.dumps(output, indent=2)
    
    def extract_to_file(self, pdf_path: str, output_path: str):
        """
        Extract tables and save to JSON file
        
        Args:
            pdf_path: Input PDF path
            output_path: Output JSON path
        """
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
        print("Usage: python pdfplumber_extractor.py <pdf_file> [output.json]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    
    extractor = PDFPlumberExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
