from canvasapi.canvas_object import CanvasObject


class PlannerNote(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.title, self.todo_date, self.id)


class PlannerOverride(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.plannable_id, self.marked_complete, self.id)
