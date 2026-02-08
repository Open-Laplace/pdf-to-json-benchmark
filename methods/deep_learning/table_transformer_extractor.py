#!/usr/bin/env python3
"""
PDF Table Extraction using Table Transformer (Microsoft)
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import time

try:
    from transformers import AutoImageProcessor, TableTransformerForObjectDetection
    from pdf2image import convert_from_path
    import torch
    from PIL import Image
    TT_AVAILABLE = True
except ImportError:
    TT_AVAILABLE = False

class TableTransformerExtractor:
    """Extract tables from PDF using Table Transformer model"""
    
    def __init__(self, verbose: bool = True, device: str = None):
        self.verbose = verbose
        self.extraction_time = 0
        
        if not TT_AVAILABLE:
            raise ImportError("Table Transformer dependencies not installed. "
                            "Run: uv pip install transformers[torch] pdf2image")
        
        # Auto-detect device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        if self.verbose:
            print(f"Initializing Table Transformer (device: {self.device})...")
        
        # Load detection model
        self.detection_processor = AutoImageProcessor.from_pretrained(
            "microsoft/table-transformer-detection"
        )
        self.detection_model = TableTransformerForObjectDetection.from_pretrained(
            "microsoft/table-transformer-detection"
        ).to(self.device)
        
        # Load structure recognition model
        self.structure_processor = AutoImageProcessor.from_pretrained(
            "microsoft/table-transformer-structure-recognition"
        )
        self.structure_model = TableTransformerForObjectDetection.from_pretrained(
            "microsoft/table-transformer-structure-recognition"  
        ).to(self.device)
        
        if self.verbose:
            print("Models loaded successfully!")
    
    def pdf_to_image(self, pdf_path: str, page_num: int = 1) -> Image.Image:
        """Convert PDF page to PIL Image"""
        images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=200)
        
        if not images:
            raise ValueError(f"Could not convert page {page_num}")
        
        return images[0]
    
    def detect_tables(self, image: Image.Image, confidence_threshold: float = 0.7) -> List[Dict]:
        """Detect table regions in image"""
        # Prepare image
        inputs = self.detection_processor(images=image, return_tensors="pt").to(self.device)
        
        # Run detection
        with torch.no_grad():
            outputs = self.detection_model(**inputs)
        
        # Post-process
        target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
        results = self.detection_processor.post_process_object_detection(
            outputs, threshold=confidence_threshold, target_sizes=target_sizes
        )[0]
        
        # Extract table bboxes
        tables = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            if self.detection_model.config.id2label[label.item()] == "table":
                tables.append({
                    "bbox": box.cpu().tolist(),
                    "confidence": score.item()
                })
        
        return tables
    
    def recognize_structure(self, image: Image.Image, table_bbox: List[float]) -> Dict:
        """Recognize table structure within detected region"""
        # Crop to table region
        x1, y1, x2, y2 = [int(coord) for coord in table_bbox]
        table_img = image.crop((x1, y1, x2, y2))
        
        # Prepare image
        inputs = self.structure_processor(images=table_img, return_tensors="pt").to(self.device)
        
        # Run structure recognition
        with torch.no_grad():
            outputs = self.structure_model(**inputs)
        
        # Post-process
        target_sizes = torch.tensor([table_img.size[::-1]]).to(self.device)
        results = self.structure_processor.post_process_object_detection(
            outputs, threshold=0.6, target_sizes=target_sizes
        )[0]
        
        # Extract cells, rows, columns
        cells = []
        rows = []
        columns = []
        
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            obj_type = self.structure_model.config.id2label[label.item()]
            bbox = box.cpu().tolist()
            
            if obj_type == "table row":
                rows.append({"bbox": bbox, "confidence": score.item()})
            elif obj_type == "table column":
                columns.append({"bbox": bbox, "confidence": score.item()})
            elif obj_type in ["table", "table cell"]:
                cells.append({"bbox": bbox, "confidence": score.item()})
        
        return {
            "rows": rows,
            "columns": columns,
            "cells": cells
        }
    
    def structure_to_table(self, structure: Dict, image: Image.Image) -> List[List[str]]:
        """Convert structure recognition to 2D table array"""
        # This is a simplified version - actual implementation would use OCR
        # For now, return placeholder based on detected structure
        
        rows = structure['rows']
        columns = structure['columns']
        
        num_rows = len(rows) if rows else 1
        num_cols = len(columns) if columns else 1
        
        # Create placeholder table
        table = []
        for r in range(num_rows):
            row = [f"Cell({r},{c})" for c in range(num_cols)]
            table.append(row)
        
        return table
    
    def extract_tables(self, pdf_path: str, pages: str = 'all') -> List[Dict[str, Any]]:
        """
        Extract tables from PDF using Table Transformer
        
        Args:
            pdf_path: Path to PDF file
            pages: Pages to process ('all' or page numbers)
            
        Returns:
            List of extracted tables with metadata
        """
        start_time = time.time()
        tables = []
        
        if self.verbose:
            print(f"Processing {Path(pdf_path).name} with Table Transformer")
        
        try:
            # Process first page
            page_num = 1
            
            if self.verbose:
                print(f"  Converting page {page_num} to image...")
            
            image = self.pdf_to_image(pdf_path, page_num)
            
            # Detect tables
            if self.verbose:
                print(f"  Detecting tables...")
            
            detected_tables = self.detect_tables(image)
            
            if self.verbose:
                print(f"  Found {len(detected_tables)} tables")
            
            # Process each detected table
            for idx, table_info in enumerate(detected_tables):
                if self.verbose:
                    print(f"  Recognizing structure for table {idx}...")
                
                structure = self.recognize_structure(image, table_info['bbox'])
                table_data = self.structure_to_table(structure, image)
                
                result = {
                    'page': page_num,
                    'table_index': idx,
                    'data': table_data,
                    'num_rows': len(table_data),
                    'num_cols': len(table_data[0]) if table_data else 0,
                    'confidence': table_info['confidence'],
                    'structure': {
                        'rows_detected': len(structure['rows']),
                        'cols_detected': len(structure['columns']),
                        'cells_detected': len(structure['cells'])
                    }
                }
                tables.append(result)
                
                if self.verbose:
                    print(f"    Detected: {result['num_rows']}x{result['num_cols']} "
                          f"(confidence: {table_info['confidence']:.2f})")
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return []
        
        self.extraction_time = time.time() - start_time
        
        if self.verbose:
            print(f"Extracted {len(tables)} tables in {self.extraction_time:.2f}s\n")
        
        return tables
    
    def tables_to_json(self, tables: List[Dict[str, Any]], 
                       include_metadata: bool = True) -> str:
        """Convert extracted tables to JSON format"""
        if include_metadata:
            output = {
                'num_tables': len(tables),
                'extraction_time': self.extraction_time,
                'method': 'table_transformer',
                'device': self.device,
                'tables': tables
            }
        else:
            output = {'tables': [t['data'] for t in tables]}
        
        return json.dumps(output, indent=2, default=str)
    
    def extract_to_file(self, pdf_path: str, output_path: str):
        """Extract tables and save to JSON file"""
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
        print("Usage: python table_transformer_extractor.py <pdf_file> [output.json]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output_tt.json"
    
    extractor = TableTransformerExtractor(verbose=True)
    extractor.extract_to_file(pdf_file, output_file)

if __name__ == "__main__":
    main()
