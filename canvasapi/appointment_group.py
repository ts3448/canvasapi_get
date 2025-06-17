from canvasapi.canvas_object import CanvasObject


class AppointmentGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)
