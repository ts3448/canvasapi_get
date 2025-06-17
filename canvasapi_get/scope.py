from canvasapi_get.canvas_object import CanvasObject


class Scope(CanvasObject):
    def __str__(self):
        return "{}".format(self.resource)
