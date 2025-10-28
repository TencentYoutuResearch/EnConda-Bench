"""
Data Processing Module

This module handles all data processing operations for the EnConda-Bench inference
system. It manages the complex directory structure of benchmark data, extracts README
files, processes golden answers, and handles repository metadata.

The DataProcessor class serves as the central hub for all data-related operations,
providing a clean interface between the raw benchmark data and the analysis engines.
It handles various file formats and naming conventions used across different repositories.

Directory Structure Expected:
    data_root_dir/
    ├── error_gen_repo1/
    │   ├── README_1/
    │   │   ├── README.md
    │   │   └── README.json
    │   └── README_2/
    │       ├── README.md
    │       └── README.json
    └── error_gen_repo2/
        └── README_1/
            ├── README.md
            └── README.json
"""

import os
import json
import re
import random
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import tarfile
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_root_dir: str, source_root_dir: str):
        self.data_root_dir = Path(data_root_dir)
        self.source_root_dir = Path(source_root_dir)
        
    def get_all_readme_folders(self) -> List[Path]:
        """Get all folders containing README files (in subfolders of error_gen_<repo_name>)"""
        folders = []
        if not self.data_root_dir.exists():
            logger.error(f"Data root directory does not exist: {self.data_root_dir}")
            return folders
            
        # Traverse error_gen_<repo_name> folders
        for repo_item in self.data_root_dir.iterdir():
            if repo_item.is_dir() and repo_item.name.startswith('error_gen_'):
                # Traverse subfolders within repo folder
                for sub_item in repo_item.iterdir():
                    if sub_item.is_dir():
                        # Check if subfolder contains README file
                        has_readme = False
                        for ext in ['.md', '.rst', '.txt', '']:
                            readme_path = sub_item / f"README{ext}"
                            if readme_path.exists():
                                has_readme = True
                                break
                        
                        if has_readme:
                            folders.append(sub_item)
        
        logger.info(f"Found {len(folders)} subfolders containing README files")
        return folders
    
    def read_readme_content(self, folder_path: Path) -> Optional[str]:
        """Read README file content"""
        readme_files = []
        for ext in ['.md', '.rst', '.txt', '']:
            readme_path = folder_path / f"README{ext}"
            if readme_path.exists():
                readme_files.append(readme_path)
        
        if not readme_files:
            logger.warning(f"No README file found in {folder_path}")
            return None
            
        # Prioritize .md files
        readme_file = readme_files[0]
        for f in readme_files:
            if f.suffix == '.md':
                readme_file = f
                break
                
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Successfully read README file: {readme_file}")
            return content
        except Exception as e:
            logger.error(f"Failed to read README file {readme_file}: {e}")
            return None
    
    def read_golden_answer(self, folder_path: Path) -> Optional[Dict]:
        """Read golden answer JSON file"""
        json_path = folder_path / "README.json"
        if not json_path.exists():
            logger.warning(f"Golden answer file not found: {json_path}")
            return None
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Successfully read golden answer: {json_path}")
            return data
        except Exception as e:
            logger.error(f"Failed to read golden answer {json_path}: {e}")
            return None
    
    def extract_repo_name_from_folder(self, folder_name: str) -> str:
        """Extract repo name from folder name"""
        # error_gen_adamchainz_django -> adamchainz_django
        if folder_name.startswith('error_gen_'):
            return folder_name[10:]  # Remove 'error_gen_' prefix
        return folder_name
    
    def find_matching_repo_archive(self, repo_name: str) -> Optional[Path]:
        """Find matching repo archive"""
        # Convert adamchainz_django to possible archive names
        # Try multiple naming patterns
        possible_names = [
            f"{repo_name.replace('_', '__')}.tar.gz",
            f"{repo_name.replace('_', '-')}.tar.gz",
            f"{repo_name}.tar.gz",
        ]
        
        for name in possible_names:
            archive_path = self.source_root_dir / name
            if archive_path.exists():
                logger.info(f"Found matching archive: {archive_path}")
                return archive_path
                
        logger.warning(f"Archive not found for repo {repo_name}")
        return None
    
    def find_repo_directory_info(self, repo_name: str) -> Optional[Dict]:
        """Find repo directory information from jsonl files"""
        jsonl_files = list(self.source_root_dir.glob("*.jsonl"))
        
        for jsonl_file in jsonl_files:
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        data = json.loads(line.strip())
                        if 'repository' in data:
                            # Handle different naming formats
                            repo_in_jsonl = data['repository']
                            # bigmlcom/python -> bigmlcom_python
                            normalized_jsonl_name = repo_in_jsonl.replace('/', '_').replace('-', '_')
                            normalized_repo_name = repo_name.replace('-', '_')
                            
                            if normalized_jsonl_name == normalized_repo_name:
                                logger.info(f"Found matching directory info: {repo_in_jsonl}")
                                return data
            except Exception as e:
                logger.error(f"Failed to read jsonl file {jsonl_file}: {e}")
                continue
                
        logger.warning(f"Directory info not found for repo {repo_name}")
        return None
    
    def get_repo_file_structure(self, directory_info: Dict) -> str:
        """Generate file structure string from directory information"""
        if not directory_info:
            return "Unable to get file structure information"
            
        structure_lines = []
        structure_lines.append(f"Repository: {directory_info.get('repository', 'Unknown')}")
        
        if 'files' in directory_info:
            structure_lines.append("File structure:")
            for file_info in directory_info['files'][:50]:  # Limit number of files displayed
                file_path = file_info.get('path', '')
                file_type = file_info.get('type', 'file')
                structure_lines.append(f"  {file_type}: {file_path}")
                
        return '\n'.join(structure_lines)
    
    def process_single_repo(self, folder_path: Path) -> Tuple[str, str, str, Optional[Dict]]:
        """Process single repo, return repo name, README content, file structure and golden answer"""
        # Extract repo info from path
        # folder_path is subfolder, its parent folder is error_gen_<repo_name>
        parent_folder = folder_path.parent
        sub_folder_name = folder_path.name
        
        if parent_folder.name.startswith('error_gen_'):
            repo_name = self.extract_repo_name_from_folder(parent_folder.name)
        else:
            repo_name = parent_folder.name
        
        # Read README content
        readme_content = self.read_readme_content(folder_path)
        if not readme_content:
            raise ValueError(f"Unable to read README content: {folder_path}")
        
        # Read golden answer
        golden_answer = self.read_golden_answer(folder_path)
        
        # Get file structure information
        directory_info = self.find_repo_directory_info(repo_name)
        file_structure = self.get_repo_file_structure(directory_info)
        
        return f"{repo_name}_{sub_folder_name}", readme_content, file_structure, golden_answer
    
    def sample_readme_folders(self, folders: List[Path], sample_size: int, random_seed: int = 42) -> List[Path]:
        """Randomly sample README folders"""
        if len(folders) <= sample_size:
            logger.info(f"Total data {len(folders)} is less than or equal to sample size {sample_size}, returning all data")
            return folders
        
        # Set random seed to ensure reproducible results
        random.seed(random_seed)
        sampled_folders = random.sample(folders, sample_size)
        
        logger.info(f"Randomly sampled {len(sampled_folders)} folders from {len(folders)} folders")
        return sampled_folders