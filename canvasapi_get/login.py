from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.util import combine_kwargs


class Login(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.id, self.unique_id)

    def get_authentication_events(self, **kwargs):
        """
        List authentication events for a given login.

        :calls: `GET /api/v1/audit/authentication/logins/:login_id \
        <https://canvas.instructure.com/doc/api/authentications_log.html#method.authentication_audit_api.for_login>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
                :class:`canvasapi_get.authentication_event.AuthenticationEvent`
        """
        from canvasapi_get.authentication_event import AuthenticationEvent

        return PaginatedList(
            AuthenticationEvent,
            self._requester,
            "GET",
            "audit/authentication/logins/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
