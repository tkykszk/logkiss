import logkiss as logging
import logkiss as logging
print("=== DEBUG: logkiss.__file__ ===", logging.__file__)
logging.warning("Minimal example for beginners")
print("handlers:", logging.getLogger().handlers)
for h in logging.getLogger().handlers:
    print("handler repr:", repr(h))
    print("handler type:", type(h))
