#!/usr/bin/env python3
"""
Compare ALL extraction methods (traditional + deep learning + LLM + hybrid)

Tests up to 10 methods on the same PDF
"""
import sys
import os
from pathlib import Path
import json
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Traditional methods
from methods.traditional.pdfplumber_extractor import PDFPlumberExtractor
from methods.traditional.camelot_extractor import CamelotExtractor, CAMELOT_AVAILABLE
from methods.traditional.tabula_extractor import TabulaExtractor

# Deep learning methods
try:
    from methods.deep_learning.table_transformer_extractor import TableTransformerExtractor
    TT_AVAILABLE = True
except ImportError:
    TT_AVAILABLE = False

try:
    from methods.deep_learning.docling_extractor import DoclingExtractor
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False

# LLM methods
try:
    from methods.llm.gpt4_vision_extractor import GPT4VisionExtractor
    GPT4_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
except ImportError:
    GPT4_AVAILABLE = False

try:
    from methods.llm.claude_vision_extractor import ClaudeVisionExtractor
    CLAUDE_AVAILABLE = bool(os.getenv("ANTHROPIC_API_KEY"))
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    from methods.llm.gemini_vision_extractor import GeminiVisionExtractor
    GEMINI_AVAILABLE = bool(os.getenv("GOOGLE_API_KEY"))
except ImportError:
    GEMINI_AVAILABLE = False

# Hybrid methods
try:
    from methods.hybrid.layout_gpt4_extractor import LayoutGPT4Extractor
    HYBRID_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
except ImportError:
    HYBRID_AVAILABLE = False

