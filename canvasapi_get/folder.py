from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.util import combine_kwargs


class Folder(CanvasObject):
    def __str__(self):
        return "{}".format(self.full_name)

    def get_files(self, **kwargs):
        """
        Returns the paginated list of files for the folder.

        :calls: `GET /api/v1/folders/:id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.file.File`
        """
        from canvasapi_get.file import File

        return PaginatedList(
            File,
            self._requester,
            "GET",
            "folders/{}/files".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_folders(
        self,
    ):
        """
        Returns the paginated list of folders in the folder.

        :calls: `GET /api/v1/folders/:id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.api_index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.folder.Folder`
        """
        return PaginatedList(
            Folder, self._requester, "GET", "folders/{}/folders".format(self.id)
        )
