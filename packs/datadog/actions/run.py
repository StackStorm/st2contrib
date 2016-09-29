import importlib
from st2actions.runners.pythonrunner import Action


class ActionWrapper(Action):
    def __init__(self, config):
        self.config = config

    def run(self, **kwargs):
        cls_name = kwargs.pop("cls")
        module_path = kwargs.pop("module_path")
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name)(self.config)
        return cls.run(**kwargs)
