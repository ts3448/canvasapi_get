from canvasapi.canvas_object import CanvasObject


class AuthenticationProvider(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.auth_type, self.position)
