from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.util import combine_kwargs, normalize_bool, obj_or_id


class Section(CanvasObject):
    def __str__(self):
        return "{} - {} ({})".format(self.name, self.course_id, self.id)

    def get_assignment_override(self, assignment):
        """
        Return override for the specified assignment for this section.

        :param assignment: The assignment to get an override for
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :calls: `GET /api/v1/sections/:course_section_id/assignments/:assignment_id/override \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.section_alias>`_

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import Assignment, AssignmentOverride

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            "GET", "sections/{}/assignments/{}/override".format(self.id, assignment_id)
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return AssignmentOverride(self._requester, response_json)

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments for the current user.

        :calls: `GET /api/v1/sections/:section_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            "GET",
            "sections/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/sections/:section_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        is_grouped = kwargs.get("grouped", False)

        if normalize_bool(is_grouped, "grouped"):
            cls = GroupedSubmission
        else:
            cls = Submission

        return PaginatedList(
            cls,
            self._requester,
            "GET",
            "sections/{}/students/submissions".format(self.id),
            {"section_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )
