"""
Environment Configuration Processor Module

This module provides the core processing engines for environment configuration analysis
in the EnConda-Bench inference system. It implements both LLM-based and Agent-based
analysis approaches with a unified interface.

Key Components:
- EnvironmentConfigProcessor: Abstract base class defining the processing interface
- LLMEnvironmentConfigProcessor: Implementation using Large Language Models
- AgentEnvironmentConfigProcessor: Implementation using intelligent agents

"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from ..models.data_models import AnalysisResult, ProcessingRecord
from ..clients.llm_client import LLMClient
from ..clients.agent_client import AgentClient
from .data_processor import DataProcessor
from .output_manager import OutputManager

logger = logging.getLogger(__name__)

class EnvironmentConfigProcessor:
    """Environment configuration processor base class"""
    
    def __init__(self, 
                 data_root_dir: str,
                 source_root_dir: str,
                 output_dir: str,
                 error_types_file: str = "./configs/error_type.json"):
        
        self.data_processor = DataProcessor(data_root_dir, source_root_dir)
        self.output_manager = OutputManager(output_dir)
        
        # Load error type definitions
        self.error_types = self._load_error_types(error_types_file)
        
        # Client will be initialized in subclasses
        self.client = None
        
    def _load_error_types(self, error_types_file: str) -> Dict:
        """Load error type definitions"""
        try:
            error_types_path = Path(error_types_file)
            if not error_types_path.exists():
                logger.warning(f"Error types file does not exist: {error_types_file}")
                return {}
                
            with open(error_types_path, 'r', encoding='utf-8') as f:
                error_types = json.load(f)
            
            logger.info(f"Successfully loaded error type definitions: {len(error_types)} types")
            return error_types
            
        except Exception as e:
            logger.error(f"Failed to load error type definitions: {e}")
            return {}
    
    def process_single_readme(self, folder_path: Path) -> Optional[ProcessingRecord]:
        """Process single README file"""
        try:
            # Process data
            repo_name, readme_content, file_structure, golden_answer = \
                self.data_processor.process_single_repo(folder_path)
            
            logger.info(f"Starting processing: {repo_name}")
            
            # Call client analysis
            if self.client is None:
                raise ValueError("Client not initialized")
                
            result = self.client.analyze_readme(readme_content, file_structure, self.error_types)
            
            if result is None:
                logger.error(f"Analysis failed: {repo_name}")
                return self._create_failed_record(repo_name, folder_path.name, "Analysis failed")
            
            # Set repo information in result
            result.repo_name = repo_name
            result.readme_name = folder_path.name
            
            # Save results
            errors_json_path, shell_script_path = self.output_manager.save_analysis_result(
                result, repo_name, folder_path.name
            )
            
            # Create processing record
            record = self.output_manager.create_processing_record(
                repo_name=repo_name,
                readme_name=folder_path.name,
                input_prompt=f"README analysis task: {repo_name}",
                model_output=result.raw_output,
                errors=result.errors,
                shell_script_path=shell_script_path,
                errors_json_path=errors_json_path,
                success=True,
                token_usage=getattr(result, 'token_usage', None)
            )
            
            # Save processing record
            self.output_manager.save_processing_record(record)
            
            logger.info(f"Processing completed: {repo_name}, found {len(result.errors)} errors")
            return record
            
        except Exception as e:
            logger.error(f"Failed to process README {folder_path}: {e}")
            return self._create_failed_record(
                folder_path.parent.name, 
                folder_path.name, 
                str(e)
            )
    
    def _create_failed_record(self, repo_name: str, readme_name: str, error_message: str) -> ProcessingRecord:
        """Create failed record"""
        return self.output_manager.create_processing_record(
            repo_name=repo_name,
            readme_name=readme_name,
            input_prompt="",
            model_output="",
            errors=[],
            shell_script_path="",
            errors_json_path="",
            success=False,
            error_message=error_message
        )
    
    def process_batch(self, 
                     sample_size: Optional[int] = None, 
                     random_seed: int = 42) -> List[ProcessingRecord]:
        """Batch process README files"""
        
        # Get all README folders
        folders = self.data_processor.get_all_readme_folders()
        
        if not folders:
            logger.warning("No README folders found")
            return []
        
        # Sampling processing
        if sample_size is not None:
            folders = self.data_processor.sample_readme_folders(folders, sample_size, random_seed)
        
        logger.info(f"Starting batch processing of {len(folders)} README files")
        
        records = []
        for i, folder_path in enumerate(folders, 1):
            logger.info(f"Processing progress: {i}/{len(folders)} - {folder_path.name}")
            
            record = self.process_single_readme(folder_path)
            if record:
                records.append(record)
        
        # Generate summary report
        self.output_manager.generate_summary_report()
        
        logger.info(f"Batch processing completed, processed {len(records)} files")
        return records

class LLMEnvironmentConfigProcessor(EnvironmentConfigProcessor):
    """LLM-based environment configuration processor"""
    
    def __init__(self, 
                 data_root_dir: str,
                 source_root_dir: str,
                 output_dir: str,
                 error_types_file: str = "./configs/error_type.json"):
        
        super().__init__(data_root_dir, source_root_dir, output_dir, error_types_file)
        self.client = LLMClient()
        logger.info("LLM environment configuration processor initialization completed")

class AgentEnvironmentConfigProcessor(EnvironmentConfigProcessor):
    """Agent-based environment configuration processor"""
    
    def __init__(self, 
                 data_root_dir: str,
                 source_root_dir: str,
                 output_dir: str,
                 agent_type: str = "simple",
                 error_types_file: str = "./configs/error_type.json"):
        
        super().__init__(data_root_dir, source_root_dir, output_dir, error_types_file)
        
        # Choose different implementations based on agent type
        if agent_type == "simple":
            from ..clients.agent_client import AgentClient, SimpleAgentFramework
            self.client = AgentClient(SimpleAgentFramework())
        elif agent_type == "real":
            from ..clients.agent_real_client import RealAgentClient
            self.client = RealAgentClient()
        else:
            # Default to simple implementation
            from ..clients.agent_client import AgentClient, SimpleAgentFramework
            self.client = AgentClient(SimpleAgentFramework())
            
        logger.info(f"Agent environment configuration processor initialization completed (type: {agent_type})")