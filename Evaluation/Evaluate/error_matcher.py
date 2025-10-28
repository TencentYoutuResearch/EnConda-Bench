#!/usr/bin/env python3
"""
Error Matcher Module

This module handles the matching between predicted errors and golden answer errors.
It implements intelligent matching strategies based on error types, descriptions,
and fix solutions to establish correspondences for evaluation purposes.

Key Features:
- Intelligent error matching with multiple criteria
- Similarity-based matching using LLM evaluation
- Configurable matching thresholds and scoring
- Error type set operations and metrics calculation
- Support for both exact and fuzzy matching strategies
"""

from typing import List, Dict, Tuple, Optional, Set
from evaluation_models import PredictedError, GoldenError, TextSimilarityResult
from text_similarity_evaluator import TextSimilarityEvaluator

class ErrorMatcher:
    """Error matcher for handling predicted and golden answer error matching"""
    
    def __init__(self, evaluation_model_name: Optional[str] = None):
        self.similarity_evaluator = TextSimilarityEvaluator(evaluation_model_name)
    
    def match_errors(self, predicted_errors: List[PredictedError], golden_errors: List[GoldenError]) -> List[Tuple[PredictedError, Optional[GoldenError]]]:
        """
        Match predicted errors with golden answer errors
        
        Returns: [(predicted_error, matched_golden_error), ...]
        If no matching golden error found, matched_golden_error is None
        """
        matches = []
        used_golden_indices = set()
        
        # First perform exact error_type matching
        for pred_error in predicted_errors:
            best_match = None
            best_match_idx = None
            best_score = 0.0
            
            for i, golden_error in enumerate(golden_errors):
                if i in used_golden_indices:
                    continue
                
                # Calculate match score
                score = self._calculate_match_score(pred_error, golden_error)
                
                if score > best_score and score > 0.5:  # Threshold is 0.5
                    best_score = score
                    best_match = golden_error
                    best_match_idx = i
            
            if best_match is not None:
                used_golden_indices.add(best_match_idx)
                matches.append((pred_error, best_match))
            else:
                matches.append((pred_error, None))
        
        return matches
    
    def _calculate_match_score(self, pred_error: PredictedError, golden_error: GoldenError) -> float:
        """
        Calculate match score between predicted error and golden error
        
        Matching strategy:
        1. error_type exact match: +0.6 points
        2. description similarity: +0.3 points  
        3. fix_answer similarity: +0.1 points
        """
        score = 0.0
        
        # error_type matching
        if pred_error.error_type == golden_error.error_type:
            score += 0.6
        
        # description similarity evaluation
        desc_similarity = self.similarity_evaluator.evaluate_similarity(
            pred_error.error_description, 
            golden_error.error_description, 
            "description"
        )
        if desc_similarity.is_similar:
            score += 0.3 * desc_similarity.confidence
        
        # golden_answer similarity evaluation
        golden_similarity = self.similarity_evaluator.evaluate_similarity(
            pred_error.fix_answer, 
            golden_error.golden_answer, 
            "golden_answer"
        )
        if golden_similarity.is_similar:
            score += 0.1 * golden_similarity.confidence
        
        return score
    
    def get_error_type_sets(self, predicted_errors: List[PredictedError], golden_errors: List[GoldenError]) -> Tuple[Set[str], Set[str]]:
        """Get predicted and golden error type sets"""
        pred_types = {error.error_type for error in predicted_errors}
        golden_types = {error.error_type for error in golden_errors}
        return pred_types, golden_types
    
    def calculate_error_type_metrics(self, predicted_errors: List[PredictedError], golden_errors: List[GoldenError]) -> Dict[str, int]:
        """Calculate TP, FP, FN for error types"""
        pred_types, golden_types = self.get_error_type_sets(predicted_errors, golden_errors)
        
        # Calculate metrics
        true_positives = len(pred_types & golden_types)  # Intersection
        false_positives = len(pred_types - golden_types)  # Predicted but not in golden
        false_negatives = len(golden_types - pred_types)  # In golden but not predicted
        
        return {
            "true_positives": true_positives,
            "false_positives": false_positives, 
            "false_negatives": false_negatives
        }