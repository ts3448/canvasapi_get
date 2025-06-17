from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.poll_choice import PollChoice
from canvasapi.poll_session import PollSession
from canvasapi.util import combine_kwargs, obj_or_id


class Poll(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.question, self.id)

    def get_choice(self, poll_choice, **kwargs):
        """
        Returns the poll choice with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_choices/:id \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.show>`_

        :rtype: :class:`canvasapi.poll_choice.PollChoice`
        """
        poll_choice_id = obj_or_id(poll_choice, "poll_choice", (PollChoice,))

        response = self._requester.request(
            "GET",
            "polls/{}/poll_choices/{}".format(self.id, poll_choice_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollChoice(self._requester, response.json()["poll_choices"][0])

    def get_choices(self, **kwargs):
        """
        Returns a paginated list of PollChoices of a poll, based on poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_choices \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.poll_choice.PollChoice`
        """
        return PaginatedList(
            PollChoice,
            self._requester,
            "GET",
            "polls/{}/poll_choices".format(self.id),
            _root="poll_choices",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_session(self, poll_session, **kwargs):
        """
        Returns the poll session with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.show>`_

        :param poll_session: List of arguments. Takes a poll session id (int) or poll session \
        object.

        :rtype: :class:`canvasapi.poll_session.PollSession`
        """
        poll_session_id = obj_or_id(poll_session, "poll_session", (PollSession,))

        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}".format(self.id, poll_session_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def get_sessions(self, **kwargs):
        """
        Returns the paginated list of PollSessions in a poll.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.index>`_

        :rtype: :class:`canvasapi_get.paginated_lsit.Paginated List` of
            :class:`canvasapi_get.poll_session.PollSession`
        """
        return PaginatedList(
            PollSession,
            self._requester,
            "GET",
            "polls/{}/poll_sessions".format(self.id),
            _root="poll_sessions",
            _kwargs=combine_kwargs(**kwargs),
        )
