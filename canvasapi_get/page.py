from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.util import combine_kwargs, obj_or_id


class Page(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def get_parent(self, **kwargs):
        """
        Return the object that spawned this page.

        :calls: `GET /api/v1/groups/:group_id \
            <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_
            or
            `GET /api/v1/courses/:id \
            <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_

        :rtype: :class:`canvasapi_get.group.Group` or :class:`canvasapi_get.course.Course`
        """
        from canvasapi_get.course import Course
        from canvasapi_get.group import Group

        response = self._requester.request(
            "GET",
            "{}s/{}".format(self.parent_type, self.parent_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if self.parent_type == "group":
            return Group(self._requester, response.json())
        elif self.parent_type == "course":
            return Course(self._requester, response.json())
        return None

    def get_revision_by_id(self, revision, **kwargs):
        """
        Retrieve the contents of the revision by the id.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/:revision_id \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :param revision: The object or ID of a specified revision.
        :type revision: :class:`canvasapi_get.pagerevision.PageRevision` or int

        :returns: Contents of the page revision.
        :rtype: :class:`canvasapi_get.pagerevision.PageRevision`
        """
        revision_id = obj_or_id(revision, "revision", (PageRevision,))

        response = self._requester.request(
            "GET",
            "{}s/{}/pages/{}/revisions/{}".format(
                self.parent_type, self.parent_id, self.url, revision_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        pagerev_json = response.json()
        if self.parent_type == "group":
            pagerev_json.update({"group_id": self.id})
        elif self.parent_type == "course":
            pagerev_json.update({"course_id": self.id})

        return PageRevision(self._requester, pagerev_json)

    def get_revisions(self, **kwargs):
        """
        List the revisions of a page.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revisions>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.pagerevision.PageRevision`
        """
        return PaginatedList(
            PageRevision,
            self._requester,
            "GET",
            "{}s/{}/pages/{}/revisions".format(
                self.parent_type, self.parent_id, self.url
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    @property
    def parent_id(self):
        """
        Return the id of the course or group that spawned this page.

        :rtype: int
        """
        if hasattr(self, "course_id"):
            return self.course_id
        elif hasattr(self, "group_id"):
            return self.group_id
        else:
            raise ValueError("Page does not have a course_id or group_id")

    @property
    def parent_type(self):
        """
        Return whether the page was spawned from a course or group.

        :rtype: str
        """
        if hasattr(self, "course_id"):
            return "course"
        elif hasattr(self, "group_id"):
            return "group"
        else:
            raise ValueError("ExternalTool does not have a course_id or group_id")

    def show_latest_revision(self, **kwargs):
        """
        Retrieve the contents of the latest revision.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/latest \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :rtype: :class:`canvasapi_get.pagerevision.PageRevision`
        """
        response = self._requester.request(
            "GET",
            "{}s/{}/pages/{}/revisions/latest".format(
                self.parent_type, self.parent_id, self.url
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PageRevision(self._requester, response.json())


class PageRevision(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.updated_at, self.revision_id)

    def get_parent(self, **kwargs):
        """
        Return the object that spawned this page.

        :calls: `GET /api/v1/groups/:group_id \
            <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_
            or :calls: `GET /api/v1/courses/:id \
            <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_

        :rtype: :class:`canvasapi_get.group.Group` or :class:`canvasapi_get.course.Course`
        """
        from canvasapi_get.course import Course
        from canvasapi_get.group import Group

        response = self._requester.request(
            "GET",
            "{}s/{}".format(self.parent_type, self.parent_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if self.parent_type == "group":
            return Group(self._requester, response.json())
        elif self.parent_type == "course":
            return Course(self._requester, response.json())
        return None

    @property
    def parent_id(self):
        """
        Return the id of the course or group that spawned this page.

        :rtype: int
        """
        if hasattr(self, "course_id"):
            return self.course_id
        elif hasattr(self, "group_id"):
            return self.group_id
        else:
            raise ValueError("Page does not have a course_id or group_id")

    @property
    def parent_type(self):
        """
        Return whether the page was spawned from a course or group.

        :rtype: str
        """
        if hasattr(self, "course_id"):
            return "course"
        elif hasattr(self, "group_id"):
            return "group"
        else:
            raise ValueError("ExternalTool does not have a course_id or group_id")
