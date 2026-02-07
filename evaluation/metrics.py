#!/usr/bin/env python3
"""
Evaluation metrics for table extraction
"""
import json
from typing import List, Dict, Any, Tuple
import time

def normalize_table(table: List[List[Any]]) -> List[List[str]]:
    """
    Normalize table to list of lists of strings
    """
    normalized = []
    for row in table:
        normalized_row = []
        for cell in row:
            # Convert to string and strip whitespace
            cell_str = str(cell).strip() if cell is not None else ""
            normalized_row.append(cell_str)
        normalized.append(normalized_row)
    return normalized

def calculate_cell_accuracy(predicted: List[List[str]], 
                            ground_truth: List[List[str]]) -> float:
    """
    Calculate cell-level accuracy
    
    Returns percentage of cells that match exactly
    """
    if not predicted or not ground_truth:
        return 0.0
    
    # Normalize dimensions
    pred_rows = len(predicted)
    gt_rows = len(ground_truth)
    
    pred_cols = max(len(row) for row in predicted) if predicted else 0
    gt_cols = max(len(row) for row in ground_truth) if ground_truth else 0
    
    # Compare cells
    total_cells = gt_rows * gt_cols
    correct_cells = 0
    
    for i in range(min(pred_rows, gt_rows)):
        for j in range(min(pred_cols, gt_cols)):
            pred_cell = predicted[i][j] if j < len(predicted[i]) else ""
            gt_cell = ground_truth[i][j] if j < len(ground_truth[i]) else ""
            
            if pred_cell == gt_cell:
                correct_cells += 1
    
    return (correct_cells / total_cells * 100) if total_cells > 0 else 0.0

def calculate_structure_accuracy(predicted: List[List[str]], 
                                 ground_truth: List[List[str]]) -> Dict[str, float]:
    """
    Calculate structural accuracy (dimensions)
    """
    pred_rows = len(predicted) if predicted else 0
    gt_rows = len(ground_truth) if ground_truth else 0
    
    pred_cols = max(len(row) for row in predicted) if predicted else 0
    gt_cols = max(len(row) for row in ground_truth) if ground_truth else 0
    
    row_match = pred_rows == gt_rows
    col_match = pred_cols == gt_cols
    
    return {
        'predicted_rows': pred_rows,
        'ground_truth_rows': gt_rows,
        'predicted_cols': pred_cols,
        'ground_truth_cols': gt_cols,
        'row_match': row_match,
        'col_match': col_match,
        'structure_match': row_match and col_match
    }

def evaluate_extraction(predicted_tables: List[List[List[str]]], 
                       ground_truth_tables: List[List[List[str]]],
                       method_name: str = "Unknown") -> Dict[str, Any]:
    """
    Evaluate table extraction results
    
    Args:
        predicted_tables: List of predicted tables
        ground_truth_tables: List of ground truth tables
        method_name: Name of extraction method
        
    Returns:
        Dictionary with evaluation metrics
    """
    start_time = time.time()
    
    # Basic stats
    num_predicted = len(predicted_tables)
    num_ground_truth = len(ground_truth_tables)
    
    results = {
        'method': method_name,
        'num_predicted_tables': num_predicted,
        'num_ground_truth_tables': num_ground_truth,
        'table_detection_recall': (num_predicted / num_ground_truth * 100) if num_ground_truth > 0 else 0,
        'per_table_metrics': []
    }
    
    # Evaluate each table
    total_cell_accuracy = 0
    total_structure_matches = 0
    
    for i, (pred, gt) in enumerate(zip(predicted_tables, ground_truth_tables)):
        # Normalize
        pred_norm = normalize_table(pred)
        gt_norm = normalize_table(gt)
        
        # Calculate metrics
        cell_acc = calculate_cell_accuracy(pred_norm, gt_norm)
        struct_acc = calculate_structure_accuracy(pred_norm, gt_norm)
        
        table_result = {
            'table_index': i,
            'cell_accuracy': cell_acc,
            'structure_accuracy': struct_acc
        }
        
        results['per_table_metrics'].append(table_result)
        
        total_cell_accuracy += cell_acc
        if struct_acc['structure_match']:
            total_structure_matches += 1
    
    # Aggregate metrics
    num_compared = min(num_predicted, num_ground_truth)
    if num_compared > 0:
        results['avg_cell_accuracy'] = total_cell_accuracy / num_compared
        results['structure_match_rate'] = (total_structure_matches / num_compared * 100)
    else:
        results['avg_cell_accuracy'] = 0
        results['structure_match_rate'] = 0
    
    results['evaluation_time'] = time.time() - start_time
    
    return results

def print_results(results: Dict[str, Any]):
    """Pretty print evaluation results"""
    print(f"\n{'='*60}")
    print(f"Evaluation Results: {results['method']}")
    print(f"{'='*60}")
    print(f"Tables Detected: {results['num_predicted_tables']} / {results['num_ground_truth_tables']}")
    print(f"Detection Recall: {results['table_detection_recall']:.2f}%")
    print(f"Avg Cell Accuracy: {results['avg_cell_accuracy']:.2f}%")
    print(f"Structure Match Rate: {results['structure_match_rate']:.2f}%")
    print(f"Evaluation Time: {results['evaluation_time']:.3f}s")
    print(f"{'='*60}\n")

def save_results(results: Dict[str, Any], output_path: str):
    """Save results to JSON file"""
    with open(output_path, 'w') as f:
        json.dumps(results, f, indent=2)
