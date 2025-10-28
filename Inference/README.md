# Environment Configuration Analysis Tool

[中文文档](docs/README_zh.md) | [English Documentation](docs/README_en.md)

A powerful Python environment configuration error detection and repair tool that supports both Large Language Model (LLM) and Intelligent Agent analysis modes.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit the configuration files in `configs/` directory:
- `llm_config.yaml` for LLM mode
- `agent_config.yaml` for Agent mode

### 3. Run Analysis
```bash
# Basic usage with LLM mode
python run.py --mode llm --data-dir ./data --output-dir ./output

# Basic usage with Agent mode  
python run.py --mode agent --data-dir ./data --output-dir ./output
```

## 📋 Features

- ✅ **Dual Analysis Modes**: LLM and Agent-based analysis
- ✅ **Error Detection**: Detects 6 types of environment setup errors (E1-E8)
- ✅ **Script Generation**: Generates corrected setup scripts
- ✅ **Batch Processing**: Handles large datasets efficiently
- ✅ **Detailed Reports**: Comprehensive analysis and statistics
- ✅ **Flexible Configuration**: YAML-based configuration system

## 🏗️ Project Structure

```
EnConda-Bench/Inference/
├── core/                    # Core modules
│   ├── models/             # Data models (ErrorInfo, AnalysisResult, etc.)
│   ├── processors/         # Processing logic (DataProcessor, OutputManager)
│   └── clients/            # Analysis clients (LLM, Agent)
├── configs/                # Configuration files
│   ├── llm_config.yaml    # LLM mode configuration
│   ├── agent_config.yaml  # Agent mode configuration
│   └── error_type.json    # Error type definitions
├── scripts/               # Execution scripts
├── utils/                 # Utility modules
├── docs/                  # Documentation
├── run.py                 # Main entry point
└── requirements.txt       # Dependencies
```

## 📊 Supported Error Types

| Type | Description | Examples |
|------|-------------|----------|
| **E1** | Dependency Installation Error | Missing requirements.txt, version conflicts |
| **E2** | Command Usage/Syntax Error | Incorrect bash commands, invalid parameters |
| **E4** | File Path/Missing File Error | Wrong paths, non-existent files |
| **E6** | Logical Order Error | Incorrect installation sequence |
| **E7** | Version Compatibility Error | Python version issues, compatibility problems |
| **E8** | Other Miscellaneous Errors | Formatting issues, unclear descriptions |

## 🔧 Configuration

### LLM Mode (`configs/llm_config.yaml`)
```yaml
openai:
  api_key: "your-openai-api-key"
  model_name: "gpt-4"
  base_url: "https://api.openai.com/v1"

data:
  data_root_dir: "./benchmark_data"
  source_root_dir: "./source_repos"

output:
  output_dir: "./output"
```

### Agent Mode (`configs/agent_config.yaml`)
```yaml
agent:
  type: "simple"  # or "real"
  model_name: "gpt-4"
  api_key: "your-api-key"

environment:
  type: "local"
  work_dir: "./agent_workspace"

task:
  max_iterations: 5
  interactive_analysis: true
```

## 📈 Usage Examples

### Basic Analysis
```bash
# Analyze with LLM mode
python run.py --mode llm --data-dir DATA_PATH --output-dir ./results

# Analyze with Agent mode
python run.py --mode agent --agent-type real --data-dir DATA_PATH --output-dir ./results
```

### Advanced Options
```bash
# Sample analysis (100 samples)
python run.py --mode llm --sample-size 100 --data-dir DATA_PATH --output-dir ./results

# Enable debug logging
python run.py --mode agent --log-level DEBUG --log-file ./logs/debug.log

# Dry run (configuration check only)
python run.py --dry-run --mode llm --data-dir DATA_PATH
```

## 📄 Output Files

The tool generates several types of output files:

1. **Error Analysis JSON**: `results/<repo_name>/<readme_name>_errors.json`
2. **Setup Scripts**: `results/<repo_name>/<readme_name>_setup.sh`
3. **Processing Records**: `processing_records.jsonl`
4. **Summary Report**: `summary_report.json`

### Example Output
```json
{
  "repo_name": "example_project",
  "readme_name": "readme_0",
  "errors": [
    {
      "error_type": "E1",
      "error_description": "Missing requirements.txt file",
      "fix_answer": "Create requirements.txt with necessary dependencies"
    }
  ]
}
```

## 🛠️ Development

### Extending Agent Capabilities
1. Inherit from `AgentFramework` protocol
2. Implement the `execute_task` method
3. Register in `AgentEnvironmentConfigProcessor`

## 🔍 Troubleshooting

### Common Issues
- **API Key Error**: Verify API keys in configuration files
- **Path Issues**: Ensure data directories exist and are accessible
- **Dependencies**: Run `pip install -r requirements.txt`

### Debug Mode
```bash
python run.py --log-level DEBUG --log-file ./debug.log
```

## 📚 Documentation

- [中文详细文档](docs/README_zh.md)
- [English Detailed Documentation](docs/README_en.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
