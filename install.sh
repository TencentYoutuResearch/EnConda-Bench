#!/bin/bash

# EnConda-Bench Installation Script
#
# This script provides automated installation for the EnConda-Bench project.
# It handles dependency management, environment setup, and configuration for both
# the inference and evaluation systems.
#
# Key Features:
# - Automatic Python version checking (requires 3.10+)
# - Docker installation verification and image pulling
# - UV package manager installation with pip fallback
# - Virtual environment creation and dependency installation
# - Configuration file generation with templates
# - Installation verification and testing
# - Comprehensive usage instructions
#
# Usage:
#   ./install.sh
#
# Requirements:
# - Python 3.10 or higher
# - Internet connection for downloading dependencies
# - Docker (optional, for evaluation system)
# - curl or wget (for UV installation)

set -e  # Exit on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
check_python_version() {
    log_info "Checking Python version..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        log_error "Python not found. Please install Python 3.10 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        log_error "Python version too low: $PYTHON_VERSION. Requires Python 3.10 or higher."
        exit 1
    fi
    
    log_success "Python version check passed: $PYTHON_VERSION"
}

# Check Docker
check_docker() {
    log_info "Checking Docker..."
    
    if ! command_exists docker; then
        log_warning "Docker not found. Some features may not be available."
        log_info "Please visit https://docs.docker.com/get-docker/ to install Docker"
        return 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        log_warning "Docker is not running or insufficient permissions."
        log_info "Please start Docker or add current user to docker group:"
        log_info "sudo usermod -aG docker \$USER"
        return 1
    fi
    
    log_success "Docker check passed"
    return 0
}

# Install UV package manager
install_uv() {
    log_info "Checking UV package manager..."
    
    if command_exists uv; then
        log_success "UV is already installed"
        return 0
    fi
    
    log_info "Installing UV package manager..."
    if command_exists curl; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command_exists wget; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        log_error "Need curl or wget to install UV"
        return 1
    fi
    
    # Reload PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if command_exists uv; then
        log_success "UV installation successful"
        return 0
    else
        log_error "UV installation failed"
        return 1
    fi
}

# Install dependencies using UV
install_with_uv() {
    log_info "Installing project dependencies using UV..."
    
    # Sync all dependencies
    uv sync
    
    log_success "UV dependency installation completed"
}

# Install dependencies using pip
install_with_pip() {
    log_info "Installing project dependencies using pip..."
    
    # Create virtual environment
    log_info "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        log_error "Cannot find virtual environment activation script"
        exit 1
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install inference system dependencies
    if [ -f "Inference/requirements.txt" ]; then
        log_info "Installing inference system dependencies..."
        pip install -r Inference/requirements.txt
    fi
    
    # Install evaluation system dependencies
    if [ -f "Evaluation/Execution/pyproject.toml" ]; then
        log_info "Installing evaluation system dependencies..."
        cd Evaluation/Execution
        pip install -e .
        cd ../..
    fi
    
    log_success "Pip dependency installation completed"
}

# Pull Docker images
pull_docker_images() {
    log_info "Pulling Docker images..."
    
    # Python environment image
    if docker pull ghcr.io/research-org/envbench-python:latest; then
        log_success "Python image pulled successfully"
    else
        log_warning "Python image pull failed, will try local build"
        if [ -f "Dockerfiles/python.Dockerfile" ]; then
            log_info "Building Python Docker image..."
            docker build -f Dockerfiles/python.Dockerfile -t envbench-python .
            log_success "Python image build completed"
        fi
    fi
    
    # JVM environment image (optional)
    if docker pull ghcr.io/research-org/envbench-jvm:latest; then
        log_success "JVM image pulled successfully"
    else
        log_warning "JVM image pull failed (optional)"
    fi
}

# Create configuration files
create_config_files() {
    log_info "Creating configuration files..."
    
    # Create .env file
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# HuggingFace Configuration (optional)
HF_TOKEN=your_huggingface_token_here

# Data Path Configuration
DATA_ROOT=./Benchmark_Data
TEMP_DIR=/tmp/envbench

# Docker Configuration
DOCKER_TIMEOUT=600

# Log Level
LOG_LEVEL=INFO

# Concurrency Settings
INFERENCE_WORKERS=4
EVAL_WORKERS=4
EOF
        log_success "Created .env configuration file"
        log_warning "Please edit .env file and add your API keys"
    else
        log_info ".env file already exists, skipping creation"
    fi
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Verify Python imports
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    elif command_exists uv; then
        # Use UV run
        UV_RUN="uv run"
    fi
    
    # Test basic imports
    if ${UV_RUN:-$PYTHON_CMD} -c "import openai, pydantic; print('✓ Core dependencies imported successfully')" 2>/dev/null; then
        log_success "Core dependencies verification passed"
    else
        log_error "Core dependencies verification failed"
        return 1
    fi
    
    # Test project imports
    if [ -d "Inference/core" ]; then
        cd Inference
        if ${UV_RUN:-$PYTHON_CMD} -c "from core.models.data_models import ErrorInfo; print('✓ Project modules imported successfully')" 2>/dev/null; then
            log_success "Project modules verification passed"
        else
            log_warning "Project modules verification failed, may need manual check"
        fi
        cd ..
    fi
    
    # Verify Docker
    if command_exists docker && docker info >/dev/null 2>&1; then
        if docker run --rm hello-world >/dev/null 2>&1; then
            log_success "Docker verification passed"
        else
            log_warning "Docker verification failed"
        fi
    fi
}

# Show usage instructions
show_usage() {
    log_info "Installation completed! Usage instructions:"
    echo ""
    echo "1. Configure API keys:"
    echo "   Edit .env file and add your OpenAI API key"
    echo ""
    echo "2. Run inference analysis:"
    echo "   cd Inference"
    if command_exists uv; then
        echo "   uv run python run.py --mode llm"
    else
        echo "   source ../venv/bin/activate  # Linux/Mac"
        echo "   # or source ../venv/Scripts/activate  # Windows"
        echo "   python run.py --mode llm"
    fi
    echo ""
    echo "3. Run evaluation:"
    echo "   cd Evaluation/Evaluate"
    echo "   python run_evaluation.py --help"
    echo ""
    echo "4. View documentation:"
    echo "   README.md (English) or README_zh.md (Chinese)"
    echo "   DEPENDENCIES.md (Dependency documentation)"
    echo ""
}

# Main function
main() {
    log_info "Starting EnConda-Bench installation..."
    echo ""
    
    # Check basic environment
    check_python_version
    DOCKER_AVAILABLE=0
    if check_docker; then
        DOCKER_AVAILABLE=1
    fi
    
    echo ""
    
    # Choose installation method
    if install_uv; then
        log_info "Using UV for installation..."
        install_with_uv
    else
        log_warning "UV installation failed, falling back to pip..."
        install_with_pip
    fi
    
    echo ""
    
    # Docker related installation
    if [ $DOCKER_AVAILABLE -eq 1 ]; then
        pull_docker_images
        echo ""
    fi
    
    # Create configuration files
    create_config_files
    echo ""
    
    # Verify installation
    verify_installation
    echo ""
    
    # Show usage instructions
    show_usage
    
    log_success "Installation completed!"
}

# Run main function
main "$@"