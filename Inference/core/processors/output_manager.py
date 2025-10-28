"""
Output Management Module

This module handles all output operations for the EnConda-Bench-Open inference system.
It manages the organization, storage, and reporting of analysis results, processing
records, and summary statistics.

Usage:
    output_manager = OutputManager("./output")
    errors_path, script_path = output_manager.save_analysis_result(result, repo, readme)
    record = output_manager.create_processing_record(...)
    output_manager.save_processing_record(record)
    output_manager.generate_summary_report()
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List
import logging
from ..models.data_models import AnalysisResult, ProcessingRecord, ErrorInfo

logger = logging.getLogger(__name__)

class OutputManager:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create main output directories
        self.results_dir = self.output_dir / "results"
        self.logs_dir = self.output_dir / "logs"
        self.results_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize record file
        self.records_file = self.output_dir / "processing_records.jsonl"
        
    def save_analysis_result(self, result: AnalysisResult, repo_name: str, readme_name: str) -> tuple[str, str]:
        """Save analysis results, return error JSON file path and shell script file path"""
        # Create repository-specific directory
        repo_dir = self.results_dir / repo_name
        repo_dir.mkdir(exist_ok=True)
        
        # Save error information JSON
        errors_data = {
            "repo_name": repo_name,
            "readme_name": readme_name,
            "timestamp": datetime.now().isoformat(),
            "errors": [
                {
                    "error_type": error.error_type,
                    "error_description": error.error_description,
                    "fix_answer": error.fix_answer
                }
                for error in result.errors
            ]
        }
        
        errors_json_path = repo_dir / f"{readme_name}_errors.json"
        with open(errors_json_path, 'w', encoding='utf-8') as f:
            json.dump(errors_data, f, ensure_ascii=False, indent=2)
        
        # Save shell script
        shell_script_path = repo_dir / f"{readme_name}_setup.sh"
        with open(shell_script_path, 'w', encoding='utf-8') as f:
            f.write(result.shell_script or "#!/bin/bash\necho 'No setup script generated'")
        
        # Set shell script execution permissions
        try:
            os.chmod(shell_script_path, 0o755)
        except OSError:
            pass  # Ignore permission setting errors
        
        logger.info(f"Analysis results saved to: {repo_dir}")
        return str(errors_json_path), str(shell_script_path)
    
    def save_processing_record(self, record: ProcessingRecord):
        """Save processing record to JSONL file"""
        try:
            with open(self.records_file, 'a', encoding='utf-8') as f:
                # Use model_dump() then manually convert to JSON
                record_dict = record.model_dump()
                json_str = json.dumps(record_dict, ensure_ascii=False)
                f.write(json_str + '\n')
            logger.info(f"Processing record saved: {record.repo_name}")
        except Exception as e:
            logger.error(f"Failed to save processing record: {e}")
    
    def create_processing_record(self, 
                               repo_name: str,
                               readme_name: str,
                               input_prompt: str,
                               model_output: str,
                               errors: List[ErrorInfo],
                               shell_script_path: str,
                               errors_json_path: str,
                               success: bool = True,
                               error_message: str = None,
                               token_usage: dict = None) -> ProcessingRecord:
        """Create processing record"""
        from ..models.data_models import TokenUsage
        
        # Process token usage information
        token_usage_obj = None
        if token_usage:
            token_usage_obj = TokenUsage(
                input_tokens=token_usage.get('input_tokens', 0),
                output_tokens=token_usage.get('output_tokens', 0),
                total_tokens=token_usage.get('total_tokens', 0)
            )
        
        return ProcessingRecord(
            repo_name=repo_name,
            readme_name=readme_name,
            input_prompt=input_prompt,
            model_output=model_output,
            errors_detected=errors,
            shell_script_path=shell_script_path,
            errors_json_path=errors_json_path,
            timestamp=datetime.now().isoformat(),
            success=success,
            error_message=error_message,
            token_usage=token_usage_obj
        )
    
    def _load_processing_records(self) -> List[dict]:
        """Load processing records from JSONL file"""
        records = []
        try:
            with open(self.records_file, 'r', encoding='utf-8') as f:
                for line in f:
                    records.append(json.loads(line.strip()))
        except Exception as e:
            logger.error(f"Failed to read processing records: {e}")
            raise
        return records
    
    def _calculate_basic_statistics(self, records: List[dict]) -> dict:
        """Calculate basic processing statistics"""
        total_repos = len(records)
        successful_repos = sum(1 for r in records if r['success'])
        failed_repos = total_repos - successful_repos
        total_errors = sum(len(r['errors_detected']) for r in records)
        
        success_rate = f"{(successful_repos/total_repos*100):.2f}%" if total_repos > 0 else "0%"
        
        return {
            "total_repositories": total_repos,
            "successful_processing": successful_repos,
            "failed_processing": failed_repos,
            "total_errors_found": total_errors,
            "success_rate": success_rate
        }
    
    def _calculate_error_type_distribution(self, records: List[dict]) -> dict:
        """Calculate error type distribution statistics"""
        error_type_counts = {}
        for record in records:
            for error in record['errors_detected']:
                error_type = error['error_type']
                error_type_counts[error_type] = error_type_counts.get(error_type, 0) + 1
        return error_type_counts
    
    def _calculate_token_statistics(self, records: List[dict]) -> dict:
        """Calculate token usage statistics"""
        total_input_tokens = 0
        total_output_tokens = 0
        total_tokens = 0
        successful_records_with_tokens = 0
        
        for record in records:
            if self._has_valid_token_usage(record):
                token_usage = record['token_usage']
                total_input_tokens += token_usage.get('input_tokens', 0)
                total_output_tokens += token_usage.get('output_tokens', 0)
                total_tokens += token_usage.get('total_tokens', 0)
                successful_records_with_tokens += 1
        
        # Calculate averages
        avg_input_tokens = self._safe_divide(total_input_tokens, successful_records_with_tokens)
        avg_output_tokens = self._safe_divide(total_output_tokens, successful_records_with_tokens)
        avg_total_tokens = self._safe_divide(total_tokens, successful_records_with_tokens)
        
        return {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_tokens,
            "average_input_tokens": round(avg_input_tokens, 2),
            "average_output_tokens": round(avg_output_tokens, 2),
            "average_total_tokens": round(avg_total_tokens, 2),
            "repositories_with_token_data": successful_records_with_tokens
        }
    
    def _has_valid_token_usage(self, record: dict) -> bool:
        """Check if record has valid token usage data"""
        return (record['success'] and 
                'token_usage' in record and 
                record['token_usage'] is not None)
    
    def _safe_divide(self, numerator: float, denominator: int) -> float:
        """Safely divide two numbers, return 0 if denominator is 0"""
        return numerator / denominator if denominator > 0 else 0
    
    def _get_failed_repositories(self, records: List[dict]) -> List[dict]:
        """Get list of failed repositories with error messages"""
        return [
            {
                "repo_name": r['repo_name'],
                "error_message": r.get('error_message', 'Unknown error')
            }
            for r in records if not r['success']
        ]
    
    def _build_summary_report(self, basic_stats: dict, token_stats: dict, 
                             error_distribution: dict, failed_repos: List[dict]) -> dict:
        """Build the complete summary report structure"""
        return {
            "summary": basic_stats,
            "token_statistics": token_stats,
            "error_type_distribution": error_distribution,
            "failed_repositories": failed_repos,
            "generated_at": datetime.now().isoformat()
        }
    
    def _save_report_to_file(self, report: dict) -> Path:
        """Save report to JSON file"""
        report_path = self.output_dir / "summary_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return report_path
    
    def _print_summary_to_console(self, basic_stats: dict, error_distribution: dict):
        """Print summary information to console"""
        print(f"\n=== Processing Summary ===")
        print(f"Total repositories: {basic_stats['total_repositories']}")
        print(f"Successfully processed: {basic_stats['successful_processing']}")
        print(f"Failed processing: {basic_stats['failed_processing']}")
        print(f"Total errors found: {basic_stats['total_errors_found']}")
        print(f"Success rate: {basic_stats['success_rate']}")
        
        if error_distribution:
            print(f"\nError type distribution:")
            for error_type, count in sorted(error_distribution.items(), 
                                          key=lambda x: x[1], reverse=True):
                print(f"  {error_type}: {count}")
    
    def generate_summary_report(self):
        """Generate processing summary report"""
        if not self.records_file.exists():
            logger.warning("Processing record file not found")
            return
        
        try:
            # Load and process data
            records = self._load_processing_records()
            
            # Calculate statistics
            basic_stats = self._calculate_basic_statistics(records)
            token_stats = self._calculate_token_statistics(records)
            error_distribution = self._calculate_error_type_distribution(records)
            failed_repos = self._get_failed_repositories(records)
            
            # Build and save report
            report = self._build_summary_report(basic_stats, token_stats, 
                                              error_distribution, failed_repos)
            report_path = self._save_report_to_file(report)
            
            # Output results
            logger.info(f"Summary report generated: {report_path}")
            self._print_summary_to_console(basic_stats, error_distribution)
            
        except Exception as e:
            logger.error(f"Failed to generate summary report: {e}")
            return