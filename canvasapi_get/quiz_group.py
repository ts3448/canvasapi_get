from canvasapi_get.canvas_object import CanvasObject


class QuizGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)
