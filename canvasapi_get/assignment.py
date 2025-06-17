from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.grade_change_log import GradeChangeEvent
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.peer_review import PeerReview
from canvasapi_get.submission import Submission
from canvasapi_get.user import User, UserDisplay
from canvasapi_get.util import combine_kwargs, obj_or_id


class Assignment(CanvasObject):
    def __init__(self, requester, attributes):
        super(Assignment, self).__init__(requester, attributes)

        if "overrides" in attributes:
            self.overrides = [
                AssignmentOverride(requester, override)
                for override in attributes["overrides"]
            ]

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_grade_change_events(self, **kwargs):
        """
        Returns the grade change events for the assignment.

        :calls: `/api/v1/audit/grade_change/assignments/:assignment_id \
        <https://canvas.instructure.com/doc/api/grade_change_log.html#method.grade_change_audit_api.for_assignment>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.grade_change_log.GradeChangeEvent`
        """

        return PaginatedList(
            GradeChangeEvent,
            self._requester,
            "GET",
            "audit/grade_change/assignments/{}".format(self.id),
            _root="events",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_gradeable_students(self, **kwargs):
        """
        List students eligible to submit the assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.user.UserDisplay`
        """
        return PaginatedList(
            UserDisplay,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/gradeable_students".format(
                self.course_id, self.id
            ),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_override(self, override, **kwargs):
        """
        Get a single assignment override with the given override id.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.show>`_

        :param override: The object or ID of the override to get
        :type override: :class:`canvasapi_get.assignment.AssignmentOverride` or int

        :rtype: :class:`canvasapi_get.assignment.AssignmentOverride`
        """
        override_id = obj_or_id(override, "override", (AssignmentOverride,))

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/overrides/{}".format(
                self.course_id, self.id, override_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def get_overrides(self, **kwargs):
        """
        Get a paginated list of overrides for this assignment that target
        sections/groups/students visible to the current user.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.assignment.AssignmentOverride`
        """
        return PaginatedList(
            AssignmentOverride,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/overrides".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_peer_reviews(self, **kwargs):
        """
        Get a list of all Peer Reviews for this assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.peer_review.PeerReview`
        """
        return PaginatedList(
            PeerReview,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/peer_reviews".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_provisional_grades_status(self, student_id, **kwargs):
        """
        Tell whether the student's submission needs one or more provisional grades.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/
            status \
        <https://canvas.instructure.com/doc/api/all_resources.html#method.provisional_grades.status>`_

        :param student_id: The object or ID of the related student
        :type student_id: :class:`canvasapi_get.user.User` or int

        :rtype: bool
        """
        kwargs["student_id"] = obj_or_id(student_id, "student_id", (User,))
        request = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/provisional_grades/status".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        request_json = request.json()

        return request_json.get("needs_provisional_grade")

    def get_students_selected_for_moderation(self, **kwargs):
        """
        Get a list of students selected for moderation.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students \
        <https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.user.User`
        """
        return PaginatedList(
            User,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/moderated_students".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_submission(self, user, **kwargs):
        """
        Get a single submission, based on user id.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi_get.user.User` or int

        :rtype: :class:`canvasapi_get.submission.Submission`
        """
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/submissions/{}".format(
                self.course_id, self.id, user_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)

        return Submission(self._requester, response_json)

    def get_submissions(self, **kwargs):
        """
        Get all existing submissions for this assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.submission.Submission`
        """
        return PaginatedList(
            Submission,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/submissions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def select_students_for_moderation(self, **kwargs):
        """
        Select student(s) for moderation.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/moderated_students \
        <https://canvas.instructure.com/doc/api/moderated_grading.html#method.moderation_set.create>`_

        :returns: The list of users that were selected
        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.user.User`
        """
        return PaginatedList(
            User,
            self._requester,
            "POST",
            "courses/{}/assignments/{}/moderated_students".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def show_provisonal_grades_for_student(self, anonymous_id, **kwargs):
        """
        :call: `GET /api/v1/courses/:course_id/assignments/:assignment_id/
            anonymous_provisional_grades/status \
        <https://canvas.instructure.com/doc/api/all_resources.html#method.anonymous_provisional_grades.status>`_

        :param anonymous_id: The ID of the student to show the status for
        :type anonymous_id: :class:`canvasapi_get.user.User` or int

        :rtype: dict
        """

        kwargs["anonymous_id"] = obj_or_id(anonymous_id, "anonymous_id", (User,))

        request = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/anonymous_provisional_grades/status".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return request.json().get("needs_provisional_grade")


class AssignmentExtension(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.assignment_id, self.user_id)


class AssignmentGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class AssignmentOverride(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)
