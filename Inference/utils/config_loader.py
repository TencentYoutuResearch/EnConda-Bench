"""
Configuration Loader Module

This module provides centralized configuration management for the EnConda-Bench
inference system. It handles loading, caching, and processing of YAML configuration
files for both LLM and Agent modes.

Key Features:
- YAML configuration file loading with error handling
- Environment variable substitution (${VAR_NAME} and $VAR_NAME formats)
- Configuration caching for improved performance
- Default configuration fallbacks when files are missing
- Support for both LLM and Agent configuration schemas
- Configuration validation and type safety
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Configuration loader"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / "configs"
        self._cached_configs = {}
    
    def load_config(self, config_type: str) -> Dict[str, Any]:
        """
        Load configuration of specified type
        
        Args:
            config_type: Configuration type, 'llm' or 'agent'
        
        Returns:
            Configuration dictionary
        """
        if config_type in self._cached_configs:
            return self._cached_configs[config_type].copy()
        
        config_file = self.config_dir / f"{config_type}_config.yaml"
        
        if not config_file.exists():
            logger.warning(f"Configuration file does not exist: {config_file}")
            return self._get_default_config(config_type)
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            # Process environment variable substitution
            config = self._process_env_vars(config)
            
            # Cache configuration
            self._cached_configs[config_type] = config.copy()
            
            logger.info(f"Successfully loaded configuration: {config_file}")
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration file {config_file}: {e}")
            return self._get_default_config(config_type)
    
    def _process_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process environment variables in configuration"""
        def replace_env_vars(obj):
            if isinstance(obj, dict):
                return {k: replace_env_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_env_vars(item) for item in obj]
            elif isinstance(obj, str):
                # Replace environment variable formats ${VAR_NAME} or $VAR_NAME
                if obj.startswith('${') and obj.endswith('}'):
                    env_var = obj[2:-1]
                    return os.getenv(env_var, obj)
                elif obj.startswith('$'):
                    env_var = obj[1:]
                    return os.getenv(env_var, obj)
                return obj
            else:
                return obj
        
        return replace_env_vars(config)
    
    def _get_default_config(self, config_type: str) -> Dict[str, Any]:
        """Get default configuration"""
        if config_type == 'llm':
            return {
                'openai': {
                    'api_key': os.getenv('OPENAI_API_KEY', ''),
                    'base_url': 'https://api.openai.com/v1',
                    'model_name': 'gpt-4',
                    'max_tokens': 4000,
                    'temperature': 0.1,
                    'timeout': 60
                },
                'data': {
                    'data_root_dir': './benchmark_data',
                    'source_root_dir': './source_repos',
                    'sampling': {
                        'enabled': False,
                        'sample_size': 100,
                        'random_seed': 42
                    }
                },
                'output': {
                    'output_dir': './output',
                    'verbose_logging': True,
                    'save_raw_output': True
                },
                'processing': {
                    'max_workers': 1,
                    'max_retries': 3,
                    'retry_delay': 5,
                    'skip_existing': True
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'file': './logs/llm_analysis.log'
                }
            }
        elif config_type == 'agent':
            return {
                'agent': {
                    'type': 'simple',
                    'model_name': 'gpt-4',
                    'max_tokens': 4000,
                    'temperature': 0.1,
                    'api_key': os.getenv('OPENAI_API_KEY', ''),
                    'base_url': 'https://api.openai.com/v1',
                    'timeout': 120
                },
                'environment': {
                    'type': 'local',
                    'work_dir': './agent_workspace',
                    'timeout': 300,
                    'safe_mode': True
                },
                'task': {
                    'max_iterations': 5,
                    'output_format': 'json_with_script',
                    'interactive_analysis': True,
                    'enable_testing': False
                },
                'tools': {
                    'bash': {
                        'enabled': True,
                        'timeout': 60,
                        'safe_commands_only': True
                    },
                    'python': {
                        'enabled': True,
                        'version': '3.8+',
                        'virtual_env': True
                    },
                    'file_operations': {
                        'enabled': True,
                        'read_only': False,
                        'max_file_size': '10MB'
                    }
                },
                'data': {
                    'data_root_dir': './benchmark_data',
                    'source_root_dir': './source_repos',
                    'sampling': {
                        'enabled': False,
                        'sample_size': 100,
                        'random_seed': 42
                    }
                },
                'output': {
                    'output_dir': './output',
                    'verbose_logging': True,
                    'save_trajectory': True,
                    'save_intermediate': False
                },
                'processing': {
                    'max_workers': 1,
                    'max_retries': 3,
                    'retry_delay': 10,
                    'skip_existing': True
                },
                'security': {
                    'forbidden_commands': ['rm -rf', 'sudo', 'chmod 777', 'wget', 'curl'],
                    'allowed_extensions': ['.py', '.txt', '.md', '.yaml', '.json', '.sh'],
                    'max_file_size': '50MB'
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'file': './logs/agent_analysis.log'
                }
            }
        else:
            return {}
    
    def get_config(self, config_type: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration (backward compatibility method)"""
        if config_type is None:
            config_type = 'agent'  # Default to agent configuration
        return self.load_config(config_type)
    
    def save_config(self, config: Dict[str, Any], config_type: str) -> bool:
        """Save configuration to file"""
        try:
            config_file = self.config_dir / f"{config_type}_config.yaml"
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            # Update cache
            self._cached_configs[config_type] = config.copy()
            
            logger.info(f"Configuration saved: {config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def clear_cache(self):
        """Clear configuration cache"""
        self._cached_configs.clear()
        logger.info("Configuration cache cleared")

# Global configuration loader instance
config_loader = ConfigLoader()