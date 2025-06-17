from canvasapi.canvas_object import CanvasObject


class PollChoice(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.text, self.id)
