#!/usr/bin/env python3
"""
Quick demo: Test PDF table extraction without needing the full dataset

This script:
1. Creates a simple test PDF with a table (or uses a provided PDF)
2. Extracts tables using pdfplumber
3. Shows the results

Usage:
    python demo_quick_test.py                    # Creates demo PDF
    python demo_quick_test.py your_file.pdf      # Tests your PDF
"""
import sys
from pathlib import Path
import json

# Import our extractor
from methods.traditional.pdfplumber_extractor import PDFPlumberExtractor

def create_demo_pdf():
    """Create a simple demo PDF with a table"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        
        output_path = "demo_table.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []
        
        # Sample financial data
        data = [
            ['Quarter', 'Revenue', 'Expenses', 'Profit'],
            ['Q1 2023', '$1,200,000', '$800,000', '$400,000'],
            ['Q2 2023', '$1,350,000', '$850,000', '$500,000'],
            ['Q3 2023', '$1,500,000', '$900,000', '$600,000'],
            ['Q4 2023', '$1,650,000', '$950,000', '$700,000'],
            ['Total', '$5,700,000', '$3,500,000', '$2,200,000'],
        ]
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        print(f"✓ Created demo PDF: {output_path}")
        return output_path
        
    except ImportError:
        print("⚠ reportlab not installed, can't create demo PDF")
        print("  Install with: uv pip install reportlab")
        print("  Or provide your own PDF file")
        return None

def test_extraction(pdf_path):
    """Test table extraction on a PDF file"""
    print(f"\n{'='*60}")
    print(f"Testing PDF Table Extraction")
    print(f"{'='*60}")
    print(f"\nFile: {pdf_path}")
    
    # Extract tables
    extractor = PDFPlumberExtractor(verbose=True)
    tables = extractor.extract_tables(pdf_path)
    
    if not tables:
        print("\n⚠ No tables found in PDF")
        return
    
    # Show results
    print(f"\n{'='*60}")
    print(f"Results")
    print(f"{'='*60}")
    
    for i, table in enumerate(tables):
        print(f"\nTable {i+1} (Page {table['page']}):")
        print(f"  Dimensions: {table['num_rows']} rows × {table['num_cols']} cols")
        print(f"\n  Data:")
        
        # Pretty print table
        for row_idx, row in enumerate(table['data']):
            if row_idx == 0:
                print(f"  {' | '.join(str(cell or '') for cell in row)}")
                print(f"  {'-' * 60}")
            else:
                print(f"  {' | '.join(str(cell or '') for cell in row)}")
    
    # Save to JSON
    output_path = Path(pdf_path).stem + "_extracted.json"
    json_output = extractor.tables_to_json(tables, include_metadata=True)
    
    with open(output_path, 'w') as f:
        f.write(json_output)
    
    print(f"\n✓ Saved results to {output_path}")
    
    return tables

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # User provided PDF
        pdf_path = sys.argv[1]
        if not Path(pdf_path).exists():
            print(f"✗ File not found: {pdf_path}")
            sys.exit(1)
    else:
        # Create demo PDF
        print("No PDF provided, creating demo...")
        pdf_path = create_demo_pdf()
        if not pdf_path:
            print("\nUsage: python demo_quick_test.py <pdf_file>")
            sys.exit(1)
    
    # Test extraction
    test_extraction(pdf_path)
    
    print(f"\n{'='*60}")
    print("Next steps:")
    print(f"{'='*60}")
    print("\n1. Test with your own financial PDFs")
    print("2. Compare with other methods (Tabula, Camelot)")
    print("3. Download full FinTabNet dataset for comprehensive testing")
    print("\nFor more options: python run_benchmark.py --help")

if __name__ == "__main__":
    main()
