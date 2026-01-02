# Installation Guide

Complete step-by-step instructions for setting up VRPTW-GRASP with GAA Integration.

## System Requirements

- **Python**: 3.10 or higher (tested on 3.14.0)
- **OS**: Windows, Linux, or macOS
- **RAM**: 2GB minimum (4GB+ recommended)
- **Disk**: 500MB free space

## Prerequisites

### Windows

1. **Python Installation**
   ```powershell
   # Download from python.org or use Windows Store
   python --version  # Should be 3.10+
   ```

2. **Git** (optional but recommended)
   ```powershell
   # Download from git-scm.com
   git --version
   ```

### Linux/macOS

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip

# macOS
brew install python3
```

## Step 1: Clone Repository

```bash
# Using Git
git clone https://github.com/username/GAA-VRPTW-GRASP-2.git
cd GAA-VRPTW-GRASP-2

# Or download ZIP and extract
unzip GAA-VRPTW-GRASP-2.zip
cd GAA-VRPTW-GRASP-2
```

## Step 2: Create Virtual Environment

### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```cmd
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate.bat
```

### Linux/macOS

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

**Verify activation**:
```bash
which python  # Should show path to .venv/python
python --version  # Should show 3.10+
```

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

### Required Packages

```
pandas>=1.3.0        # Data manipulation
numpy>=1.21.0        # Numerical computing
scipy>=1.7.0         # Statistical functions
matplotlib>=3.4.0    # Plotting and visualization
pytest>=7.0.0        # Testing framework
pytest-cov>=3.0.0    # Code coverage
pyyaml>=5.4.0        # Configuration files
```

## Step 4: Verify Installation

```bash
# Run pytest to verify all tests pass
pytest -v

# Expected output: 253 passed
```

### Quick Test

```bash
# Test imports
python -c "import pandas, numpy, scipy, matplotlib; print('All imports OK')"

# Test framework
python -c "from src.core.instance import Instance; print('Framework OK')"
```

## Step 5: Download Datasets (Optional)

The Solomon benchmark instances should already be in `datasets/benchmark/`. To verify:

```bash
# Check if datasets exist
ls datasets/benchmark/  # Should show C101.csv, C102.csv, etc.

# Verify 56 instances are present
ls datasets/benchmark/*.csv | wc -l  # Should output 56
```

If missing, follow [USAGE.md](USAGE.md#loading-datasets) to load them.

## Configuration

### Main Configuration File: config.yaml

```yaml
solver:
  name: "GRASP-ILS"
  seed: 42
  max_iterations: 100
  max_runtime: 300

dataset:
  instances_dir: "datasets/benchmark"
  format: "csv"

output:
  directory: "output"
  timestamp_format: "DD-MM-YY_HH-MM-SS"
```

See [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) for all options.

## Project Structure

```
GAA-VRPTW-GRASP-2/
├── .venv/                    # Virtual environment
├── src/
│   ├── core/                # Core classes
│   ├── gaa/                 # Algorithm generation
│   └── utils/               # Utilities
├── scripts/                 # Executable scripts
├── datasets/                # Benchmark instances
├── output/                  # Experiment results
├── tests/                   # Test files
├── config.yaml             # Configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Troubleshooting

### Python Version Issue

```bash
# Check Python version
python --version

# If Python 2 is default
python3 -m venv .venv
```

### Virtual Environment Not Activating

```powershell
# Windows PowerShell - If execution policy blocked:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activation again
.\.venv\Scripts\Activate.ps1
```

### Import Errors

```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Check installation
pip list | grep -E "pandas|numpy|scipy|matplotlib"
```

### Tests Failing

```bash
# Run with verbose output
pytest -v --tb=short

# Run single test file
pytest scripts/test_phase11.py -v

# Check coverage
pytest --cov=src --cov-report=html
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.

## Next Steps

1. **Read [USAGE.md](USAGE.md)** - Learn how to use the framework
2. **Check [EXAMPLES.md](EXAMPLES.md)** - See code examples
3. **Review [API_REFERENCE.md](API_REFERENCE.md)** - Class documentation
4. **Explore [ARCHITECTURE.md](ARCHITECTURE.md)** - System design

## Development Setup

For developers who want to contribute:

```bash
# Install development dependencies (if available)
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run code quality checks
flake8 src/
pylint src/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Getting Help

- **Installation Issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **General Questions**: See [FAQ.md](FAQ.md)
- **Code Documentation**: See [API_REFERENCE.md](API_REFERENCE.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)

---

**Last Updated**: January 2, 2026  
**Status**: Installation Verified ✅
