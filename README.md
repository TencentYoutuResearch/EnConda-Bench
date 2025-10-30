# EnConda-Bench: Process-Level Trajectory Evaluation for Environment Configuration in Software Engineering Agents

A comprehensive benchmark framework for evaluating AI agents' performance on Python environment configuration tasks.

## 🌟 Project Overview

EnConda-Bench is an end-to-end environment configuration benchmark system specifically designed to evaluate the capabilities of large language models and AI agents in identifying, analyzing, and fixing Python environment configuration errors. The system provides a complete dataset, inference tools, and evaluation framework.

## 📁 Project Structure

```
EnConda-Bench/
├── Benchmark_Data/           # Benchmark Dataset
│   ├── error_types.json         # Error type definitions
│   ├── Enconda_benchmark_data.jsonl  # Main benchmark data
│   └── final_output_benchmark_data_final/  # Processed dataset
├── Inference/                # Inference System
│   ├── core/                     # Core inference modules
│   ├── configs/                  # Configuration files
│   ├── scripts/                  # Run scripts
│   └── docs/                     # Documentation
├── Evaluation/               # Evaluation System
│   ├── Evaluate/                 # Automated metric evaluation
│   └── Execution/                # End-to-end execution testing
└── Dockerfiles/              # Docker configuration files
```

## 🎯 Core Features

### 1. Dataset (Benchmark_Data)

- **Error Type Definitions**: 6 major environment configuration error types (E1-E8)
- **Real-world Data**: Based on real GitHub repository README files
- **Standardized Format**: Structured JSON/JSONL data format
- **Original Data Source**: Raw repositories available from [HuggingFace Dataset](https://huggingface.co/datasets/JetBrains-Research/EnvBench/tree/main/repos/final/python)

#### Supported Error Types

| Type | Name | Description |
|------|------|-------------|
| E1 | Dependency Installation Error | Missing dependencies, version errors, etc. |
| E2 | Command Usage or Syntax Error | Incorrect commands, parameters, or syntax |
| E4 | File Path or Missing File Error | Path errors or non-existent files |
| E6 | Logical Order Error | Incorrect installation step sequence |
| E7 | Version Compatibility Error | Version conflicts or incompatibilities |
| E8 | Other Miscellaneous Errors | Formatting issues, unclear descriptions, etc. |

### 2. Inference System (Inference)

Agent inference system supporting two modes:

- **LLM Mode**: Direct analysis based on large language models
- **Agent Mode**: Interactive analysis based on intelligent agents

#### Key Features
- 🔍 Automatic error detection and classification
- 🛠️ Fix script generation
- 📊 Batch processing and analysis
- 📈 Detailed statistical reports

### 3. Evaluation System (Evaluation)

Dual evaluation framework:

#### Automated Metric Evaluation (Evaluate)
- **Error Type Accuracy**: Precision, recall, F1-score
- **Text Similarity**: LLM-based semantic similarity evaluation
- **Intelligent Matching**: Handles inconsistencies between predictions and ground truth

#### End-to-End Execution Testing (Execution)
- **Docker Containers**: Isolated execution environment
- **Script Validation**: Actual execution of generated configuration scripts
- **Success Rate Statistics**: Environment configuration success rate analysis
- **Error Diagnosis**: Detailed execution logs and error analysis

## 🚀 Quick Start

### Requirements

- Python 3.10+
- Docker Engine
- 8GB+ RAM (recommended)
- OpenAI API key (for LLM evaluation)

### Installation

```bash
# Clone the project
git clone <repository-url>
cd EnConda-Bench

# Install Python dependencies
pip install -r requirements.txt

# Or use uv (recommended)
uv sync
```

### Docker Environment Setup

```bash
# Pull pre-built images
docker pull ghcr.io/research-org/envbench-python:latest

# Or build local images
docker build -f Dockerfiles/python.Dockerfile -t envbench-python .
```

### Configuration

1. **Create environment variables file**:
```bash
cp .env.example .env
# Edit .env file and add your OpenAI API key
```

2. **Configure inference parameters** (`Inference/configs/llm_config.yaml`):
```yaml
openai:
  api_key: "your-openai-api-key"
  model_name: "gpt-4"
  base_url: "https://api.openai.com/v1"
```

## 📖 Usage Guide

### 1. Run Inference Analysis

```bash
cd Inference

# LLM mode
python run.py --mode llm --config configs/llm_config.yaml

# Agent mode  
python run.py --mode agent --config configs/agent_config.yaml
```

### 2. Evaluate Results

#### Automated Metric Evaluation
```bash
cd Evaluation/Evaluate

python run_evaluation.py \
    --results_dir /path/to/inference/results \
    --data_root_dir /path/to/Benchmark_Data \
    --output_dir evaluation_output
```

#### End-to-End Execution Testing
```bash
cd Evaluation/Execution

# Convert data format
python convert_to_jsonl.py \
    --input_file inference_results.jsonl \
    --output_file execution_input.jsonl

# Run execution tests
./uv_run.sh
```

### 3. View Results

After evaluation completion, results will be saved in the specified output directory:

- `detailed_evaluation_results.json`: Detailed evaluation results
- `evaluation_summary.json`: Summary statistics
- `results.jsonl`: Execution test results

## 📊 Evaluation Metrics

### Automated Metrics
- **Error Type Recognition**: Precision, recall, F1-score
- **Description Accuracy**: Semantic similarity of error descriptions
- **Fix Solution Quality**: Semantic similarity of fix solutions

### Execution Metrics
- **Environment Configuration Success Rate**: Proportion of successful script executions
- **Clean Pass Rate**: Proportion of environment configurations with no issues
- **Error Diagnosis**: Specific failure cause analysis

## 🔧 Customization and Extension

### Adding New Error Types

1. Update `Benchmark_Data/error_types.json`
2. Add corresponding detection logic in the inference system
3. Update evaluation metric calculations

### Supporting New Programming Languages

1. Create new Dockerfile (`Dockerfiles/new_language.Dockerfile`)
2. Add language-specific configuration files
3. Extend inference and evaluation logic

### Integrating New LLM Models

1. Add new client in `Inference/core/clients/`
2. Update configuration file format
3. Test compatibility

## 📈 Performance Optimization

### Inference Optimization
- Use batch processing to reduce API calls
- Enable result caching
- Parallel processing of multiple files

### Evaluation Optimization
- Adjust Docker resource limits
- Use SSD storage for improved I/O performance
- Set reasonable concurrent worker counts

## 📄 License

This project is licensed under an open source license. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the EnvBench project for providing the foundational framework
- Thanks to all contributors for their efforts
- Thanks to the open source community for their support

## 📚 Citation
If you find this work useful, please give us a ⭐️ and consider citing:
```bibtex
@article{EnConda_Bench,
      title={Process-Level Trajectory Evaluation for Environment Configuration in Software Engineering Agents}, 
      author={Kuang, Jiayi and Li, Yinghui and Zhang, Xin and Li, Yangning and Yin, Di and Sun, Xing and Shen, Ying and Yu, Philip S},
      journal={arXiv preprint arXiv:2510.25694},
      url={https://arxiv.org/abs/2510.25694},
      year={2025}
}
```