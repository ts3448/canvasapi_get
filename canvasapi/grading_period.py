from canvasapi.canvas_object import CanvasObject


class GradingPeriod(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)
