import logging

# 1. import直後のhandlersの中身
print("[1] after import logging:", logging.getLogger().handlers)

# 2. handlersが空ならKissConsoleHandler(ダミー)を追加
def dummy_handler():
    class DummyHandler(logging.Handler):
        def emit(self, record):
            print("DUMMY:", record.getMessage())
    return DummyHandler()

if not logging.getLogger().handlers:
    logging.getLogger().addHandler(dummy_handler())

print("[2] after adding dummy handler:", logging.getLogger().handlers)

# 3. ここでlogging.warning()を呼ぶ（StreamHandlerが自動追加されるか？）
logging.warning("This should go to dummy handler only!")
print("[3] after warning:", logging.getLogger().handlers)
