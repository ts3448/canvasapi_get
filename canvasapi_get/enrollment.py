from canvasapi_get.canvas_object import CanvasObject


class Enrollment(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.type, self.id)
