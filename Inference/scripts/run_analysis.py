#!/usr/bin/env python3
"""
Environment Configuration Analysis Main Program

This is the core analysis engine for the EnConda-Bench inference system.
It supports two analysis modes:
- LLM Mode: Uses large language models for environment configuration analysis
- Agent Mode: Uses intelligent agents for interactive analysis and problem solving

Usage:
    python run_analysis.py --mode llm --data-dir ./data --output-dir ./results
    python run_analysis.py --mode agent --agent-type real --data-dir ./data --output-dir ./results
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.processors.environment_processor import (
    LLMEnvironmentConfigProcessor, 
    AgentEnvironmentConfigProcessor
)
from utils.config_loader import config_loader

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Setup logging configuration"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )

def main():
    parser = argparse.ArgumentParser(description="Environment Configuration Analysis Tool")
    
    # Basic parameters
    parser.add_argument("--mode", choices=["llm", "agent"], default="llm",
                       help="Analysis mode: llm (Large Language Model) or agent (Intelligent Agent)")
    
    parser.add_argument("--agent-type", choices=["simple", "real"], default="simple",
                       help="Agent type (only effective in agent mode)")
    
    # Data path parameters
    parser.add_argument("--data-dir", type=str,
                       help="Data root directory path (containing error_gen_<repo_name> folders)")
    
    parser.add_argument("--source-dir", type=str,
                       help="Source code root directory path (containing archives and jsonl files)")
    
    parser.add_argument("--output-dir", type=str,
                       help="Output directory path")
    
    # Processing parameters
    parser.add_argument("--sample-size", type=int,
                       help="Sample size (if not specified, process all data)")
    
    parser.add_argument("--random-seed", type=int, default=42,
                       help="Random seed (default: 42)")
    
    # Configuration parameters
    parser.add_argument("--config", type=str,
                       help="Configuration file path (optional)")
    
    # Logging parameters
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Log level")
    
    parser.add_argument("--log-file", type=str,
                       help="Log file path (optional)")
    
    # Other parameters
    parser.add_argument("--dry-run", action="store_true",
                       help="Dry run mode, only show configuration without executing analysis")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = config_loader.load_config(args.mode)
        
        # Command line arguments override configuration file
        if args.data_dir:
            if args.mode == "llm":
                config['data']['data_root_dir'] = args.data_dir
            else:
                config['data']['data_root_dir'] = args.data_dir
                
        if args.source_dir:
            if args.mode == "llm":
                config['data']['source_root_dir'] = args.source_dir
            else:
                config['data']['source_root_dir'] = args.source_dir
                
        if args.output_dir:
            if args.mode == "llm":
                config['output']['output_dir'] = args.output_dir
            else:
                config['output']['output_dir'] = args.output_dir
        
        # Get final configuration values
        if args.mode == "llm":
            data_root_dir = config['data']['data_root_dir']
            source_root_dir = config['data']['source_root_dir']
            output_dir = config['output']['output_dir']
        else:
            data_root_dir = config['data']['data_root_dir']
            source_root_dir = config['data']['source_root_dir']
            output_dir = config['output']['output_dir']
        
        sample_size = args.sample_size
        random_seed = args.random_seed
        
        # Display configuration information
        logger.info("=" * 60)
        logger.info("Environment Configuration Analysis Tool")
        logger.info("=" * 60)
        logger.info(f"Analysis mode: {args.mode.upper()}")
        if args.mode == "agent":
            logger.info(f"Agent type: {args.agent_type}")
        logger.info(f"Data directory: {data_root_dir}")
        logger.info(f"Source directory: {source_root_dir}")
        logger.info(f"Output directory: {output_dir}")
        if sample_size:
            logger.info(f"Sample size: {sample_size}")
        logger.info(f"Random seed: {random_seed}")
        logger.info("=" * 60)
        
        if args.dry_run:
            logger.info("Dry run mode, not executing actual analysis")
            return
        
        # Create processor
        if args.mode == "llm":
            processor = LLMEnvironmentConfigProcessor(
                data_root_dir=data_root_dir,
                source_root_dir=source_root_dir,
                output_dir=output_dir
            )
        else:  # agent mode
            processor = AgentEnvironmentConfigProcessor(
                data_root_dir=data_root_dir,
                source_root_dir=source_root_dir,
                output_dir=output_dir,
                agent_type=args.agent_type
            )
        
        # Execute batch processing
        logger.info("Starting analysis task execution...")
        records = processor.process_batch(sample_size=sample_size, random_seed=random_seed)
        
        # Display result statistics
        successful_count = sum(1 for r in records if r.success)
        failed_count = len(records) - successful_count
        
        logger.info("=" * 60)
        logger.info("Analysis completed!")
        logger.info(f"Total processed: {len(records)}")
        logger.info(f"Successfully processed: {successful_count}")
        logger.info(f"Failed to process: {failed_count}")
        if len(records) > 0:
            logger.info(f"Success rate: {successful_count/len(records)*100:.2f}%")
        logger.info(f"Results saved in: {output_dir}")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("User interrupted program execution")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Program execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()