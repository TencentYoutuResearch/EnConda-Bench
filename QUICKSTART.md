# 🚀 Quick Start Guide

Welcome to EnConda-Bench! This guide will help you set up the project and run your first example in 5 minutes.

## ⚡ One-Click Installation

```bash
# Clone the project
git clone <repository-url>
cd EnConda-Bench

# Run automatic installation script
./install.sh
```

The installation script will automatically:
- ✅ Check Python and Docker environment
- ✅ Install all required dependencies
- ✅ Create configuration files
- ✅ Pull Docker images
- ✅ Verify installation results

## 🔑 Configure API Keys

Edit the `.env` file and add your OpenAI API key:

```bash
# Edit configuration file
nano .env

# Or use your preferred editor
code .env
```

Set in the `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 🎯 Run Your First Example

### 1. Inference Analysis Example

```bash
cd Inference

# Run with uv (recommended)
uv run python run.py --mode llm --data-dir ../Benchmark_Data --output-dir results

# Or use traditional method
source ../venv/bin/activate  # Linux/Mac
python run.py --mode llm --data-dir ../Benchmark_Data --output-dir results
```

### 2. View Inference Results

```bash
# Check generated results
ls results/
cat results/analysis_summary.json
```

### 3. Run Evaluation

```bash
cd ../Evaluation/Evaluate

# Evaluate inference results
python run_evaluation.py \
    --results_dir ../../Inference/results \
    --data_root_dir ../../Benchmark_Data \
    --output_dir evaluation_output

# View evaluation results
cat evaluation_output/evaluation_summary.json
```

## 📊 Example Output

### Inference Result Example
```json
{
  "repo_name": "example/repo",
  "readme_name": "README.md",
  "errors": [
    {
      "error_type": "E1",
      "error_description": "Missing required dependency 'numpy'",
      "fix_answer": "Add 'pip install numpy' to installation steps"
    }
  ],
  "shell_script": "#!/bin/bash\npip install numpy\npython setup.py install"
}
```

### Evaluation Result Example
```json
{
  "total_files": 50,
  "overall_metrics": {
    "error_type": {
      "precision": 0.85,
      "recall": 0.78,
      "f1_score": 0.81
    },
    "description_accuracy": 0.72,
    "fix_solution_accuracy": 0.68
  }
}
```

## 🐳 Docker Execution Testing (Optional)

If you want to test whether the generated scripts actually work:

```bash
cd Evaluation/Execution

# Convert inference results to execution format
python convert_to_jsonl.py \
    --input_file ../../Inference/results/results.jsonl \
    --output_file execution_input.jsonl

# Run Docker execution testing
./uv_run.sh
```

## 🔧 Custom Configuration

### Modify Inference Parameters

Edit `Inference/configs/llm_config.yaml`:

```yaml
openai:
  model_name: "gpt-4"  # or "gpt-3.5-turbo"
  temperature: 0.1
  max_tokens: 2000

processing:
  batch_size: 10
  max_workers: 4
```

### Modify Evaluation Parameters

Edit `Evaluation/Execution/conf/base.yaml`:

```yaml
inference_workers: 2  # Reduce concurrency
eval_workers: 2
evaluation:
  docker:
    container_timeout: 300  # Reduce timeout
```

## 📝 Process Your Own Data

### 1. Prepare Data Format

Create your data directory structure `my_data_folder/`:

```
my_data_folder/
├── error_gen_my_repo/
│   ├── README_1/
│   │   ├── README.md
│   │   └── README.json
│   └── README_2/
│       ├── README.md
│       └── README.json
└── error_gen_another_repo/
    └── README_1/
        ├── README.md
        └── README.json
```

Each README.json should contain:
```json
{
  "repo_name": "my/repo",
  "readme_content": "# My Project\n\nInstall dependencies:\n```bash\npip install pandas\n```"
}
```

### 2. Run Analysis

```bash
cd Inference
uv run python run.py --mode llm --data-dir my_data_folder --output-dir my_results
```

### 3. Evaluate Results (if you have ground truth)

Prepare ground truth format and run evaluation:

```bash
cd Evaluation/Evaluate
python run_evaluation.py --results_dir my_results --data_root_dir my_ground_truth
```

## 🐛 Common Issues

### Q: Installation script fails?
A: Check Python version (>=3.10) and network connection, or install manually following `DEPENDENCIES.md`

### Q: OpenAI API call fails?
A: Check if API key is correct, account has balance, and network can access OpenAI

### Q: Docker permission error?
A: Run `sudo usermod -aG docker $USER` and re-login

### Q: Out of memory?
A: Reduce `max_workers` parameter or increase system memory

### Q: Poor results?
A: Try stronger model (gpt-4), adjust prompts, or check input data quality

## 📚 Further Learning

- 📖 Complete documentation: `README.md` (English) or `README_zh.md` (Chinese)
- 🔧 Dependencies: `DEPENDENCIES.md`
- 🏗️ Inference system: `Inference/docs/README_zh.md`
- 📊 Evaluation system: `Evaluation/Evaluate/EVALUATION_README.md`
- 🐳 Execution testing: `Evaluation/Execution/README.md`

## 💡 Tips

1. **First run**: Recommend testing with small dataset first to ensure environment is configured correctly
2. **API costs**: Be aware of OpenAI API call costs, can test with gpt-3.5-turbo first
3. **Concurrency control**: Adjust worker count based on your hardware configuration
4. **Result analysis**: Use Jupyter notebook for deeper result analysis
5. **Issue reporting**: Check project Issues or contact development team when encountering problems

---

🎉 **Congratulations! You have successfully run your first example. Now you can start exploring more features!**