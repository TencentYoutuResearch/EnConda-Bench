#!/usr/bin/env python3
"""
Evaluation Data Models Module

This module defines the data structures and models used throughout the evaluation system.
It provides Pydantic models for type safety and data validation for various evaluation
components including golden answers, predicted results, and evaluation metrics.

Key Features:
- Pydantic models for type safety and validation
- Golden answer and predicted result structures
- Evaluation metrics and results models
- Text similarity evaluation results
- Comprehensive error evaluation structures
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class GoldenError(BaseModel):
    """Error information in golden answer"""
    error_type: str
    error_description: str
    golden_answer: str

class GoldenAnswer(BaseModel):
    """Golden answer data structure"""
    readme_name: str
    errors: List[GoldenError]

class PredictedError(BaseModel):
    """Model predicted error information"""
    error_type: str
    error_description: str
    fix_answer: str

class PredictedResult(BaseModel):
    """Model prediction result"""
    repo_name: str
    readme_name: str
    errors: List[PredictedError]
    shell_script: Optional[str] = None
    raw_output: str

class ErrorTypeMetrics(BaseModel):
    """Evaluation metrics for error types"""
    precision: float
    recall: float
    f1: float
    true_positives: int
    false_positives: int
    false_negatives: int

class TextSimilarityResult(BaseModel):
    """Text similarity evaluation result"""
    is_similar: bool
    confidence: float
    reason: str

class ErrorEvaluationResult(BaseModel):
    """Evaluation result for a single error"""
    predicted_error: PredictedError
    matched_golden_error: Optional[GoldenError]
    error_type_correct: bool
    description_similar: Optional[TextSimilarityResult]
    golden_answer_similar: Optional[TextSimilarityResult]

class FileEvaluationResult(BaseModel):
    """Evaluation result for a single file"""
    readme_name: str
    repo_name: str
    golden_errors_count: int
    predicted_errors_count: int
    error_evaluations: List[ErrorEvaluationResult]
    error_type_metrics: ErrorTypeMetrics
    description_accuracy: float
    golden_answer_accuracy: float

class OverallEvaluationResult(BaseModel):
    """Overall evaluation result"""
    total_files: int
    overall_error_type_metrics: ErrorTypeMetrics
    overall_description_accuracy: float
    overall_golden_answer_accuracy: float
    per_file_results: List[FileEvaluationResult]
    error_type_breakdown: Dict[str, ErrorTypeMetrics]