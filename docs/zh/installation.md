# 安装

## 要求

- Python 3.8或更高版本

## 使用pip安装

最简单的安装方法是使用pip：

```bash
pip install logkiss
```

对于云日志功能（AWS CloudWatch和Google Cloud Logging）：

```bash
pip install "logkiss[cloud]"
```

## 使用PDM安装

如果您使用PDM，可以通过以下方式安装：

```bash
pdm add logkiss
```

对于云日志功能：

```bash
pdm add "logkiss[cloud]"
```

## 使用Poetry安装

如果您使用Poetry，可以通过以下方式安装：

```bash
poetry add logkiss
```

对于云日志功能：

```bash
poetry add "logkiss[cloud]"
```

## 从源代码安装

如果您想使用最新的开发版本，可以克隆GitHub仓库并直接安装：

```bash
git clone https://github.com/yourusername/logkiss.git
cd logkiss
pip install -e .
```

## 依赖项

- **必需**: PyYAML
- **可选**: 
  - 对于AWS CloudWatch: boto3
  - 对于Google Cloud Logging: google-cloud-logging
