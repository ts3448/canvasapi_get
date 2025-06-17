from canvasapi_get.canvas_object import CanvasObject


class Conversation(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.subject, self.id)
