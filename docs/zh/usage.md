# 使用方法

## 基本用法

logkiss与标准Python日志模块兼容，可以以类似的方式使用。

```python
import logkiss as logging

# 获取日志记录器
logger = logging.getLogger(__name__)

# 设置日志级别
logger.setLevel(logging.DEBUG)

# 输出日志
logger.debug("调试信息")
logger.info("信息消息")
logger.warning("警告消息")
logger.error("错误消息")
logger.critical("严重错误消息")
```

## 使用KissConsoleHandler

logkiss的主要特点是`KissConsoleHandler`，它提供彩色控制台输出。

```python
import logkiss as logging

# 获取日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 清除现有处理器
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 添加KissConsoleHandler
console_handler = logging.KissConsoleHandler()
logger.addHandler(console_handler)

# 输出日志
logger.debug("调试信息")
logger.info("信息消息")
logger.warning("警告消息")
logger.error("错误消息")
logger.critical("严重错误消息")
```

## 禁用颜色

在某些环境中，您可能不需要彩色输出。您可以按如下方式禁用颜色：

```python
import logkiss as logging

# 获取日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 清除现有处理器
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 创建禁用颜色的格式化器
formatter = logging.ColoredFormatter(use_color=False)

# 添加KissConsoleHandler并设置格式化器
console_handler = logging.KissConsoleHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 输出日志
logger.debug("无颜色的调试信息")
logger.info("无颜色的信息消息")
logger.warning("无颜色的警告消息")
logger.error("无颜色的错误消息")
```

## 记录到文件

要记录到文件，请使用标准的`FileHandler`与`ColoredFormatter`：

```python
import logging
from logkiss import ColoredFormatter

# 创建记录器
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# 添加FileHandler与ColoredFormatter
file_handler = logging.FileHandler("app.log")
formatter = ColoredFormatter(use_color=False)  # 为文件输出禁用颜色
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 记录消息
logger.debug("调试消息")
logger.info("信息消息")
logger.warning("警告消息")
logger.error("错误消息")
logger.critical("严重消息")
```

## 记录到AWS CloudWatch

要将日志发送到AWS CloudWatch，请使用`AWSCloudWatchHandler`：

```python
import logkiss as logging
from logkiss.handlers import AWSCloudWatchHandler

# 获取日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 添加AWSCloudWatchHandler
aws_handler = AWSCloudWatchHandler(
    log_group_name="my-log-group",
    log_stream_name="my-log-stream",
    region_name="ap-northeast-1"
)
logger.addHandler(aws_handler)

# 输出日志
logger.info("发送到AWS CloudWatch的信息消息")
```

## 记录到Google Cloud Logging

要将日志发送到Google Cloud Logging，请使用`GCPCloudLoggingHandler`：

```python
import logkiss as logging
from logkiss.handlers import GCPCloudLoggingHandler

# 获取日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 添加GCPCloudLoggingHandler
gcp_handler = GCPCloudLoggingHandler(
    project_id="my-gcp-project",
    log_name="my-log"
)
logger.addHandler(gcp_handler)

# 输出日志
logger.info("发送到Google Cloud Logging的信息消息")
```
