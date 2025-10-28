# 环境配置分析工具

基于大语言模型和智能代理的Python环境配置错误检测与修复任务。

## 🌟 功能特性

- **错误检测**: 自动检测README文件中的环境配置错误
- **脚本生成**: 生成修复后的环境配置脚本
- **批量处理**: 支持大规模数据集的批量分析
- **详细报告**: 生成完整的分析报告和统计信息

## 📋 错误类型

- **E1**: 依赖安装错误（缺失依赖、版本错误等）
- **E2**: 命令使用或语法错误
- **E4**: 文件路径或缺失文件错误
- **E6**: 逻辑顺序错误
- **E7**: 版本兼容性错误
- **E8**: 其他杂项错误

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置设置

1. **LLM模式配置** (`configs/llm_config.yaml`):
```yaml
openai:
  api_key: "your-openai-api-key"
  model_name: "gpt-4"
  base_url: "https://api.openai.com/v1"
```

2. **Agent模式配置** (`configs/agent_config.yaml`):
```yaml
agent:
  api_key: "your-api-key"
  model_name: "gpt-4"
```

### 运行分析

#### 基本用法

```bash
# 使用LLM模式
python run.py --mode llm --data-dir ./data --output-dir ./output

# 使用Agent模式
python run.py --mode agent --agent-type simple --data-dir ./data --output-dir ./output
```

#### 高级用法

```bash
# 采样分析（处理100个样本）
python run.py --mode llm --sample-size 100 --data-dir ./data --output-dir ./output

# 指定日志级别和文件
python run.py --mode agent --log-level DEBUG --log-file ./logs/analysis.log

# 试运行（只显示配置，不执行分析）
python run.py --dry-run --mode llm --data-dir ./data
```

## 📁 项目结构

```
EnConda-Bench/Inference/
├── core/                    # 核心模块
│   ├── models/             # 数据模型
│   ├── processors/         # 处理器
│   └── clients/            # 客户端实现
├── configs/                # 配置文件
│   ├── llm_config.yaml    # LLM配置
│   ├── agent_config.yaml  # Agent配置
│   └── error_type.json    # 错误类型定义
├── scripts/               # 脚本文件
├── utils/                 # 工具模块
├── docs/                  # 文档
├── run.py                 # 主运行脚本
└── requirements.txt       # 依赖包列表
```

## 🔧 配置说明

### LLM模式配置

- `openai.api_key`: OpenAI API密钥
- `openai.model_name`: 使用的模型名称
- `data.data_root_dir`: 数据根目录
- `output.output_dir`: 输出目录

### Agent模式配置

- `agent.type`: Agent类型（simple/real）
- `environment.type`: 环境类型（local/docker）
- `task.max_iterations`: 最大迭代次数
- `tools`: 工具配置

## 📊 输出说明

### 生成的文件

1. **错误分析JSON** (`results/<repo_name>/<readme_name>_errors.json`)
2. **修复脚本** (`results/<repo_name>/<readme_name>_setup.sh`)
3. **处理记录** (`processing_records.jsonl`)
4. **摘要报告** (`summary_report.json`)

### 输出示例

```json
{
  "repo_name": "example_repo",
  "readme_name": "readme_0",
  "errors": [
    {
      "error_type": "E1",
      "error_description": "缺少requirements.txt文件",
      "fix_answer": "创建requirements.txt文件并列出所需依赖"
    }
  ]
}
```

## 🛠️ 开发指南

### 扩展Agent功能

1. 继承 `AgentFramework` 协议
2. 实现 `execute_task` 方法
3. 在 `AgentEnvironmentConfigProcessor` 中注册新的Agent类型

## 🔍 故障排除

### 常见问题

1. **API密钥错误**: 检查配置文件中的API密钥设置
2. **数据路径错误**: 确认数据目录路径正确
3. **依赖包缺失**: 运行 `pip install -r requirements.txt`

### 日志分析

启用详细日志来诊断问题：

```bash
python run.py --log-level DEBUG --log-file ./logs/debug.log
```

## 📈 性能优化

- 使用采样功能处理大数据集
- 调整并发处理数量
- 启用结果缓存

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 参与讨论