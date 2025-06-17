from canvasapi.bookmark import Bookmark
from canvasapi.course import Course
from canvasapi.group import Group
from canvasapi.paginated_list import PaginatedList
from canvasapi.user import User
from canvasapi.util import combine_kwargs, obj_or_id


class CurrentUser(User):
    def __init__(self, _requester):
        self._requester = _requester

        response = self._requester.request("GET", "users/self")

        super(CurrentUser, self).__init__(self._requester, response.json())

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_bookmark(self, bookmark, **kwargs):
        """
        Return single Bookmark by id

        :calls: `GET /api/v1/users/self/bookmarks/:id \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.show>`_

        :param bookmark: The object or ID of the bookmark.
        :type bookmark: :class:`canvasapi.bookmark.Bookmark` or int

        :rtype: :class:`canvasapi.bookmark.Bookmark`
        """
        from canvasapi.bookmark import Bookmark

        bookmark_id = obj_or_id(bookmark, "bookmark", (Bookmark,))

        response = self._requester.request(
            "GET",
            "users/self/bookmarks/{}".format(bookmark_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Bookmark(self._requester, response.json())

    def get_bookmarks(self):
        """
        List bookmarks that the current user can view or manage.

        :calls: `GET /api/v1/users/self/bookmarks \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.bookmark.Bookmark`
        """
        return PaginatedList(Bookmark, self._requester, "GET", "users/self/bookmarks")

    def get_favorite_courses(self, **kwargs):
        """
        Retrieve the paginated list of favorite courses for the current user.
        If the user has not chosen any favorites,
        then a selection of currently enrolled courses will be returned.

        :calls: `GET /api/v1/users/self/favorites/courses \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_courses>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """

        return PaginatedList(
            Course,
            self._requester,
            "GET",
            "users/self/favorites/courses",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_favorite_groups(self, **kwargs):
        """
        Retrieve the paginated list of favorite groups for the current user.
        If the user has not chosen any favorites, then a selection of groups
        that the user is a member of will be returned.

        :calls: `GET /api/v1/users/self/favorites/groups \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_groups>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.Group`
        """

        return PaginatedList(
            Group,
            self._requester,
            "GET",
            "users/self/favorites/groups",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_groups(self, **kwargs):
        """
        Return the list of active groups for the user.

        :calls: `GET /api/v1/users/self/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        from canvasapi.group import Group

        return PaginatedList(
            Group,
            self._requester,
            "GET",
            "users/self/groups",
            _kwargs=combine_kwargs(**kwargs),
        )
