"""
Real Agent Client Module

This module provides a real agent framework implementation that interfaces with
actual agent systems through command-line interfaces. It enables advanced
environment configuration analysis using intelligent agents that can execute
commands, test installations, and provide interactive analysis.

Usage:
    client = RealAgentClient()
    result = client.analyze_readme(readme_content, file_structure, error_types)
    
    # Or with custom configuration
    config = {"model_name": "gpt-4", "max_iterations": 10}
    client = RealAgentClient(config=config)
    result = client.analyze_readme(readme_content, file_structure, error_types)
"""

import json
import logging
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional
from pathlib import Path
from ..models.data_models import AnalysisResult, ErrorInfo
from ...utils.config_loader import config_loader

logger = logging.getLogger(__name__)

class RealAgentFramework:
    """Real agent framework implementation (via command-line interface)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agent_path = Path("./agent")
        self.configure(self.config)
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure agent parameters"""
        # Merge user configuration with default configuration
        agent_config = config_loader.get_config()
        agent_config.update(config)
        
        # Basic configuration
        self.model_name = agent_config.get('model_name', 'gpt-4')
        self.max_tokens = agent_config.get('max_tokens', 4000)
        self.temperature = agent_config.get('temperature', 0.1)
        self.base_url = agent_config.get('base_url', 'https://api.openai.com/v1')
        self.api_key = agent_config.get('api_key', '')
        
        # Environment configuration
        env_config = agent_config.get('environment', {})
        self.environment_setup = env_config.get('type', 'local')
        self.timeout_seconds = env_config.get('timeout', 300)
        self.work_dir = env_config.get('work_dir', './agent_workspace')
        
        # Task configuration
        task_config = agent_config.get('task', {})
        self.max_iterations = agent_config.get('max_iterations', 5)
        self.output_format = task_config.get('output_format', 'json_with_script')
        
        # Tools configuration
        self.tools_config = agent_config.get('tools', {})
        
        # Security configuration
        self.security_config = agent_config.get('security', {})
        
        logger.info(f"Real agent configuration completed: model={self.model_name}, env={self.environment_setup}")
    
    def execute_task(self, task_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task via command line"""
        try:
            logger.info("Starting real agent task execution")
            
            # Create temporary working directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Create task file
                task_file = temp_path / "task.md"
                task_file.write_text(self._create_task_content(task_description, context))
                
                # Create configuration file
                config_file = temp_path / "config.yaml"
                config_file.write_text(self._create_config_content())
                
                # Execute real agent via command line
                result = self._execute_real_agent(task_file, config_file, temp_path)
                
                logger.info("Real agent task execution completed")
                return result
                
        except Exception as e:
            logger.error(f"Real agent task execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'raw_output': '',
                'detected_errors': [],
                'shell_script': ''
            }
    
    def _create_task_content(self, task_description: str, context: Dict[str, Any]) -> str:
        """Create agent task content"""
        readme_content = context.get('readme_content', '')
        file_structure = context.get('file_structure', '')
        
        task_content = f"""# Environment Configuration Analysis Task

## Task Description
{task_description}

## Repository Structure
```
{file_structure}
```

## README Content
```markdown
{readme_content}
```

## Instructions
1. Analyze the README file for environment setup errors
2. Test the installation commands if possible
3. Generate a corrected setup script
4. Provide detailed error analysis in JSON format
"""
        return task_content
    
    def _create_config_content(self) -> str:
        """Create agent configuration content"""
        config_content = f"""# Agent Configuration for Environment Analysis

model_name: {self.model_name}
max_tokens: {self.max_tokens}
temperature: {self.temperature}
max_iterations: {self.max_iterations}

# Environment setup
environment:
  type: {self.environment_setup}
  timeout: {self.timeout_seconds}

# Tools configuration
tools:
  - name: bash
    enabled: true
  - name: python
    enabled: true
  - name: file_operations
    enabled: true

# Task-specific settings
task_type: environment_analysis
output_format: json_with_script
"""
        return config_content
    
    def _execute_real_agent(self, task_file: Path, config_file: Path, work_dir: Path) -> Dict[str, Any]:
        """Execute real agent via command line interface"""
        try:
            # Prepare agent command
            agent_cmd = self._build_agent_command(task_file, config_file, work_dir)
            
            logger.info(f"Executing agent command: {' '.join(agent_cmd)}")
            
            # Execute agent with timeout
            result = subprocess.run(
                agent_cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                env=self._prepare_environment()
            )
            
            # Parse agent output
            if result.returncode == 0:
                return self._parse_agent_output(result.stdout, result.stderr, work_dir)
            else:
                logger.error(f"Agent execution failed with return code {result.returncode}")
                logger.error(f"Agent stderr: {result.stderr}")
                return {
                    'success': False,
                    'error': f"Agent execution failed: {result.stderr}",
                    'raw_output': result.stdout,
                    'detected_errors': [],
                    'shell_script': '',
                    'return_code': result.returncode
                }
                
        except subprocess.TimeoutExpired:
            logger.error(f"Agent execution timed out after {self.timeout_seconds} seconds")
            return {
                'success': False,
                'error': f"Agent execution timed out after {self.timeout_seconds} seconds",
                'raw_output': '',
                'detected_errors': [],
                'shell_script': ''
            }
        except FileNotFoundError:
            logger.error("Agent executable not found. Please ensure the agent is installed and accessible.")
            return {
                'success': False,
                'error': "Agent executable not found",
                'raw_output': '',
                'detected_errors': [],
                'shell_script': ''
            }
        except Exception as e:
            logger.error(f"Unexpected error during agent execution: {e}")
            return {
                'success': False,
                'error': str(e),
                'raw_output': '',
                'detected_errors': [],
                'shell_script': ''
            }
    
    def _build_agent_command(self, task_file: Path, config_file: Path, work_dir: Path) -> list:
        """Build agent command line arguments"""
        # Use SWE-agent wrapper script
        agent_script = Path(__file__).parent.parent.parent / "agent" / "swe_agent_wrapper.py"
        
        cmd = [
            "python", str(agent_script),
            "--task-file", str(task_file),
            "--config-file", str(config_file),
            "--work-dir", str(work_dir)
        ]
            
        return cmd
    
    def _prepare_environment(self) -> Dict[str, str]:
        """Prepare environment variables for agent execution"""
        env = os.environ.copy()
        
        # Add API key if available
        if self.api_key:
            env['OPENAI_API_KEY'] = self.api_key
            env['API_KEY'] = self.api_key
        
        # Add base URL if specified
        if self.base_url:
            env['OPENAI_BASE_URL'] = self.base_url
            env['API_BASE_URL'] = self.base_url
            
        # Add work directory
        env['AGENT_WORK_DIR'] = str(self.work_dir)
        
        return env
    
    def _parse_agent_output(self, stdout: str, stderr: str, work_dir: Path) -> Dict[str, Any]:
        """Parse agent output and extract results"""
        try:
            # Look for JSON output in stdout
            json_start = stdout.find('{')
            json_end = stdout.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_output = stdout[json_start:json_end]
                result_data = json.loads(json_output)
                
                # Extract required fields
                detected_errors = result_data.get('detected_errors', [])
                shell_script = result_data.get('shell_script', '')
                raw_output = result_data.get('analysis_report', stdout)
                token_usage = result_data.get('token_usage', {})
                
                return {
                    'success': True,
                    'raw_output': raw_output,
                    'detected_errors': detected_errors,
                    'shell_script': shell_script,
                    'work_directory': str(work_dir),
                    'execution_method': 'real_agent',
                    'token_usage': token_usage,
                    'stderr': stderr
                }
            else:
                # Fallback: try to extract information from text output
                return self._parse_text_output(stdout, stderr, work_dir)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON output: {e}")
            return self._parse_text_output(stdout, stderr, work_dir)
        except Exception as e:
            logger.error(f"Error parsing agent output: {e}")
            return {
                'success': False,
                'error': f"Failed to parse agent output: {e}",
                'raw_output': stdout,
                'detected_errors': [],
                'shell_script': '',
                'stderr': stderr
            }
    
    def _parse_text_output(self, stdout: str, stderr: str, work_dir: Path) -> Dict[str, Any]:
        """Fallback method to parse text-based agent output"""
        # Try to extract shell script from output
        shell_script = ""
        script_start = stdout.find("#!/bin/bash")
        if script_start != -1:
            # Find the end of the script (usually marked by a separator or end of output)
            script_lines = []
            lines = stdout[script_start:].split('\n')
            for line in lines:
                if line.strip() and not line.startswith('---') and not line.startswith('==='):
                    script_lines.append(line)
                elif script_lines and (line.startswith('---') or line.startswith('===')):
                    break
            shell_script = '\n'.join(script_lines)
        
        # Try to extract errors (this is a simple heuristic)
        detected_errors = []
        error_patterns = ['ERROR:', 'Error:', 'ISSUE:', 'Issue:', 'PROBLEM:', 'Problem:']
        for line in stdout.split('\n'):
            for pattern in error_patterns:
                if pattern in line:
                    detected_errors.append({
                        'error_type': 'E8',
                        'error_description': line.strip(),
                        'fix_suggestion': 'Please review the agent output for specific recommendations'
                    })
        
        return {
            'success': True,
            'raw_output': stdout,
            'detected_errors': detected_errors,
            'shell_script': shell_script,
            'work_directory': str(work_dir),
            'execution_method': 'real_agent_text_parsed',
            'token_usage': {},
            'stderr': stderr
        }
    


class RealAgentClient:
    """Real agent client (using command-line interface)"""
    
    def __init__(self, agent_framework=None, config: Dict[str, Any] = None):
        """Initialize real agent client"""
        self.config = config or {}
        
        if agent_framework is None:
            self.agent_framework = RealAgentFramework(self.config)
        else:
            self.agent_framework = agent_framework
            self.agent_framework.configure(self.config)
        
        logger.info("Real agent client initialization completed")
    
    def create_analysis_prompt(self, readme_content: str, file_structure: str, error_types: Dict) -> str:
        """Create analysis task description (compatible with original interface)"""
        task_description = f"""Analyze the following README file for environment setup errors and provide solutions.

You are an Agent with the ability to:
1. Execute commands to test installation procedures
2. Analyze file structures and dependencies
3. Generate working setup scripts
4. Provide detailed error analysis

Focus on detecting these error types:
- E1: Dependency Installation Error
- E2: Command Usage or Syntax Error  
- E4: File Path or Missing File Error
- E6: Logical Order Error
- E7: Version Compatibility Error
- E8: Other Miscellaneous Errors

Repository Structure:
{file_structure}

README Content:
{readme_content}

Please provide:
1. JSON analysis of detected errors
2. A working shell script for environment setup

**CRITICAL REQUIREMENT**: The environment setup script MUST end with a test command that validates the environment setup. The script should only exit successfully after the test passes. Examples of test commands:
- `python -c "import main_module; print('Environment test passed!')"`
- `python -m pytest tests/ --tb=short`
- `python setup.py test`
- `python -c "import sys; print(f'Python {{sys.version}} environment ready')"`
- `python -c "exec(open('test_script.py').read())"`

The test command should verify that the environment is working correctly and all dependencies are properly installed.
"""
        return task_description
    
    def analyze_readme(self, readme_content: str, file_structure: str, error_types: Dict) -> Optional[AnalysisResult]:
        """Analyze README using real agent"""
        try:
            task_description = self.create_analysis_prompt(readme_content, file_structure, error_types)
            
            context = {
                'readme_content': readme_content,
                'file_structure': file_structure,
                'error_types': error_types
            }
            
            result = self.agent_framework.execute_task(task_description, context)
            
            if not result.get('success', False):
                logger.error(f"Real agent execution failed: {result.get('error', 'Unknown error')}")
                return None
            
            return self.parse_agent_response(result)
            
        except Exception as e:
            logger.error(f"Real agent analysis failed: {e}")
            return None
    
    def parse_agent_response(self, agent_result: Dict[str, Any]) -> Optional[AnalysisResult]:
        """Parse real agent response"""
        try:
            raw_output = agent_result.get('raw_output', '')
            detected_errors = agent_result.get('detected_errors', [])
            shell_script = agent_result.get('shell_script', '')
            
            # Build ErrorInfo objects
            errors = []
            for error_data in detected_errors:
                error_info = ErrorInfo(
                    error_type=error_data.get('error_type', 'E8'),
                    error_description=error_data.get('error_description', ''),
                    fix_answer=error_data.get('fix_suggestion', '')
                )
                errors.append(error_info)
            
            result = AnalysisResult(
                repo_name="",  # Will be set at call site
                readme_name="",  # Will be set at call site
                errors=errors,
                shell_script=shell_script,
                raw_output=raw_output
            )
            
            logger.info(f"Successfully parsed real agent response, found {len(errors)} errors")
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse real agent response: {e}")
            return None