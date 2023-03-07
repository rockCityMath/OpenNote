import os
import importlib

def get_plugins():
    plugins = {}

    for filename in os.listdir("./plugins"):
        if filename[-3:]!=".py": continue
        className = filename[:-3]
        #begin magic
        module = importlib.__import__(f"plugins.{className}")
        c = getattr(getattr(module,className),className)
        #end magic
        plugins[className]=c

    return plugins.items()
