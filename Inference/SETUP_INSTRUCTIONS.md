# Setup Instructions for Real Agent Implementation

## Prerequisites

Before using the real agent implementation, you need to set up the agent dependency. We take the SWE-agent as an exapmle.

## SWE-Agent Setup

### Option 1: Clone SWE-Agent (Recommended)

1. **Clone SWE-agent repository**:
   ```bash
   git clone https://github.com/princeton-nlp/SWE-agent.git swe-agent
   ```

2. **Install SWE-agent dependencies**:
   ```bash
   cd swe-agent
   pip install -e .
   ```

### Option 2: Use Existing Installation

If you already have SWE-agent installed elsewhere:

1. **Create symbolic link**:
   ```bash
   cd EnConda-Bench/Inference
   ln -s /path/to/your/swe-agent ./swe-agent
   ```

2. **Or update configuration**:
   Edit `configs/agent.yaml` and change the `swe_agent_path` to point to your installation:
   ```yaml
   execution:
     swe_agent_path: "/path/to/your/swe-agent"
   ```

## Configuration Setup

### 1. API Key Configuration

Set your OpenAI API key in one of these ways:

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: Configuration File**
Edit `configs/agent.yaml`:
```yaml
agent:
  api_key: "your-api-key-here"
```

### 2. Verify Configuration

Check that all paths are correct:
```bash
cd EnConda-Bench/Inference
python -c "from configs.config import Config; c = Config.from_config_type('agent'); print(f'SWE-agent path: {c.swe_agent_path}')"
```

## Directory Structure

After setup, your directory structure should look like:

```
EnConda-Bench/Inference/
├── agent/
│   ├── swe_agent_wrapper.py
│   └── README.md
├── configs/
│   ├── agent.yaml
│   ├── agent_config_template.json
│   └── config.py
├── core/
│   └── clients/
│       └── agent_real_client.py
├── swe-agent/                    # SWE-agent installation
│   ├── sweagent/
│   ├── config/
│   └── ...
└── test_real_agent.py
```

## Troubleshooting

### Common Issues

1. **SWE-agent not found**:
   - Verify the `swe-agent` directory exists
   - Check the path in `configs/agent.yaml`
   - Ensure SWE-agent is properly installed

2. **API key issues**:
   - Verify your OpenAI API key is set
   - Check API key format and permissions
   - Ensure sufficient API credits

3. **Permission errors**:
   - Make sure the agent wrapper script is executable:
     ```bash
     chmod +x agent/swe_agent_wrapper.py
     ```

4. **Import errors**:
   - Verify all dependencies are installed
   - Check Python path configuration
   - Ensure SWE-agent dependencies are installed

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Production Deployment

For production use:

1. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY="your-production-key"
   export AGENT_WORK_DIR="/path/to/agent/workspace"
   ```

2. **Configure resource limits**:
   Edit `configs/agent.yaml`:
   ```yaml
   execution:
     agent_timeout: 600  # Increase for complex analyses
     max_workers: 4      # Adjust based on system resources
   ```

3. **Set up monitoring**:
   - Monitor agent execution times
   - Track API usage and costs
   - Log analysis results for review

## Security Considerations

1. **API Key Security**:
   - Never commit API keys to version control
   - Use environment variables in production
   - Rotate keys regularly

2. **Workspace Isolation**:
   - Agent workspaces are automatically isolated
   - Temporary files are cleaned up after execution
   - No persistent state between analyses

3. **Input Validation**:
   - All inputs are validated before processing
   - Malicious content is filtered out
   - Safe execution environment is maintained

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs for error details
3. Verify your configuration matches the examples
4. Ensure all dependencies are properly installed

For additional help, refer to:
- SWE-agent documentation - https://github.com/princeton-nlp/SWE-agent