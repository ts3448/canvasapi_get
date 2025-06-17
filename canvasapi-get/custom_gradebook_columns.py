from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class CustomGradebookColumn(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def get_column_entries(self, **kwargs):
        """
        Returns a list of ColumnData objects.

        :calls: `GET /api/v1/courses/:course_id/custom_gradebook_columns/:id/data \
            <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.index>`_

        :rtype: :class:`canvasapi-get.paginated_list.PaginatedList` of
            :class:`canvasapi-get.custom_gradebook_columns.ColumnData`
        """
        return PaginatedList(
            ColumnData,
            self._requester,
            "GET",
            "courses/{}/custom_gradebook_columns/{}/data".format(
                self.course_id, self.id
            ),
            {"course_id": self.course_id, "gradebook_column_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )


class ColumnData(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.user_id, self.content)
