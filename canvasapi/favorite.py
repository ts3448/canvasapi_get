from canvasapi.canvas_object import CanvasObject


class Favorite(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.context_type, self.context_id)
