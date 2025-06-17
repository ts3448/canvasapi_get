from canvasapi.canvas_object import CanvasObject
from canvasapi.file import File
from canvasapi.paginated_list import PaginatedList
from canvasapi.peer_review import PeerReview
from canvasapi.util import combine_kwargs


class Submission(CanvasObject):
    def __init__(self, requester, attributes):
        super(Submission, self).__init__(requester, attributes)

        self.attachments = [
            File(requester, attachment)
            for attachment in attributes.get("attachments", [])
        ]

    def __str__(self):
        return "{}-{}".format(self.assignment_id, self.user_id)

    def get_submission_peer_reviews(self, **kwargs):
        """
        Get a list of all Peer Reviews this submission.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:submission_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.peer_review.PeerReview`
        """
        return PaginatedList(
            PeerReview,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/submissions/{}/peer_reviews".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )


class GroupedSubmission(CanvasObject):
    def __init__(self, requester, attributes):
        super(GroupedSubmission, self).__init__(requester, attributes)

        try:
            self.submissions = [
                Submission(requester, submission)
                for submission in attributes["submissions"]
            ]
        except KeyError:
            self.submissions = list()

    def __str__(self):
        return "{} submission(s) for User #{}".format(
            len(self.submissions), self.user_id
        )
