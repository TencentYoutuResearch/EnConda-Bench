#!/usr/bin/env python3
"""
Main Evaluator Module

This module coordinates the entire evaluation process for environment configuration
analysis results. It manages the evaluation workflow, handles file processing,
and generates comprehensive evaluation reports with metrics and statistics.

Key Features:
- Complete evaluation workflow orchestration
- File discovery and golden answer matching
- Progress tracking with detailed statistics
- Result aggregation and report generation
- Error handling and logging throughout the process
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
from evaluation_engine import EvaluationEngine
from evaluation_models import OverallEvaluationResult

class Evaluator:
    """Main evaluator for coordinating the evaluation process"""
    
    def __init__(self, results_dir: str, data_root_dir: str, output_dir: str = "evaluation_output", evaluation_model_name: Optional[str] = None):
        """
        Initialize evaluator
        
        Args:
            results_dir: Model output results directory (results folder)
            data_root_dir: Original data root directory (containing error_gen_* folders)
            output_dir: Evaluation results output directory
            evaluation_model_name: Model name for evaluation (default uses gpt-4o-mini)
        """
        self.results_dir = Path(results_dir)
        self.data_root_dir = Path(data_root_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.evaluation_engine = EvaluationEngine(evaluation_model_name)
    
    def run_evaluation(self) -> OverallEvaluationResult:
        """Run complete evaluation process"""
        
        print("Starting evaluation...")
        print(f"Results directory: {self.results_dir}")
        print(f"Data root directory: {self.data_root_dir}")
        
        # Find all result files
        result_files = self._find_result_files()
        print(f"Found {len(result_files)} result files")
        
        file_results = []
        
        # Use tqdm to show progress bar
        with tqdm(result_files, desc="Evaluation progress", unit="files") as pbar:
            for result_file in pbar:
                try:
                    pbar.set_description(f"Evaluating: {result_file.name}")
                    
                    # Load predicted result
                    predicted_result = self.evaluation_engine.load_predicted_result(result_file)
                    
                    # Find corresponding golden answer
                    golden_answer_file = self._find_golden_answer_file(predicted_result.readme_name)
                    
                    if golden_answer_file is None:
                        tqdm.write(f"⚠️  Golden answer not found for {predicted_result.readme_name}")
                        continue
                    
                    # Load golden answer
                    golden_answer = self.evaluation_engine.load_golden_answer(golden_answer_file)
                    
                    # Evaluate single file
                    file_result = self.evaluation_engine.evaluate_single_file(
                        predicted_result, 
                        golden_answer
                    )
                    
                    file_results.append(file_result)
                    
                    # Update progress bar postfix information
                    pbar.set_postfix({
                        'Completed': len(file_results),
                        'Predicted errors': file_result.predicted_errors_count,
                        'Golden errors': file_result.golden_errors_count,
                        'F1': f"{file_result.error_type_metrics.f1:.3f}"
                    })
                    
                except Exception as e:
                    tqdm.write(f"❌ Error evaluating file {result_file.name}: {e}")
                    continue
        
        # Aggregate results
        overall_result = self.evaluation_engine.aggregate_results(file_results)
        
        # Save results
        self._save_evaluation_results(overall_result)
        
        print(f"\n🎉 Evaluation completed!")
        print(f"\n📊 Overall evaluation results (aggregated metrics from {overall_result.total_files} files):")
        print(f"{'='*60}")
        print(f"📁 Total evaluated files: {overall_result.total_files}")
        print(f"\n🎯 Error type identification metrics (overall):")
        print(f"   Precision: {overall_result.overall_error_type_metrics.precision:.4f}")
        print(f"   Recall:    {overall_result.overall_error_type_metrics.recall:.4f}")
        print(f"   F1 Score:  {overall_result.overall_error_type_metrics.f1:.4f}")
        print(f"   TP: {overall_result.overall_error_type_metrics.true_positives}, "
              f"FP: {overall_result.overall_error_type_metrics.false_positives}, "
              f"FN: {overall_result.overall_error_type_metrics.false_negatives}")
        
        print(f"\n📝 Text similarity metrics (overall):")
        print(f"   Description accuracy:     {overall_result.overall_description_accuracy:.4f}")
        print(f"   Fix solution accuracy:    {overall_result.overall_golden_answer_accuracy:.4f}")
        
        if overall_result.error_type_breakdown:
            print(f"\n🔍 Breakdown by error type (overall):")
            for error_type, metrics in overall_result.error_type_breakdown.items():
                print(f"   {error_type}: P={metrics.precision:.3f}, R={metrics.recall:.3f}, F1={metrics.f1:.3f}")
        
        print(f"{'='*60}")
        
        return overall_result
    
    def _find_result_files(self) -> List[Path]:
        """Find all result JSON files"""
        result_files = []
        
        for subfolder in self.results_dir.iterdir():
            if subfolder.is_dir():
                # Look for JSON files
                for json_file in subfolder.glob("*.json"):
                    if "error" in json_file.name.lower():  # Only process error analysis files
                        result_files.append(json_file)
        
        return result_files
    
    def _find_golden_answer_file(self, readme_name: str) -> Optional[Path]:
        """
        Find corresponding golden answer file based on readme_name
        
        Args:
            readme_name: e.g., "README_1.md"
        """
        
        # Traverse all repo folders under data root directory
        for repo_folder in self.data_root_dir.iterdir():
            if not repo_folder.is_dir():
                continue
            
            # Traverse all subfolders under repo folder (named after readme_name)
            for readme_folder in repo_folder.iterdir():
                if not readme_folder.is_dir():
                    continue
                
                # Check if folder name matches readme_name
                readme_base_name = readme_name.rsplit('.', 1)[0] if '.' in readme_name else readme_name
                
                # Multiple matching strategies
                is_match = (
                    readme_folder.name == readme_name or  # Exact match
                    readme_folder.name == readme_base_name or  # Match without extension
                    readme_base_name in readme_folder.name or  # Contains match
                    readme_folder.name in readme_base_name  # Reverse contains match
                )
                
                if is_match:
                    # Look for README.json file
                    json_file = readme_folder / "README.json"
                    if json_file.exists():
                        return json_file
        
        return None
    
    def _save_evaluation_results(self, overall_result: OverallEvaluationResult):
        """Save evaluation results"""
        
        # Save detailed results
        detailed_result_file = self.output_dir / "detailed_evaluation_results.json"
        with open(detailed_result_file, 'w', encoding='utf-8') as f:
            json.dump(overall_result.model_dump(), f, ensure_ascii=False, indent=2)
        
        # Save summary results
        summary_result = {
            "total_files": overall_result.total_files,
            "overall_metrics": {
                "error_type": {
                    "precision": overall_result.overall_error_type_metrics.precision,
                    "recall": overall_result.overall_error_type_metrics.recall,
                    "f1_score": overall_result.overall_error_type_metrics.f1
                },
                "description_accuracy": overall_result.overall_description_accuracy,
                "fix_solution_accuracy": overall_result.overall_golden_answer_accuracy
            },
            "error_type_breakdown": {
                error_type: {
                    "precision": metrics.precision,
                    "recall": metrics.recall,
                    "f1_score": metrics.f1
                }
                for error_type, metrics in overall_result.error_type_breakdown.items()
            }
        }
        
        summary_result_file = self.output_dir / "evaluation_summary.json"
        with open(summary_result_file, 'w', encoding='utf-8') as f:
            json.dump(summary_result, f, ensure_ascii=False, indent=2)
        
        print(f"Detailed results saved to: {detailed_result_file}")
        print(f"Summary results saved to: {summary_result_file}")