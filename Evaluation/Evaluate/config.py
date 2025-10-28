#!/usr/bin/env python3
"""
Configuration Management Module

This module handles the configuration settings for the evaluation system.
It loads environment variables and provides default values for API keys,
model names, and other evaluation parameters.

Key Features:
- Environment variable loading with .env file support
- OpenAI API configuration management
- Default model and parameter settings
- Secure API key handling
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for evaluation system"""
    
    def __init__(self):
        # OpenAI API configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        # Default evaluation model
        self.evaluation_model_name = os.getenv("EVALUATION_MODEL_NAME", "gpt-4o-mini")
        
        # Text similarity evaluation thresholds
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        # Evaluation parameters
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
    def validate(self):
        """Validate configuration settings"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required but not set")
        
        if self.similarity_threshold < 0 or self.similarity_threshold > 1:
            raise ValueError("SIMILARITY_THRESHOLD must be between 0 and 1")