#!/bin/bash

# Function to check the last command's exit status
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Create miniconda directory and download installer
echo "Setting up Miniconda..."
mkdir -p ~/miniconda3
check_error "Creating miniconda directory"

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
check_error "Downloading Miniconda"

# Install miniconda
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
check_error "Installing Miniconda"

rm ~/miniconda3/miniconda.sh

# Initialize conda for bash
echo "Initializing conda..."
eval "$(~/miniconda3/bin/conda shell.bash hook)"
check_error "Initializing conda"

# Create and activate conda environment
echo "Creating conda environment..."
conda create -n zero python=3.9 -y
check_error "Creating conda environment"

echo "Activating conda environment..."
conda activate zero
check_error "Activating conda environment"

# Install CUDA toolkit and PyTorch dependencies
echo "Installing CUDA toolkit and PyTorch..."
conda install pytorch cuda-toolkit nvcc -c pytorch -c nvidia -y
check_error "Installing CUDA toolkit"

# Install PyTorch
echo "Installing PyTorch..."
pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu121
check_error "Installing PyTorch"

# Install vllm and ray
echo "Installing vllm and ray..."
pip install vllm==0.6.3
check_error "Installing vllm"

pip install ray
check_error "Installing ray"

# Install requirements
echo "Installing requirements from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    check_error "Installing requirements"
else
    echo "Warning: requirements.txt not found"
fi

# Install additional packages
echo "Installing additional packages..."
pip install flash-attn --no-build-isolation
check_error "Installing flash-attn"

pip install wandb IPython matplotlib
check_error "Installing additional packages"

echo "Installation completed successfully!"