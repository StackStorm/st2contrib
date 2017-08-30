from lib.action import PyraxBaseAction

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
