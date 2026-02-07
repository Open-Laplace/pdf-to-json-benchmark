#!/usr/bin/env python3
"""
Compare all extraction methods on the same PDF

Tests PDFPlumber, Tabula, and Camelot side-by-side
"""
import sys
from pathlib import Path
import json
from typing import List, Dict

from methods.traditional.pdfplumber_extractor import PDFPlumberExtractor
from methods.traditional.tabula_extractor import TabulaExtractor
from methods.traditional.camelot_extractor import CamelotExtractor, CAMELOT_AVAILABLE

def compare_extractors(pdf_path: str):
    """Compare all available extraction methods"""
    
    print("="*70)
    print("PDF Table Extraction Comparison")
    print("="*70)
    print(f"\nFile: {pdf_path}\n")
    
    results = {}
    
    # 1. PDFPlumber
    print("\n" + "="*70)
    print("Method 1: PDFPlumber")
    print("="*70)
    try:
        extractor = PDFPlumberExtractor(verbose=True)
        tables = extractor.extract_tables(pdf_path)
        results['pdfplumber'] = {
            'tables': tables,
            'count': len(tables),
            'time': extractor.extraction_time,
            'success': True
        }
    except Exception as e:
        print(f"✗ Error: {e}")
        results['pdfplumber'] = {'success': False, 'error': str(e)}
    
    # 2. Tabula
    print("\n" + "="*70)
    print("Method 2: Tabula")
    print("="*70)
    try:
        extractor = TabulaExtractor(verbose=True)
        tables = extractor.extract_tables(pdf_path)
        results['tabula'] = {
            'tables': tables,
            'count': len(tables),
            'time': extractor.extraction_time,
            'success': True
        }
    except Exception as e:
        print(f"✗ Error: {e}")
        results['tabula'] = {'success': False, 'error': str(e)}
    
    # 3. Camelot
    print("\n" + "="*70)
    print("Method 3: Camelot")
    print("="*70)
    if CAMELOT_AVAILABLE:
        try:
            extractor = CamelotExtractor(verbose=True)
            tables = extractor.extract_auto(pdf_path)
            results['camelot'] = {
                'tables': tables,
                'count': len(tables),
                'time': extractor.extraction_time,
                'success': True
            }
        except Exception as e:
            print(f"✗ Error: {e}")
            results['camelot'] = {'success': False, 'error': str(e)}
    else:
        print("⚠ Camelot not installed")
        results['camelot'] = {'success': False, 'error': 'Not installed'}
    
    # Summary
    print("\n" + "="*70)
    print("COMPARISON SUMMARY")
    print("="*70)
    
    print(f"\n{'Method':<15} {'Tables':<10} {'Time (s)':<12} {'Status'}")
    print("-" * 70)
    
    for method, data in results.items():
        if data['success']:
            count = data['count']
            time_str = f"{data['time']:.3f}"
            status = "✓ Success"
        else:
            count = "N/A"
            time_str = "N/A"
            status = f"✗ {data.get('error', 'Failed')[:30]}"
        
        print(f"{method:<15} {str(count):<10} {time_str:<12} {status}")
    
    # Detailed comparison
    print("\n" + "="*70)
    print("DETAILED COMPARISON")
    print("="*70)
    
    for method, data in results.items():
        if not data['success']:
            continue
        
        print(f"\n{method.upper()}:")
        for i, table in enumerate(data['tables']):
            dims = f"{table['num_rows']}x{table['num_cols']}"
            page = table.get('page', 'N/A')
            
            extra = ""
            if 'accuracy' in table:
                extra = f", accuracy={table['accuracy']:.2f}"
            elif 'method' in table:
                extra = f", method={table['method']}"
            
            print(f"  Table {i+1}: {dims} (page {page}{extra})")
    
    # Save comparison
    output_file = Path(pdf_path).stem + "_comparison.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Comparison saved to {output_file}")
    
    # Best recommendation
    print("\n" + "="*70)
    print("RECOMMENDATION")
    print("="*70)
    
    successful = {k: v for k, v in results.items() if v['success']}
    if successful:
        # Sort by number of tables found (more is usually better)
        best = max(successful.items(), key=lambda x: (x[1]['count'], -x[1]['time']))
        print(f"\nBest method: {best[0].upper()}")
        print(f"  Tables found: {best[1]['count']}")
        print(f"  Extraction time: {best[1]['time']:.3f}s")
    else:
        print("\n⚠ No method succeeded")
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_methods.py <pdf_file>")
        print("\nCompares PDFPlumber, Tabula, and Camelot on the same PDF")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    compare_extractors(pdf_path)

if __name__ == "__main__":
    main()
