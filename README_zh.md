# EnConda-Bench: 软件工程智能体中环境配置的过程级轨迹评估

一个用于评估AI智能体在Python环境配置任务上性能的综合基准测试框架。

## 🌟 项目概述

EnConda-Bench是一个端到端的环境配置基准测试系统，专门设计用于评估大语言模型和AI智能体在识别、分析和修复Python环境配置错误方面的能力。该系统提供了完整的数据集、推理工具和评估框架。

## 📁 项目结构

```
EnConda-Bench/
├── Benchmark_Data/           # 基准数据集
│   ├── error_types.json         # 错误类型定义
│   ├── Enconda_benchmark_data.jsonl  # 主要基准数据
│   └── final_output_benchmark_data_final/  # 处理后的数据集
├── Inference/                # 推理系统
│   ├── core/                     # 核心推理模块
│   ├── configs/                  # 配置文件
│   ├── scripts/                  # 运行脚本
│   └── docs/                     # 文档
├── Evaluation/               # 评估系统
│   ├── Evaluate/                 # 自动指标评估
│   └── Execution/                # 端到端执行测试
└── Dockerfiles/              # Docker配置文件
```

## 🎯 核心功能

### 1. 数据集 (Benchmark_Data)

- **错误类型定义**: 6种主要的环境配置错误类型 (E1-E8)
- **真实场景数据**: 基于真实GitHub仓库的README文件
- **标准化格式**: 结构化的JSON/JSONL数据格式
- **repos**: 可从 [HuggingFace数据集](https://huggingface.co/datasets/JetBrains-Research/EnvBench/tree/main/repos/final/python) 下载原始仓库

#### 支持的错误类型

| 类型 | 名称 | 描述 |
|------|------|------|
| E1 | 依赖安装错误 | 缺失依赖、版本错误等 |
| E2 | 命令使用或语法错误 | 错误的命令、参数或语法 |
| E4 | 文件路径或缺失文件错误 | 路径错误或文件不存在 |
| E6 | 逻辑顺序错误 | 安装步骤顺序错误 |
| E7 | 版本兼容性错误 | 版本冲突或不兼容 |
| E8 | 其他杂项错误 | 格式问题、描述不清等 |

### 2. 推理系统 (Inference)

智能体推理系统，支持两种模式：

- **LLM模式**: 基于大语言模型的直接分析
- **Agent模式**: 基于智能代理的交互式分析

#### 主要特性
- 🔍 自动错误检测和分类
- 🛠️ 生成修复脚本
- 📊 批量处理和分析
- 📈 详细的统计报告

### 3. 评估系统 (Evaluation)

双重评估框架：

#### 自动指标评估 (Evaluate)
- **错误类型准确性**: 精确率、召回率、F1分数
- **文本相似度**: 基于LLM的语义相似度评估
- **智能匹配**: 处理预测与标准答案的不一致

#### 端到端执行测试 (Execution)
- **Docker容器**: 隔离的执行环境
- **脚本验证**: 实际执行生成的配置脚本
- **成功率统计**: 环境配置成功率分析
- **错误诊断**: 详细的执行日志和错误分析

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Docker Engine
- 8GB+ RAM (推荐)
- OpenAI API密钥 (用于LLM评估)

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd EnConda-Bench

# 安装Python依赖
pip install -r requirements.txt

# 或使用uv (推荐)
uv sync
```

### Docker环境准备

```bash
# 拉取预构建镜像
docker pull ghcr.io/research-org/envbench-python:latest

# 或构建本地镜像
docker build -f Dockerfiles/python.Dockerfile -t envbench-python .
```

### 配置设置

1. **创建环境变量文件**:
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 OpenAI API 密钥
```

2. **配置推理参数** (`Inference/configs/llm_config.yaml`):
```yaml
openai:
  api_key: "your-openai-api-key"
  model_name: "gpt-4"
  base_url: "https://api.openai.com/v1"
```

## 📖 使用指南

### 1. 运行推理分析

```bash
cd Inference

# LLM模式
python run.py --mode llm --config configs/llm_config.yaml

# Agent模式  
python run.py --mode agent --config configs/agent_config.yaml
```

### 2. 评估结果

#### 自动指标评估
```bash
cd Evaluation/Evaluate

python run_evaluation.py \
    --results_dir /path/to/inference/results \
    --data_root_dir /path/to/Benchmark_Data \
    --output_dir evaluation_output
```

#### 端到端执行测试
```bash
cd Evaluation/Execution

# 转换数据格式
python convert_to_jsonl.py \
    --input_file inference_results.jsonl \
    --output_file execution_input.jsonl

# 运行执行测试
./uv_run.sh
```

### 3. 查看结果

评估完成后，结果将保存在指定的输出目录中：

- `detailed_evaluation_results.json`: 详细评估结果
- `evaluation_summary.json`: 摘要统计
- `results.jsonl`: 执行测试结果

## 📊 评估指标

### 自动指标
- **错误类型识别**: 精确率、召回率、F1分数
- **描述准确性**: 错误描述的语义相似度
- **修复方案质量**: 修复方案的语义相似度

### 执行指标
- **环境配置成功率**: 脚本执行成功的比例
- **清洁通过率**: 无任何问题的环境配置比例
- **错误诊断**: 具体的失败原因分析

## 🔧 自定义和扩展

### 添加新的错误类型

1. 更新 `Benchmark_Data/error_types.json`
2. 在推理系统中添加相应的检测逻辑
3. 更新评估指标计算

### 支持新的编程语言

1. 创建新的Dockerfile (`Dockerfiles/new_language.Dockerfile`)
2. 添加语言特定的配置文件
3. 扩展推理和评估逻辑

### 集成新的LLM模型

1. 在 `Inference/core/clients/` 中添加新的客户端
2. 更新配置文件格式
3. 测试兼容性

## 📈 性能优化

### 推理优化
- 使用批处理减少API调用
- 启用结果缓存
- 并行处理多个文件

### 评估优化
- 调整Docker资源限制
- 使用SSD存储提升I/O性能
- 合理设置并发worker数量

## 📄 许可证

本项目采用开源许可证，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢EnvBench项目提供的端到端执行框架
- 感谢所有贡献者的努力
- 感谢开源社区的支持

---

*如果这个项目对你有帮助，请给我们一个⭐️！*