def run_method(name: str, extractor, pdf_path: str, verbose: bool = False) -> Dict:
    """Run a single extraction method"""
    print(f"\n{'='*70}")
    print(f"Method: {name}")
    print(f"{'='*70}")
    
    try:
        tables = extractor.extract_tables(pdf_path)
        return {
            'tables': tables,
            'count': len(tables),
            'time': extractor.extraction_time,
            'cost': getattr(extractor, 'total_cost', 0),
            'success': True
        }
    except Exception as e:
        print(f"✗ Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return {'success': False, 'error': str(e)}

def compare_all_methods(pdf_path: str, methods: List[str] = None):
    """Compare all available extraction methods"""
    
    print("="*70)
    print("PDF Table Extraction - COMPLETE COMPARISON")
    print("="*70)
    print(f"\nFile: {pdf_path}\n")
    
    results = {}
    
    # Define all methods
    all_methods = {
        'pdfplumber': (True, lambda: PDFPlumberExtractor(verbose=True)),
        'camelot': (CAMELOT_AVAILABLE, lambda: CamelotExtractor(verbose=True)),
        'tabula': (True, lambda: TabulaExtractor(verbose=True)),
        'table_transformer': (TT_AVAILABLE, lambda: TableTransformerExtractor(verbose=True)),
        'docling': (DOCLING_AVAILABLE, lambda: DoclingExtractor(verbose=True)),
        'gpt4_vision': (GPT4_AVAILABLE, lambda: GPT4VisionExtractor(verbose=True)),
        'claude_vision': (CLAUDE_AVAILABLE, lambda: ClaudeVisionExtractor(verbose=True)),
        'gemini_vision': (GEMINI_AVAILABLE, lambda: GeminiVisionExtractor(verbose=True)),
        'hybrid_layout_gpt4': (HYBRID_AVAILABLE, lambda: LayoutGPT4Extractor(verbose=True))
    }
    
    # Filter methods if specified
    if methods:
        all_methods = {k: v for k, v in all_methods.items() if k in methods}
    
    # Run each method
    for method_name, (available, extractor_fn) in all_methods.items():
        if not available:
            print(f"\n{'='*70}")
            print(f"Method: {method_name}")
            print(f"{'='*70}")
            if method_name in ['gpt4_vision', 'claude_vision', 'gemini_vision', 'hybrid_layout_gpt4']:
                print("⚠ Skipped - API key not configured")
                print(f"  Set {method_name.upper()}_API_KEY in .env file")
            else:
                print("⚠ Skipped - dependencies not installed")
            results[method_name] = {'success': False, 'error': 'Not available'}
            continue
        
        try:
            extractor = extractor_fn()
            results[method_name] = run_method(method_name, extractor, pdf_path)
        except Exception as e:
            print(f"\n{'='*70}")
            print(f"Method: {method_name}")
            print(f"{'='*70}")
            print(f"✗ Error initializing: {e}")
            results[method_name] = {'success': False, 'error': str(e)}
    
    # Summary
    print("\n" + "="*70)
    print("COMPARISON SUMMARY")
    print("="*70)
    
    print(f"\n{'Method':<20} {'Tables':<10} {'Time (s)':<12} {'Cost ($)':<12} {'Status'}")
    print("-" * 70)
    
    for method, data in results.items():
        if data['success']:
            count = data['count']
            time_str = f"{data['time']:.3f}"
            cost_str = f"{data['cost']:.4f}" if data['cost'] > 0 else "Free"
            status = "✓ Success"
        else:
            count = "N/A"
            time_str = "N/A"
            cost_str = "N/A"
            status = f"✗ {data.get('error', 'Failed')[:20]}"
        
        print(f"{method:<20} {str(count):<10} {time_str:<12} {cost_str:<12} {status}")
    
    # Cost analysis
    total_cost = sum(r['cost'] for r in results.values() if r['success'] and 'cost' in r)
    if total_cost > 0:
        print(f"\n{'='*70}")
        print(f"Total API Cost: ${total_cost:.4f}")
        print(f"{'='*70}")
    
    # Save results
    output_file = Path(pdf_path).stem + "_all_methods_comparison.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Full comparison saved to {output_file}")
    
    # Recommendations
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    
    successful = {k: v for k, v in results.items() if v['success']}
    
    if successful:
        # Fastest free method
        free_methods = {k: v for k, v in successful.items() if v.get('cost', 0) == 0}
        if free_methods:
            fastest_free = min(free_methods.items(), key=lambda x: x[1]['time'])
            print(f"\nFastest free method: {fastest_free[0].upper()}")
            print(f"  Time: {fastest_free[1]['time']:.3f}s")
            print(f"  Tables: {fastest_free[1]['count']}")
        
        # Most accurate (highest table count as proxy)
        most_tables = max(successful.items(), key=lambda x: x[1]['count'])
        print(f"\nMost tables detected: {most_tables[0].upper()}")
        print(f"  Tables: {most_tables[1]['count']}")
        print(f"  Time: {most_tables[1]['time']:.3f}s")
        
        # Best value (paid methods)
        paid_methods = {k: v for k, v in successful.items() if v.get('cost', 0) > 0}
        if paid_methods:
            # Sort by cost/table ratio
            best_value = min(paid_methods.items(), 
                           key=lambda x: x[1]['cost'] / max(x[1]['count'], 1))
            print(f"\nBest value (paid): {best_value[0].upper()}")
            print(f"  Cost: ${best_value[1]['cost']:.4f}")
            print(f"  Tables: {best_value[1]['count']}")
            print(f"  Cost/table: ${best_value[1]['cost']/max(best_value[1]['count'], 1):.4f}")
    else:
        print("\n⚠ No methods succeeded")
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_all_methods.py <pdf_file> [methods...]")
        print("\nAvailable methods:")
        print("  Traditional: pdfplumber, camelot, tabula")
        print("  Deep Learning: table_transformer, docling")
        print("  LLM Vision: gpt4_vision, claude_vision, gemini_vision")
        print("  Hybrid: hybrid_layout_gpt4")
        print("\nExamples:")
        print("  python compare_all_methods.py file.pdf")
        print("  python compare_all_methods.py file.pdf pdfplumber gpt4_vision")
        print("\nNote: LLM methods require API keys in .env file")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    # Get specific methods if provided
    methods = sys.argv[2:] if len(sys.argv) > 2 else None
    
    compare_all_methods(pdf_path, methods)

if __name__ == "__main__":
    main()
