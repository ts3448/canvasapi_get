from canvasapi.canvas_object import CanvasObject


class Rubric(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)


class RubricAssessment(CanvasObject):
    def __str__(self):
        return "{}, {}".format(self.id, self.artifact_type)


class RubricAssociation(CanvasObject):
    def __str__(self):
        return "{}, {}".format(self.id, self.association_type)
