#!/usr/bin/env python3
"""
Main Evaluation Script

This script serves as the main entry point for running the evaluation system.
It handles command-line arguments, validates input paths, and orchestrates
the complete evaluation process for environment configuration analysis results.

Key Features:
- Command-line interface for evaluation parameters
- Input path validation and error handling
- Integration with the main Evaluator class
- Comprehensive error reporting and logging
"""

import argparse
from pathlib import Path
from evaluator import Evaluator

def main():
    parser = argparse.ArgumentParser(description="Evaluate environment configuration analysis results")
    parser.add_argument(
        "--results_dir", 
        type=str, 
        required=True,
        help="Model output results directory (results folder path)"
    )
    parser.add_argument(
        "--data_root_dir", 
        type=str, 
        required=True,
        help="Original data root directory (directory containing error_gen_* folders)"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default="evaluation_output",
        help="Evaluation results output directory (default: evaluation_output)"
    )
    parser.add_argument(
        "--evaluation_model", 
        type=str, 
        default="gpt-4o-mini",
        help="Model name for evaluation (default: gpt-4o-mini)"
    )
    
    args = parser.parse_args()
    
    # Validate paths
    results_dir = Path(args.results_dir)
    data_root_dir = Path(args.data_root_dir)
    
    if not results_dir.exists():
        print(f"Error: Results directory does not exist: {results_dir}")
        return
    
    if not data_root_dir.exists():
        print(f"Error: Data root directory does not exist: {data_root_dir}")
        return
    
    # Create evaluator and run evaluation
    evaluator = Evaluator(
        results_dir=str(results_dir),
        data_root_dir=str(data_root_dir),
        output_dir=args.output_dir,
        evaluation_model_name=args.evaluation_model
    )
    
    try:
        overall_result = evaluator.run_evaluation()
        print("\n=== Evaluation Completed ===")
        
    except Exception as e:
        print(f"Error occurred during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()