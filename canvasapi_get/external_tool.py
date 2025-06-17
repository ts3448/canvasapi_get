from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.exceptions import CanvasException
from canvasapi_get.util import combine_kwargs


class ExternalTool(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    @property
    def parent_id(self):
        """
        Return the id of the course or account that spawned this tool.

        :rtype: int
        """
        if hasattr(self, "course_id"):
            return self.course_id
        elif hasattr(self, "account_id"):
            return self.account_id
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    @property
    def parent_type(self):
        """
        Return whether the tool was spawned from a course or account.

        :rtype: str
        """
        if hasattr(self, "course_id"):
            return "course"
        elif hasattr(self, "account_id"):
            return "account"
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    def get_parent(self, **kwargs):
        """
        Return the object that spawned this tool.

        :rtype: :class:`canvasapi_get.account.Account` or :class:`canvasapi_get.account.Course`
        """
        from canvasapi_get.account import Account
        from canvasapi_get.course import Course

        response = self._requester.request(
            "GET",
            "{}s/{}".format(self.parent_type, self.parent_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if self.parent_type == "account":
            return Account(self._requester, response.json())
        elif self.parent_type == "course":
            return Course(self._requester, response.json())
        return None

    def get_sessionless_launch_url(self, **kwargs):
        """
        Return a sessionless launch url for an external tool.

        :calls: `GET /api/v1/courses/:course_id/external_tools/sessionless_launch
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch>`_
            or `GET /api/v1/accounts/:account_id/external_tools/sessionless_launch \
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch>`_

        :rtype: str
        """
        kwargs["id"] = self.id
        response = self._requester.request(
            "GET",
            "{}s/{}/external_tools/sessionless_launch".format(
                self.parent_type, self.parent_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        try:
            return response.json()["url"]
        except KeyError:
            raise CanvasException("Canvas did not respond with a valid URL")
