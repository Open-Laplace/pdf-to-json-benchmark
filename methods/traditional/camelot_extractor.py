#!/usr/bin/env python3
"""
PDF Table Extraction using Camelot
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import time

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    print("Warning: Camelot not available. Install with: uv pip install 'camelot-py[base]'")

class CamelotExtractor:
    """Extract tables from PDF using Camelot"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.extraction_time = 0
        
        if not CAMELOT_AVAILABLE:
            raise ImportError("Camelot is not installed")
    
    def extract_tables(self, pdf_path: str, 
                      flavor: str = 'lattice',
                      pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract all tables from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            flavor: 'lattice' for bordered tables, 'stream' for borderless
            pages: Pages to process ('all' or '1,2,3' or '1-3')
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        try:
            if self.verbose:
                print(f"Processing {Path(pdf_path).name} (Camelot {flavor} method)")
            
            # Extract tables
            table_list = camelot.read_pdf(
                pdf_path,
                pages=pages,
                flavor=flavor
            )
            
            if self.verbose:
                print(f"  Found {len(table_list)} tables")
            
            # Convert to our format
            for idx, table in enumerate(table_list):
                # Get table data as list of lists
                table_data = table.df.values.tolist()
                
                # Add headers (check if first column name is unnamed)
                col_names = table.df.columns.tolist()
                first_col = str(col_names[0]) if col_names else ''
                if not first_col.startswith('Unnamed'):
                    table_data = [col_names] + table_data
                
                table_info = {
                    'page': table.page,
                    'table_index': idx,
                    'data': table_data,
                    'num_rows': len(table_data),
                    'num_cols': len(table_data[0]) if table_data else 0,
                    'accuracy': table.accuracy,
                    'whitespace': table.whitespace,
                    'flavor': flavor
                }
                tables.append(table_info)
                
                if self.verbose:
                    print(f"  Table {idx} (Page {table.page}): "
                          f"{table_info['num_rows']}x{table_info['num_cols']}, "
                          f"accuracy={table.accuracy:.2f}")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return []
        
        self.extraction_time = time.time() - start_time
        
        if self.verbose:
            print(f"Extracted {len(tables)} tables in {self.extraction_time:.2f}s\n")
        
        return tables
    
    def extract_auto(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Auto-detect best method (tries both lattice and stream)
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process
            
        Returns:
            List of extracted tables
        """
        # Try lattice first
        tables_lattice = self.extract_tables(pdf_path, flavor='lattice', pages=pages)
        
        # Try stream if lattice found nothing
        if not tables_lattice:
            if self.verbose:
                print("Lattice found nothing, trying stream method...")
            tables_stream = self.extract_tables(pdf_path, flavor='stream', pages=pages)
            return tables_stream
        
        return tables_lattice
    
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
                'method': 'camelot',
                'tables': tables
            }
        else:
            output = {'tables': [t['data'] for t in tables]}
        
        return json.dumps(output, indent=2, default=str)
    
    def extract_to_file(self, pdf_path: str, output_path: str, 
                       flavor: str = 'auto'):
        """
        Extract tables and save to JSON file
        
        Args:
            pdf_path: Input PDF path
            output_path: Output JSON path
            flavor: 'lattice', 'stream', or 'auto'
        """
        if flavor == 'auto':
            tables = self.extract_auto(pdf_path)
        else:
            tables = self.extract_tables(pdf_path, flavor=flavor)
        
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
    
    if not CAMELOT_AVAILABLE:
        print("Error: Camelot not installed")
        print("Install with: uv pip install 'camelot-py[base]' opencv-python-headless")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python camelot_extractor.py <pdf_file> [output.json] [flavor]")
        print("  flavor: lattice, stream, or auto (default: auto)")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_camelot.json"
    flavor = sys.argv[3] if len(sys.argv) > 3 else "auto"
    
    extractor = CamelotExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file, flavor=flavor)

if __name__ == "__main__":
    main()
