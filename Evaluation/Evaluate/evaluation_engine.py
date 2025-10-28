#!/usr/bin/env python3
"""
Evaluation Engine Module

This module contains the core evaluation logic for the environment configuration
analysis system. It orchestrates the evaluation process, handles data loading,
performs error matching, and calculates comprehensive evaluation metrics.

Key Features:
- Core evaluation logic and workflow orchestration
- JSON data loading and parsing for predictions and golden answers
- Single file and batch evaluation capabilities
- Comprehensive metrics calculation (precision, recall, F1)
- Text similarity evaluation integration
- Result aggregation and breakdown analysis
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from evaluation_models import *
from error_matcher import ErrorMatcher
from text_similarity_evaluator import TextSimilarityEvaluator

class EvaluationEngine:
    """Core evaluation engine for processing and evaluating results"""
    
    def __init__(self, evaluation_model_name: Optional[str] = None):
        self.error_matcher = ErrorMatcher(evaluation_model_name)
        self.similarity_evaluator = TextSimilarityEvaluator(evaluation_model_name)
    
    def load_predicted_result(self, json_file_path: Path) -> PredictedResult:
        """Load model prediction results"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert error format
        errors = []
        for error_data in data.get('errors', []):
            errors.append(PredictedError(**error_data))
        
        return PredictedResult(
            repo_name=data.get('repo_name', ''),
            readme_name=data.get('readme_name', ''),
            errors=errors,
            shell_script=data.get('shell_script'),
            raw_output=data.get('raw_output', '')
        )
    
    def load_golden_answer(self, json_file_path: Path) -> GoldenAnswer:
        """Load golden answer"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert error format
        errors = []
        for error_data in data.get('errors', []):
            errors.append(GoldenError(**error_data))
        
        return GoldenAnswer(
            readme_name=data.get('readme_name', ''),
            errors=errors
        )
    
    def evaluate_single_file(self, predicted_result: PredictedResult, golden_answer: GoldenAnswer) -> FileEvaluationResult:
        """Evaluate results for a single file"""
        
        # Match errors
        error_matches = self.error_matcher.match_errors(
            predicted_result.errors, 
            golden_answer.errors
        )
        
        # Evaluate each error
        error_evaluations = []
        for pred_error, matched_golden in error_matches:
            evaluation = self._evaluate_single_error(pred_error, matched_golden)
            error_evaluations.append(evaluation)
        
        # Calculate error type metrics
        error_type_metrics = self._calculate_error_type_metrics(
            predicted_result.errors, 
            golden_answer.errors
        )
        
        # Calculate description and fix solution accuracy
        description_accuracy = self._calculate_text_accuracy(
            error_evaluations, 
            'description'
        )
        golden_answer_accuracy = self._calculate_text_accuracy(
            error_evaluations, 
            'golden_answer'
        )
        
        return FileEvaluationResult(
            readme_name=predicted_result.readme_name,
            repo_name=predicted_result.repo_name,
            golden_errors_count=len(golden_answer.errors),
            predicted_errors_count=len(predicted_result.errors),
            error_evaluations=error_evaluations,
            error_type_metrics=error_type_metrics,
            description_accuracy=description_accuracy,
            golden_answer_accuracy=golden_answer_accuracy
        )
    
    def _evaluate_single_error(self, pred_error: PredictedError, matched_golden: Optional[GoldenError]) -> ErrorEvaluationResult:
        """Evaluate a single error"""
        
        error_type_correct = False
        description_similar = None
        golden_answer_similar = None
        
        if matched_golden is not None:
            # Check if error type is correct
            error_type_correct = pred_error.error_type == matched_golden.error_type
            
            # Evaluate description similarity
            description_similar = self.similarity_evaluator.evaluate_similarity(
                pred_error.error_description,
                matched_golden.error_description,
                "description"
            )
            
            # Evaluate fix solution similarity
            golden_answer_similar = self.similarity_evaluator.evaluate_similarity(
                pred_error.fix_answer,
                matched_golden.golden_answer,
                "golden_answer"
            )
        
        return ErrorEvaluationResult(
            predicted_error=pred_error,
            matched_golden_error=matched_golden,
            error_type_correct=error_type_correct,
            description_similar=description_similar,
            golden_answer_similar=golden_answer_similar
        )
    
    def _calculate_error_type_metrics(self, predicted_errors: List[PredictedError], golden_errors: List[GoldenError]) -> ErrorTypeMetrics:
        """Calculate evaluation metrics for error types"""
        
        metrics_data = self.error_matcher.calculate_error_type_metrics(
            predicted_errors, 
            golden_errors
        )
        
        tp = metrics_data["true_positives"]
        fp = metrics_data["false_positives"]
        fn = metrics_data["false_negatives"]
        
        # Calculate precision, recall, F1 score
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return ErrorTypeMetrics(
            precision=precision,
            recall=recall,
            f1=f1,
            true_positives=tp,
            false_positives=fp,
            false_negatives=fn
        )
    
    def _calculate_text_accuracy(self, error_evaluations: List[ErrorEvaluationResult], text_type: str) -> float:
        """Calculate text accuracy"""
        
        total_matched = 0
        correct_count = 0
        
        for evaluation in error_evaluations:
            if evaluation.matched_golden_error is not None:
                total_matched += 1
                
                if text_type == 'description' and evaluation.description_similar:
                    if evaluation.description_similar.is_similar:
                        correct_count += 1
                elif text_type == 'golden_answer' and evaluation.golden_answer_similar:
                    if evaluation.golden_answer_similar.is_similar:
                        correct_count += 1
        
        return correct_count / total_matched if total_matched > 0 else 0.0
    
    def aggregate_results(self, file_results: List[FileEvaluationResult]) -> OverallEvaluationResult:
        """Aggregate evaluation results from all files"""
        
        if not file_results:
            return OverallEvaluationResult(
                total_files=0,
                overall_error_type_metrics=ErrorTypeMetrics(
                    precision=0.0, recall=0.0, f1=0.0,
                    true_positives=0, false_positives=0, false_negatives=0
                ),
                overall_description_accuracy=0.0,
                overall_golden_answer_accuracy=0.0,
                per_file_results=[],
                error_type_breakdown={}
            )
        
        # Aggregate error type metrics
        total_tp = sum(result.error_type_metrics.true_positives for result in file_results)
        total_fp = sum(result.error_type_metrics.false_positives for result in file_results)
        total_fn = sum(result.error_type_metrics.false_negatives for result in file_results)
        
        overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0
        
        overall_error_type_metrics = ErrorTypeMetrics(
            precision=overall_precision,
            recall=overall_recall,
            f1=overall_f1,
            true_positives=total_tp,
            false_positives=total_fp,
            false_negatives=total_fn
        )
        
        # Calculate overall text accuracy
        overall_description_accuracy = sum(result.description_accuracy for result in file_results) / len(file_results)
        overall_golden_answer_accuracy = sum(result.golden_answer_accuracy for result in file_results) / len(file_results)
        
        # Error type breakdown metrics
        error_type_breakdown = self._calculate_error_type_breakdown(file_results)
        
        return OverallEvaluationResult(
            total_files=len(file_results),
            overall_error_type_metrics=overall_error_type_metrics,
            overall_description_accuracy=overall_description_accuracy,
            overall_golden_answer_accuracy=overall_golden_answer_accuracy,
            per_file_results=file_results,
            error_type_breakdown=error_type_breakdown
        )
    
    def _calculate_error_type_breakdown(self, file_results: List[FileEvaluationResult]) -> Dict[str, ErrorTypeMetrics]:
        """Calculate breakdown metrics by error type"""
        
        error_type_stats = {}
        
        # Collect statistics for each error type
        for file_result in file_results:
            for evaluation in file_result.error_evaluations:
                error_type = evaluation.predicted_error.error_type
                
                if error_type not in error_type_stats:
                    error_type_stats[error_type] = {"tp": 0, "fp": 0, "fn": 0}
                
                if evaluation.matched_golden_error is not None:
                    if evaluation.error_type_correct:
                        error_type_stats[error_type]["tp"] += 1
                    else:
                        error_type_stats[error_type]["fp"] += 1
                else:
                    error_type_stats[error_type]["fp"] += 1
        
        # Calculate metrics for each error type
        breakdown = {}
        for error_type, stats in error_type_stats.items():
            tp, fp, fn = stats["tp"], stats["fp"], stats["fn"]
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            
            breakdown[error_type] = ErrorTypeMetrics(
                precision=precision,
                recall=recall,
                f1=f1,
                true_positives=tp,
                false_positives=fp,
                false_negatives=fn
            )
        
        return breakdown