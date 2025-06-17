from canvasapi.canvas_object import CanvasObject
from canvasapi.poll_submission import PollSubmission
from canvasapi.util import combine_kwargs, obj_or_id


class PollSession(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.poll_id, self.id)

    def close(self, **kwargs):
        """
        Close a poll session to answers based on the poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id/close \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.close>`_

        :returns: :class:`canvasapi-get.poll_session.PollSession`
        """
        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/close".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def get_submission(self, poll_submission, **kwargs):
        """
        Returns the poll submission with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions/:id \
        <https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.show>`_

        :param poll_submission: Takes a poll submission id (int) or object.
        :type poll_submission: int or :class:`canvasapi.poll_submission.PollSubmission`

        :rtype: :class:`canvasapi.poll_submission.PollSubmission`
        """
        poll_submission_id = obj_or_id(
            poll_submission, "poll_submission", (PollSubmission,)
        )

        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/poll_submissions/{}".format(
                self.poll_id, self.id, poll_submission_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSubmission(self._requester, response.json()["poll_submissions"][0])

    def open(self, **kwargs):
        """
        Open a poll session to answers based on the poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id/open \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.open>`_

        :returns: :class:`canvasapi-get.poll_session.PollSession`
        """
        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/open".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])
