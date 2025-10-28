# Environment Configuration Analysis Result Evaluation System

This evaluation system is used to assess performance on environment configuration error analysis tasks.

## Features

- **Error Type Evaluation**: Calculate precision, recall, and F1 scores for error type identification
- **Text Similarity Evaluation**: Use LLM to evaluate semantic similarity of error descriptions and fix solutions
- **Intelligent Error Matching**: Handle inconsistencies in quantity and order between predicted errors and golden answers
- **Detailed Report Generation**: Generate detailed evaluation reports and summary statistics

## File Structure

```
├── evaluation_models.py          # Evaluation-related data models
├── text_similarity_evaluator.py  # Text similarity evaluator
├── error_matcher.py              # Error matcher
├── evaluation_engine.py          # Evaluation engine core logic
├── evaluator.py                  # Main evaluator
├── run_evaluation.py             # Command line execution script
├── evaluation_example.py         # Usage examples
├── test_evaluation.py            # Test script
└── EVALUATION_README.md          # This document
```

## Install Dependencies

The evaluation system uses the same dependencies as the main project:

```bash
pip install -r requirements.txt
```

Make sure you have a valid OpenAI API key set in your `.env` file.

## Usage

### Method 1: Command Line Usage

```bash
python run_evaluation.py \
    --results_dir /path/to/results \
    --data_root_dir /path/to/data_root \
    --output_dir evaluation_output
```

Parameter descriptions:
- `--results_dir`: Model output results directory (containing various subfolders and JSON files)
- `--data_root_dir`: Original data root directory (containing error_gen_* folders)
- `--output_dir`: Evaluation results output directory (optional, defaults to evaluation_output)

### Method 2: Create Python Script Usage

```python
from evaluator import Evaluator

# Create evaluator
evaluator = Evaluator(
    results_dir="results",
    data_root_dir="/path/to/data_root",
    output_dir="evaluation_output"
)

# Run evaluation
overall_result = evaluator.run_evaluation()

# View results
print(f"Overall F1 Score: {overall_result.overall_error_type_metrics.f1:.3f}")
```

## Input Data Format

### Model Output Results Format

Results directory structure should be as follows:
```
results/
├── repo1_subfolder1/
│   └── repo1_subfolder1_error_readme_1.json
├── repo2_subfolder2/
│   └── repo2_subfolder2_error_readme_2.json
└── ...
```

Each JSON file should contain:
```json
{
    "repo_name": "repo_name",
    "readme_name": "README_1.md",
    "errors": [
        {
            "error_type": "E1",
            "error_description": "Error description",
            "fix_answer": "Fix solution"
        }
    ],
    "shell_script": "#!/bin/bash\n...",
    "raw_output": "Raw output"
}
```

### Golden Answer Format

Data root directory structure should be as follows:
```
data_root/
├── error_gen_repo1/
│   └── subfolder1/
│       ├── README_1.md
│       └── README.json
├── error_gen_repo2/
│   └── subfolder2/
│       ├── README_2.md
│       └── README.json
└── ...
```

README.json format:
```json
{
    "readme_name": "README_1.md",
    "errors": [
        {
            "error_type": "E1",
            "error_description": "Standard error description",
            "fix_answer": "Standard fix solution"
        }
    ]
}
```

## Evaluation Metrics

### Error Type Metrics
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)  
- **F1 Score**: 2 * P * R / (P + R)

### Text Similarity Metrics
- **Description Accuracy**: Proportion of error descriptions semantically similar to golden answer
- **Fix Solution Accuracy**: Proportion of fix solutions semantically similar to golden answer

## Error Matching Strategy

Since the number and order of errors output by the model may be inconsistent with the golden answer, the system uses the following matching strategy:

1. **Error Type Matching** (weight 0.6): Prioritize matching the same error type
2. **Description Similarity** (weight 0.3): Use LLM to evaluate description semantic similarity
3. **Fix Solution Similarity** (weight 0.1): Use LLM to evaluate fix solution semantic similarity

Error pairs with matching scores > 0.5 will be considered matched.

## Output Results

After evaluation completion, two files will be generated:

1. **detailed_evaluation_results.json**: Contains all detailed evaluation information
2. **evaluation_summary.json**: Contains summary statistics

Example summary results:
```json
{
    "Total Files": 100,
    "Overall Metrics": {
        "Error Type": {
            "Precision": 0.85,
            "Recall": 0.78,
            "F1 Score": 0.81
        },
        "Description Accuracy": 0.72,
        "Fix Solution Accuracy": 0.68
    },
    "By Error Type Breakdown": {
        "E1": {"Precision": 0.90, "Recall": 0.85, "F1 Score": 0.87},
        "E2": {"Precision": 0.80, "Recall": 0.75, "F1 Score": 0.77}
    }
}
```

## Testing

Run the test script to verify system functionality:

```bash
python test_evaluation.py
```

Note: Testing requires a valid OpenAI API key.

## Important Notes

1. **API Call Costs**: Text similarity evaluation will call OpenAI API, please be aware of API usage costs
2. **Processing Time**: Evaluation of large numbers of files may take considerable time
3. **Error Handling**: The system will skip files that cannot be processed and continue evaluating other files
4. **Path Matching**: Ensure readme_name can correctly match to corresponding golden answer files

## Extended Features

To add new evaluation metrics or modify matching strategies, you can:

1. Modify `evaluation_models.py` to add new data models
2. Implement new evaluation logic in `evaluation_engine.py`
3. Update `error_matcher.py` to adjust matching strategies