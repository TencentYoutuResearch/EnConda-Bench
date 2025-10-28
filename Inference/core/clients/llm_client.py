"""
Large Language Model Client Module

This module provides the LLMClient class for interacting with OpenAI's API to perform
environment configuration analysis. It handles prompt creation, API communication,
and response parsing for README file analysis.

Key Features:
- Dynamic configuration loading to avoid circular imports
- Comprehensive prompt engineering for error detection
- Structured response parsing (JSON + Bash script extraction)
- Error handling and logging for robust operation
- Support for multiple error types (E1-E8) with detailed analysis

The client generates detailed prompts that instruct the LLM to:
1. Analyze README files for environment setup errors
2. Provide structured JSON error reports
3. Generate corrective shell scripts
4. Handle various Python environment patterns (pip, conda, poetry)
"""

import json
import logging
from typing import Dict, Any, Optional
import openai
from ..models.data_models import AnalysisResult, ErrorInfo

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        # Dynamically load configuration to avoid circular imports
        from ...utils.config_loader import config_loader
        config_data = config_loader.load_config('llm')
        
        openai_config = config_data.get('openai', {})
        self.api_key = openai_config.get('api_key', '')
        self.base_url = openai_config.get('base_url', 'https://api.openai.com/v1')
        self.model_name = openai_config.get('model_name', 'gpt-4')
        self.max_tokens = openai_config.get('max_tokens', 4000)
        self.temperature = openai_config.get('temperature', 0.1)
        
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
    def create_analysis_prompt(self, readme_content: str, file_structure: str, error_types: Dict[str, Any]) -> str:
        """Create analysis prompt"""
        
        prompt = f"""You are an expert Python environment setup assistant. Your task is to analyze README files, detect potential errors in environment setup instructions, and provide comprehensive solutions.

Given a README file, you should:

1. **Error Detection and Analysis**: Carefully analyze the README for potential errors in environment setup instructions, including:
   - E1: Dependency Installation Error (missing dependencies, unnecessary dependencies, or version errors)
   - E2: Command Usage or Syntax Error (incorrect commands, invalid parameters, or improper syntax)
   - E4: File Path or Missing File Error (incorrect dependency file paths or referenced files that do not exist)
   - E6: Logical Order Error (incorrect execution order of installation steps)
   - E7: Version Compatibility Error (unspecified Python or dependency versions, version conflicts, or incompatibilities)
   - E8: Other Miscellaneous Errors (messy formatting, missing critical explanations, or unclear descriptions)

2. **Error Analysis Output**: First, output a JSON object containing your error analysis with the following structure:
```json
{{
  "detected_errors": [
    {{
      "error_type": "E1|E2|E4|E6|E7|E8",
      "error_description": "Detailed description of the error found",
      "fix_suggestion": "Specific suggestion on how to fix this error"
    }}
  ]
}}
```

3. **Environment Setup Script**: After the error analysis, create a comprehensive shell script that:
   - Fixes all detected errors
   - Sets up the environment correctly
   - Handles common Python environment setup patterns (pip, conda, poetry, etc.)
   - Includes error handling and verification steps

Your response should contain:
1. The JSON error analysis (wrapped in ```json code blocks)
2. The corrected shell script (wrapped in ```bash code blocks)

Technical requirements:
- Always start by examining the repository structure to locate dependency definitions
- Check for Python version requirements and use pyenv for version management
- Identify the dependency manager (pip, Poetry, etc.) and use appropriately
- Handle system-level dependencies with apt-get
- Ensure proper virtual environment setup
- Include verification steps to confirm successful installation
- Use non-interactive commands (e.g., `apt-get install -y`)
- Install from local repository, not PyPI packages

## Repository Structure:
{file_structure}

## README Content:
{readme_content}

Please analyze the above README file and provide your response in the specified format."""
        return prompt
    
    def analyze_readme(self, readme_content: str, file_structure: str, error_types: Dict[str, Any]) -> Optional[AnalysisResult]:
        """Call LLM to analyze README"""
        try:
            prompt = self.create_analysis_prompt(readme_content, file_structure, error_types)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a professional environment configuration expert, skilled at analyzing configuration issues in README documents and providing solutions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            raw_output = response.choices[0].message.content
            if raw_output is None:
                logger.error("LLM returned empty response")
                return None
                
            logger.info("Successfully obtained LLM response")
            
            # Parse response
            return self.parse_llm_response(raw_output)
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return None
    
    def parse_llm_response(self, raw_output: str) -> Optional[AnalysisResult]:
        """Parse LLM response"""
        try:
            # Extract JSON part (error analysis)
            json_start = raw_output.find('```json')
            json_end = raw_output.find('```', json_start + 7)
            
            # Extract bash script part
            bash_start = raw_output.find('```bash')
            bash_end = raw_output.find('```', bash_start + 7)
            
            if json_start == -1 or json_end == -1:
                logger.error("JSON format error analysis not found")
                return None
            
            # Parse JSON error analysis
            json_content = raw_output[json_start + 7:json_end].strip()
            data = json.loads(json_content)
            
            # Extract shell script
            shell_script = ""
            if bash_start != -1 and bash_end != -1:
                shell_script = raw_output[bash_start + 7:bash_end].strip()
            else:
                logger.warning("Bash script not found, attempting to extract from response")
                # If no bash code block found, try to generate basic script
                shell_script = "#!/bin/bash\n\n# Environment setup script\necho 'Setting up environment...'\n\necho 'Environment setup completed.'"
            
            # Build ErrorInfo objects
            errors = []
            detected_errors = data.get('detected_errors', [])
            for error_data in detected_errors:
                error_info = ErrorInfo(
                    error_type=error_data['error_type'],
                    error_description=error_data['error_description'],
                    fix_answer=error_data['fix_suggestion']
                )
                errors.append(error_info)
            
            result = AnalysisResult(
                repo_name="",  # Will be set at call site
                readme_name="",  # Will be set at call site
                errors=errors,
                shell_script=shell_script,
                raw_output=raw_output
            )
            
            logger.info(f"Successfully parsed LLM response, found {len(errors)} errors")
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.error(f"Raw response: {raw_output}")
            return None