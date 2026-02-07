#!/usr/bin/env python3
"""
PDF Table Extraction using Tabula
"""
import tabula
import json
from pathlib import Path
from typing import List, Dict, Any
import time

class TabulaExtractor:
    """Extract tables from PDF using Tabula-py"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.extraction_time = 0
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract all tables from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process ('all' or '1,2,3' or '1-3')
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        # Check if Java is available
        import subprocess
        try:
            subprocess.run(['java', '-version'], 
                         capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            if self.verbose:
                print("  ⚠ Java not found - Tabula requires Java to be installed")
                print("    Install: sudo apt install default-jre")
            return []
        
        try:
            # Extract tables using Tabula
            # lattice=True for tables with clear borders
            # stream=True for tables without borders
            
            if self.verbose:
                print(f"Processing {Path(pdf_path).name} (Tabula method)")
            
            # Try lattice method first (for bordered tables)
            dfs_lattice = tabula.read_pdf(
                pdf_path,
                pages=pages,
                lattice=True,
                multiple_tables=True,
                silent=not self.verbose
            )
            
            # Try stream method (for borderless tables)
            dfs_stream = tabula.read_pdf(
                pdf_path,
                pages=pages,
                stream=True,
                multiple_tables=True,
                silent=not self.verbose
            )
            
            # Combine results (prefer lattice if both found tables)
            all_dfs = dfs_lattice if len(dfs_lattice) >= len(dfs_stream) else dfs_stream
            method_used = 'lattice' if len(dfs_lattice) >= len(dfs_stream) else 'stream'
            
            if self.verbose:
                print(f"  Method used: {method_used}")
                print(f"  Found {len(all_dfs)} tables")
            
            # Convert DataFrames to our format
            for idx, df in enumerate(all_dfs):
                if df.empty:
                    continue
                
                # Convert DataFrame to list of lists
                table_data = [df.columns.tolist()] + df.values.tolist()
                
                table_info = {
                    'page': -1,  # Tabula doesn't provide page info easily
                    'table_index': idx,
                    'data': table_data,
                    'num_rows': len(table_data),
                    'num_cols': len(table_data[0]) if table_data else 0,
                    'method': method_used
                }
                tables.append(table_info)
                
                if self.verbose:
                    print(f"  Table {idx}: {table_info['num_rows']}x{table_info['num_cols']}")
        
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
                'method': 'tabula',
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
        print("Usage: python tabula_extractor.py <pdf_file> [output.json]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_tabula.json"
    
    extractor = TabulaExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
