#!/usr/bin/env python3
"""
Inspect FinTabNet.c dataset structure to understand format
"""
from datasets import load_dataset
import json

print("Inspecting FinTabNet.c dataset structure...")
print("=" * 60)

# Load streaming dataset
dataset = load_dataset("bsmock/FinTabNet.c", split="train", streaming=True)

# Get first 3 samples
print("\nFetching first 3 samples...\n")
samples = list(dataset.take(3))

for i, sample in enumerate(samples):
    print(f"\n{'='*60}")
    print(f"Sample {i+1}:")
    print(f"{'='*60}")
    
    print(f"\nKey: {sample['__key__']}")
    print(f"URL: {sample['__url__']}")
    
    # Inspect JSON structure
    json_data = sample['json']
    print(f"\nJSON structure:")
    print(f"  Type: {type(json_data)}")
    
    if isinstance(json_data, list):
        print(f"  Number of tables: {len(json_data)}")
        if len(json_data) > 0:
            first_table = json_data[0]
            print(f"\n  First table structure:")
            print(f"    Keys: {list(first_table.keys()) if isinstance(first_table, dict) else 'N/A'}")
            
            if isinstance(first_table, dict) and 'cells' in first_table:
                print(f"    Number of cells: {len(first_table['cells'])}")
                if len(first_table['cells']) > 0:
                    print(f"    First cell: {json.dumps(first_table['cells'][0], indent=6)}")

print("\n" + "="*60)
print("Analysis:")
print("="*60)
print("\nThis dataset contains:")
print("- Ground truth JSON annotations for table structure")
print("- References to source PDFs via __url__")
print("- Cell-level annotations with headers, spans, etc.")
print("\nTo benchmark extraction methods, we need:")
print("1. Download the actual PDF files from the URLs")
print("2. OR: Compare different table parsing libraries on the ground truth")
print("3. OR: Use a different dataset that includes PDFs")
