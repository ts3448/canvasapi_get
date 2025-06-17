from canvasapi.canvas_object import CanvasObject


class SisImport(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.workflow_state, self.id)
