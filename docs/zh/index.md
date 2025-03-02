# logkiss

![logkiss logo](https://via.placeholder.com/200x100?text=logkiss)

**logkiss**是一个简单而美观的Python日志库。

## 特点

- **彩色日志输出** - 通过颜色编码的日志级别提高可见性
- **简单API** - 易于使用的API，与标准Python日志兼容
- **云就绪** - 支持AWS CloudWatch和Google Cloud Logging
- **可定制** - 轻松自定义颜色和格式

## 快速开始

```python
import logkiss as logging

# 获取日志记录器
logger = logging.getLogger(__name__)

# 输出日志
logger.debug("调试信息")
logger.info("信息消息")
logger.warning("警告消息")
logger.error("错误消息")
logger.critical("严重错误消息")
```

## 安装

```bash
pip install logkiss
```

对于云日志功能：

```bash
pip install "logkiss[cloud]"
```

## 许可证

根据MIT许可证分发。有关更多信息，请参阅[LICENSE](https://github.com/yourusername/logkiss/blob/main/LICENSE)文件。
