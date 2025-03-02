# Installation

## Requirements

- Python 3.8 or higher

## Installation with pip

The easiest way to install is using pip:

```bash
pip install logkiss
```

To use cloud logging features (AWS CloudWatch and Google Cloud Logging), install with:

```bash
pip install "logkiss[cloud]"
```

## Installation with PDM

If you're using PDM, you can install with:

```bash
pdm add logkiss
```

For cloud logging features:

```bash
pdm add "logkiss[cloud]"
```

## Installation with Poetry

If you're using Poetry, you can install with:

```bash
poetry add logkiss
```

For cloud logging features:

```bash
poetry add "logkiss[cloud]"
```

## Installation from Source

If you want to use the latest development version, you can clone the GitHub repository and install directly:

```bash
git clone https://github.com/yourusername/logkiss.git
cd logkiss
pip install -e .
```

## Dependencies

- **Required**: PyYAML
- **Optional**: 
  - For AWS CloudWatch: boto3
  - For Google Cloud Logging: google-cloud-logging
