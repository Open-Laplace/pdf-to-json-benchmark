#!/usr/bin/env python3
"""
Quick test to verify all extraction methods can be imported
"""
import sys

def test_imports():
    """Test importing all extraction methods"""
    print("Testing extraction method imports...\n")
    
    results = {}
    
    # Traditional methods
    print("Traditional Methods:")
    try:
        from methods.traditional.pdfplumber_extractor import PDFPlumberExtractor
        print("  ✓ PDFPlumber")
        results['pdfplumber'] = True
    except Exception as e:
        print(f"  ✗ PDFPlumber: {e}")
        results['pdfplumber'] = False
    
    try:
        from methods.traditional.camelot_extractor import CamelotExtractor
        print("  ✓ Camelot")
        results['camelot'] = True
    except Exception as e:
        print(f"  ✗ Camelot: {e}")
        results['camelot'] = False
    
    try:
        from methods.traditional.tabula_extractor import TabulaExtractor
        print("  ✓ Tabula")
        results['tabula'] = True
    except Exception as e:
        print(f"  ✗ Tabula: {e}")
        results['tabula'] = False
    
    # Deep learning methods
    print("\nDeep Learning Methods:")
    try:
        from methods.deep_learning.table_transformer_extractor import TableTransformerExtractor
        print("  ✓ Table Transformer")
        results['table_transformer'] = True
    except Exception as e:
        print(f"  ✗ Table Transformer: {e}")
        results['table_transformer'] = False
    
    try:
        from methods.deep_learning.docling_extractor import DoclingExtractor
        print("  ✓ Docling")
        results['docling'] = True
    except Exception as e:
        print(f"  ✗ Docling: {e}")
        results['docling'] = False
    
    # LLM methods
    print("\nLLM Vision Methods:")
    try:
        from methods.llm.gpt4_vision_extractor import GPT4VisionExtractor
        print("  ✓ GPT-4 Vision")
        results['gpt4_vision'] = True
    except Exception as e:
        print(f"  ✗ GPT-4 Vision: {e}")
        results['gpt4_vision'] = False
    
    try:
        from methods.llm.claude_vision_extractor import ClaudeVisionExtractor
        print("  ✓ Claude Vision")
        results['claude_vision'] = True
    except Exception as e:
        print(f"  ✗ Claude Vision: {e}")
        results['claude_vision'] = False
    
    try:
        from methods.llm.gemini_vision_extractor import GeminiVisionExtractor
        print("  ✓ Gemini Vision")
        results['gemini_vision'] = True
    except Exception as e:
        print(f"  ✗ Gemini Vision: {e}")
        results['gemini_vision'] = False
    
    # Hybrid methods
    print("\nHybrid Methods:")
    try:
        from methods.hybrid.layout_gpt4_extractor import LayoutGPT4Extractor
        print("  ✓ Layout + GPT-4")
        results['hybrid'] = True
    except Exception as e:
        print(f"  ✗ Layout + GPT-4: {e}")
        results['hybrid'] = False
    
    # Summary
    print("\n" + "="*50)
    total = len(results)
    passed = sum(results.values())
    print(f"Results: {passed}/{total} methods can be imported")
    print("="*50)
    
    if passed == total:
        print("\n✓ All methods imported successfully!")
        return 0
    else:
        print(f"\n⚠ {total - passed} methods failed to import")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
