from lib.action import PyraxBaseAction
from lib.formatters import to_server_dict

__all__ = [
    'ListVMImagesAction'
]

class ListVMImagesAction(PyraxBaseAction):
    def run(self):
        cs = self.pyrax.cloudservers
        imgs = cs.images.list()
        result = {}

        for img in imgs:
            result[img.id] = img.name

        return result
