#!/usr/bin/env python3
"""
Text Similarity Evaluator Module

This module uses large language models to evaluate text similarity between predicted
and golden answers. It provides semantic similarity assessment for error descriptions
and fix solutions using OpenAI's API.

Key Features:
- LLM-based semantic similarity evaluation
- Support for different evaluation types (description, fix_answer)
- Batch processing capabilities
- JSON response parsing with fallback mechanisms
- Configurable similarity thresholds and models
"""

import json
from openai import OpenAI
from typing import List, Tuple, Optional
from config import Config
from evaluation_models import TextSimilarityResult

class TextSimilarityEvaluator:
    """Text similarity evaluator using LLM"""
    
    def __init__(self, evaluation_model_name: Optional[str] = None):
        self.config = Config()
        self.evaluation_model_name = evaluation_model_name or self.config.evaluation_model_name
        
        # Create OpenAI client using configured API key and base_url
        self.client = OpenAI(
            api_key=self.config.openai_api_key,
            base_url=self.config.openai_base_url
        )
        
    def evaluate_similarity(self, text1: str, text2: str, evaluation_type: str = "general") -> TextSimilarityResult:
        """
        Evaluate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text  
            evaluation_type: Evaluation type ("description" or "fix_answer")
        """
        try:
            prompt = self._build_similarity_prompt(text1, text2, evaluation_type)
            
            response = self.client.chat.completions.create(
                model=self.evaluation_model_name,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator for text similarity assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            if result_text:
                result_text = result_text.strip()
            else:
                result_text = ""
            return self._parse_similarity_result(result_text)
            
        except Exception as e:
            print(f"Text similarity evaluation failed: {e}")
            return TextSimilarityResult(
                is_similar=False,
                confidence=0.0,
                reason=f"Evaluation failed: {str(e)}"
            )
    
    def _build_similarity_prompt(self, text1: str, text2: str, evaluation_type: str) -> str:
        """Build prompt for similarity evaluation"""
        
        if evaluation_type == "description":
            task_description = """
You need to evaluate whether two error descriptions are semantically similar.
Two descriptions are considered similar if they describe the same type of problem, 
even if the wording is different.
"""
        elif evaluation_type == "golden_answer":
            task_description = """
You need to evaluate whether two fix solutions are semantically similar.
Two solutions are considered similar if they propose the same or equivalent 
approach to solve the problem, even if the specific commands or wording differ.
"""
        else:
            task_description = """
You need to evaluate whether two texts are semantically similar.
"""
        
        prompt = f"""
{task_description}

Text 1: {text1}

Text 2: {text2}

Please evaluate the similarity and respond in the following JSON format:
{{
    "is_similar": true/false,
    "confidence": 0.0-1.0,
    "reason": "Brief explanation of your decision"
}}

Consider the texts similar if they convey the same core meaning, even with different wording.
"""
        return prompt
    
    def _parse_similarity_result(self, result_text: str) -> TextSimilarityResult:
        """Parse similarity evaluation result"""
        try:
            # Try to extract JSON part
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = result_text[start_idx:end_idx]
                result_data = json.loads(json_str)
                
                return TextSimilarityResult(
                    is_similar=result_data.get("is_similar", False),
                    confidence=float(result_data.get("confidence", 0.0)),
                    reason=result_data.get("reason", "No reason provided")
                )
            else:
                # If no JSON format found, try simple parsing
                is_similar = "true" in result_text.lower() or "similar" in result_text.lower()
                return TextSimilarityResult(
                    is_similar=is_similar,
                    confidence=0.5,
                    reason="Parsed from non-JSON response"
                )
                
        except Exception as e:
            return TextSimilarityResult(
                is_similar=False,
                confidence=0.0,
                reason=f"Parsing failed: {str(e)}"
            )
    
    def batch_evaluate_similarity(self, text_pairs: List[Tuple[str, str]], evaluation_type: str = "general") -> List[TextSimilarityResult]:
        """Batch evaluate text similarity"""
        from tqdm import tqdm
        
        results = []
        with tqdm(text_pairs, desc=f"Evaluating {evaluation_type} similarity", unit="pairs") as pbar:
            for text1, text2 in pbar:
                result = self.evaluate_similarity(text1, text2, evaluation_type)
                results.append(result)
                pbar.set_postfix({'Similar': sum(1 for r in results if r.is_similar)})
        return results