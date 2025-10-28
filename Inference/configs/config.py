"""
Configuration Management Module

This module provides a unified configuration management system for the EnConda-Bench-Open
inference system. It defines the main Config class using Pydantic for type validation
and automatic configuration loading from YAML files.

Usage:
    config = Config.from_config_type("llm")
    config = Config.from_config_type("agent")
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ..utils.config_loader import config_loader

class Config(BaseModel):
    """Unified configuration class"""
    
    # OpenAI API configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API base URL")
    model_name: str = Field(default="gpt-4", description="Model name to use")
    max_tokens: int = Field(default=4000, description="Maximum number of tokens")
    temperature: float = Field(default=0.1, description="Temperature parameter")
    
    # Data path configuration
    data_root_dir: str = Field(default="./benchmark_data", description="Data root directory")
    source_root_dir: str = Field(default="./source_repos", description="Source code root directory")
    output_dir: str = Field(default="./output", description="Output directory")
    
    # Processing configuration
    sample_size: Optional[int] = Field(default=None, description="Sample size")
    random_seed: int = Field(default=42, description="Random seed")
    max_workers: int = Field(default=1, description="Maximum number of worker threads")
    
    # Error type file path
    error_types_file: str = Field(default="./configs/error_type.json", description="Error type definition file")
    
    # Agent execution configuration
    agent_executable: str = Field(default="python", description="Agent executable command")
    agent_script_path: str = Field(default="./agent/swe_agent_wrapper.py", description="Agent script path")
    agent_timeout: int = Field(default=300, description="Agent execution timeout in seconds")
    agent_work_dir: str = Field(default="./agent_workspace", description="Agent working directory")
    agent_config_template: str = Field(default="./configs/agent_config_template.json", description="Agent configuration template")
    swe_agent_path: str = Field(default="./swe-agent", description="Path to SWE-agent installation")
    
    @classmethod
    def _extract_common_config(cls, config_data: dict, api_config_key: str = 'openai') -> dict:
        """Extract common configuration parameters"""
        api_config = config_data.get(api_config_key, {})
        data_config = config_data.get('data', {})
        output_config = config_data.get('output', {})
        processing_config = config_data.get('processing', {})
        
        return {
            'openai_api_key': api_config.get('api_key', ''),
            'openai_base_url': api_config.get('base_url', 'https://api.openai.com/v1'),
            'model_name': api_config.get('model_name', 'gpt-4'),
            'max_tokens': api_config.get('max_tokens', 4000),
            'temperature': api_config.get('temperature', 0.1),
            'data_root_dir': data_config.get('data_root_dir', './benchmark_data'),
            'source_root_dir': data_config.get('source_root_dir', './source_repos'),
            'output_dir': output_config.get('output_dir', './output'),
            'sample_size': data_config.get('sampling', {}).get('sample_size') if data_config.get('sampling', {}).get('enabled') else None,
            'random_seed': data_config.get('sampling', {}).get('random_seed', 42),
            'max_workers': processing_config.get('max_workers', 1)
        }
    
    @classmethod
    def from_config_type(cls, config_type: str = "llm") -> "Config":
        """Create Config instance from configuration file"""
        config_data = config_loader.load_config(config_type)
        
        if config_type == "llm":
            return cls(**cls._extract_common_config(config_data, 'openai'))
        elif config_type == "agent":
            # Get common configuration
            common_config = cls._extract_common_config(config_data, 'agent')
            
            # Add agent-specific configuration
            execution_config = config_data.get('execution', {})
            agent_specific_config = {
                'agent_executable': execution_config.get('agent_executable', 'python'),
                'agent_script_path': execution_config.get('agent_script_path', './agent/swe_agent_wrapper.py'),
                'agent_timeout': execution_config.get('agent_timeout', 300),
                'agent_work_dir': execution_config.get('agent_work_dir', './agent_workspace'),
                'agent_config_template': execution_config.get('agent_config_template', './configs/agent_config_template.json'),
                'swe_agent_path': execution_config.get('swe_agent_path', './swe-agent')
            }
            
            # Merge common and agent-specific configurations
            return cls(**{**common_config, **agent_specific_config})
        else:
            return cls()

# Global configuration instance (defaults to LLM configuration)
config = Config.from_config_type("llm")