#!/usr/bin/env python3
"""
Main benchmark script to evaluate all methods
"""
import json
import argparse
from pathlib import Path
from typing import List, Dict
import sys

# Add methods to path
sys.path.append(str(Path(__file__).parent))

from methods.traditional.pdfplumber_extractor import PDFPlumberExtractor
from evaluation.metrics import evaluate_extraction, print_results, save_results


def load_ground_truth(dataset_path: str, sample_limit: int = None) -> List[Dict]:
    """
    Load ground truth from FinTabNet.c dataset
    
    Args:
        dataset_path: Path to dataset directory
        sample_limit: Maximum number of samples to load
        
    Returns:
        List of samples with ground truth
    """
    from datasets import load_from_disk
    
    print(f"Loading dataset from {dataset_path}...")
    dataset = load_from_disk(dataset_path)
    
    # Use test split if available
    if 'test' in dataset:
        data = dataset['test']
    elif 'validation' in dataset:
        data = dataset['validation']
    else:
        # Use first split available
        split_name = list(dataset.keys())[0]
        data = dataset[split_name]
    
    print(f"Loaded {len(data)} samples")
    
    if sample_limit:
        data = data.select(range(min(sample_limit, len(data))))
        print(f"Limited to {len(data)} samples")
    
    return data


def run_pdfplumber_benchmark(samples: List[Dict], output_dir: Path) -> Dict:
    """Run pdfplumber benchmark"""
    print("\n" + "="*60)
    print("Running pdfplumber benchmark")
    print("="*60)
    
    extractor = PDFPlumberExtractor(verbose=False)
    
    predicted_tables = []
    ground_truth_tables = []
    
    for i, sample in enumerate(samples):
        print(f"Processing sample {i+1}/{len(samples)}...", end='\r')
        
        # Extract tables
        # Note: This assumes samples have 'pdf_path' and 'ground_truth' fields
        # Adjust based on actual dataset structure
        if 'pdf' in sample or 'pdf_path' in sample:
            pdf_path = sample.get('pdf_path') or sample.get('pdf')
            tables = extractor.extract_tables(pdf_path)
            predicted_tables.extend([t['data'] for t in tables])
        
        # Get ground truth
        if 'tables' in sample or 'ground_truth' in sample:
            gt = sample.get('tables') or sample.get('ground_truth')
            if isinstance(gt, list):
                ground_truth_tables.extend(gt)
    
    print()  # New line after progress
    
    # Evaluate
    results = evaluate_extraction(
        predicted_tables, 
        ground_truth_tables,
        method_name="pdfplumber"
    )
    
    # Save results
    output_file = output_dir / "pdfplumber_results.json"
    save_results(results, str(output_file))
    
    print_results(results)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Run PDF to JSON benchmark")
    parser.add_argument(
        '--dataset', 
        type=str, 
        default='data/fintabnet',
        help='Path to dataset directory'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='Output directory for results'
    )
    parser.add_argument(
        '--samples',
        type=int,
        default=10,
        help='Number of samples to test (default: 10, use -1 for all)'
    )
    parser.add_argument(
        '--methods',
        nargs='+',
        default=['pdfplumber'],
        choices=['pdfplumber', 'tabula', 'camelot'],
        help='Methods to benchmark'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load samples
    sample_limit = None if args.samples == -1 else args.samples
    samples = load_ground_truth(args.dataset, sample_limit=sample_limit)
    
    # Run benchmarks
    all_results = {}
    
    if 'pdfplumber' in args.methods:
        all_results['pdfplumber'] = run_pdfplumber_benchmark(samples, output_dir)
    
    # TODO: Add other methods
    # if 'tabula' in args.methods:
    #     all_results['tabula'] = run_tabula_benchmark(samples, output_dir)
    
    # Save combined results
    combined_file = output_dir / "benchmark_results.json"
    with open(combined_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✓ All results saved to {output_dir}")
    print(f"  Combined results: {combined_file}")


if __name__ == "__main__":
    main()
