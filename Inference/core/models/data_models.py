"""
Data Models Module

This module defines the core data structures used throughout the EnConda-Bench
inference system. It provides Pydantic models for type validation and serialization
of analysis results, error information, and processing records.

Key Models:
- ErrorInfo: Represents detected environment configuration errors
- TokenUsage: Tracks API token consumption for cost monitoring
- AnalysisResult: Contains complete analysis output including errors and fixes
- ProcessingRecord: Records detailed processing information for audit trails

All models use Pydantic for automatic validation, serialization, and documentation
generation, ensuring data consistency across the entire system.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ErrorInfo(BaseModel):
    """Error information model"""
    error_type: str = Field(description="Error type, such as E1, E2, etc.")
    error_description: str = Field(description="Error description")
    fix_answer: str = Field(description="Fix recommendation")

class TokenUsage(BaseModel):
    """Token usage statistics model"""
    input_tokens: int = Field(default=0, description="Number of input tokens")
    output_tokens: int = Field(default=0, description="Number of output tokens")
    total_tokens: int = Field(default=0, description="Total number of tokens")

class AnalysisResult(BaseModel):
    """Analysis result model"""
    repo_name: str = Field(description="Repository name")
    readme_name: str = Field(description="README file name")
    errors: List[ErrorInfo] = Field(default_factory=list, description="List of detected errors")
    shell_script: str = Field(default="", description="Generated shell script")
    raw_output: str = Field(default="", description="Raw output")
    token_usage: Optional[TokenUsage] = Field(default=None, description="Token usage statistics")

class ProcessingRecord(BaseModel):
    """Processing record model"""
    repo_name: str = Field(description="Repository name")
    readme_name: str = Field(description="README file name")
    input_prompt: str = Field(description="Input prompt")
    model_output: str = Field(description="Model output")
    errors_detected: List[ErrorInfo] = Field(default_factory=list, description="Detected errors")
    shell_script_path: str = Field(description="Shell script path")
    errors_json_path: str = Field(description="Error JSON file path")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp")
    success: bool = Field(default=True, description="Whether successful")
    error_message: Optional[str] = Field(default=None, description="Error message")
    token_usage: Optional[TokenUsage] = Field(default=None, description="Token usage statistics")