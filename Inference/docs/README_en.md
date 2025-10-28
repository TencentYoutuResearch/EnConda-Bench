# Environment Configuration Analysis Tool

A Python environment configuration error detection and repair tool based on Large Language Models (LLM) and Intelligent Agents.

## 🌟 Features

- **Dual Mode Support**: Supports both LLM (Large Language Model) and Agent (Intelligent Agent) analysis modes
- **Error Detection**: Automatically detects environment configuration errors in README files
- **Script Generation**: Generates corrected environment setup scripts
- **Batch Processing**: Supports large-scale dataset batch analysis
- **Detailed Reports**: Generates comprehensive analysis reports and statistics

## 📋 Supported Error Types

- **E1**: Dependency Installation Error (missing dependencies, version errors, etc.)
- **E2**: Command Usage or Syntax Error
- **E4**: File Path or Missing File Error
- **E6**: Logical Order Error
- **E7**: Version Compatibility Error
- **E8**: Other Miscellaneous Errors

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration Setup

1. **LLM Mode Configuration** (`configs/llm_config.yaml`):
```yaml
openai:
  api_key: "your-openai-api-key"
  model_name: "gpt-4"
  base_url: "https://api.openai.com/v1"
```

2. **Agent Mode Configuration** (`configs/agent_config.yaml`):
```yaml
agent:
  type: "simple"  # or "real"
  api_key: "your-api-key"
  model_name: "gpt-4"
```

### Run Analysis

#### Basic Usage

```bash
# Using LLM mode
python run.py --mode llm --data-dir ./data --output-dir ./output

# Using Agent mode
python run.py --mode agent --agent-type simple --data-dir ./data --output-dir ./output
```

#### Advanced Usage

```bash
# Sample analysis (process 100 samples)
python run.py --mode llm --sample-size 100 --data-dir ./data --output-dir ./output

# Specify log level and file
python run.py --mode agent --log-level DEBUG --log-file ./logs/analysis.log

# Dry run (show configuration only, no actual analysis)
python run.py --dry-run --mode llm --data-dir ./data
```

## 📁 Project Structure

```
EnConda-Bench/Inference/
├── core/                    # Core modules
│   ├── models/             # Data models
│   ├── processors/         # Processors
│   └── clients/            # Client implementations
├── configs/                # Configuration files
│   ├── llm_config.yaml    # LLM configuration
│   ├── agent_config.yaml  # Agent configuration
│   └── error_type.json    # Error type definitions
├── scripts/               # Script files
├── utils/                 # Utility modules
├── docs/                  # Documentation
├── run.py                 # Main run script
└── requirements.txt       # Dependencies
```

## 🔧 Configuration Guide

### LLM Mode Configuration

- `openai.api_key`: OpenAI API key
- `openai.model_name`: Model name to use
- `data.data_root_dir`: Data root directory
- `output.output_dir`: Output directory

### Agent Mode Configuration

- `agent.type`: Agent type (simple/real)
- `environment.type`: Environment type (local/docker)
- `task.max_iterations`: Maximum iterations
- `tools`: Tool configurations

## 📊 Output Description

### Generated Files

1. **Error Analysis JSON** (`results/<repo_name>/<readme_name>_errors.json`)
2. **Fix Script** (`results/<repo_name>/<readme_name>_setup.sh`)
3. **Processing Records** (`processing_records.jsonl`)
4. **Summary Report** (`summary_report.json`)

### Output Example

```json
{
  "repo_name": "example_repo",
  "readme_name": "readme_0",
  "errors": [
    {
      "error_type": "E1",
      "error_description": "Missing requirements.txt file",
      "fix_answer": "Create requirements.txt file and list required dependencies"
    }
  ]
}
```

## 🛠️ Development Guide

### Adding New Error Detection Rules

1. Define new error types in `configs/error_type.json`
2. Implement detection logic in corresponding clients
3. Update test cases

### Extending Agent Functionality

1. Inherit from `AgentFramework` protocol
2. Implement `execute_task` method
3. Register new Agent type in `AgentEnvironmentConfigProcessor`

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**: Check API key settings in configuration files
2. **Data Path Error**: Verify data directory path is correct
3. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Log Analysis

Enable verbose logging to diagnose issues:

```bash
python run.py --log-level DEBUG --log-file ./logs/debug.log
```

## 📈 Performance Optimization

- Use sampling feature for large datasets
- Adjust concurrent processing count
- Enable result caching

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or suggestions, please contact us through:

- Submit an Issue
- Send an email
- Join the discussion