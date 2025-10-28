#!/usr/bin/env python3
"""
Evaluation System Usage Example

This module provides a complete example of how to use the evaluation system
for environment configuration analysis results. It demonstrates the basic
workflow and shows how to interpret evaluation results.

Key Features:
- Complete evaluation workflow demonstration
- Example configuration and setup
- Result interpretation and display
- Error handling and debugging guidance
"""

from evaluator import Evaluator

def main():
    """Run evaluation example"""
    
    # Configure paths
    results_dir = "results"  # Your model output results directory
    data_root_dir = "/path/to/your/data_root"  # Your original data root directory
    output_dir = "evaluation_output"  # Evaluation results output directory
    
    print("=== Environment Configuration Analysis Result Evaluation ===")
    print(f"Results directory: {results_dir}")
    print(f"Data root directory: {data_root_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create evaluator
    evaluator = Evaluator(
        results_dir=results_dir,
        data_root_dir=data_root_dir,
        output_dir=output_dir
    )
    
    # Run evaluation
    try:
        overall_result = evaluator.run_evaluation()
        
        print("\n=== Evaluation Results Summary ===")
        print(f"Total evaluated files: {overall_result.total_files}")
        
        print(f"\nError type metrics:")
        print(f"  Precision: {overall_result.overall_error_type_metrics.precision:.3f}")
        print(f"  Recall: {overall_result.overall_error_type_metrics.recall:.3f}")
        print(f"  F1 Score: {overall_result.overall_error_type_metrics.f1:.3f}")
        
        print(f"\nText similarity metrics:")
        print(f"  Description accuracy: {overall_result.overall_description_accuracy:.3f}")
        print(f"  Fix solution accuracy: {overall_result.overall_golden_answer_accuracy:.3f}")
        
        print(f"\nBreakdown by error type:")
        for error_type, metrics in overall_result.error_type_breakdown.items():
            print(f"  {error_type}: P={metrics.precision:.3f}, R={metrics.recall:.3f}, F1={metrics.f1:.3f}")
        
        print(f"\nDetailed results saved to {output_dir} directory")
        
    except Exception as e:
        print(f"Error occurred during evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()