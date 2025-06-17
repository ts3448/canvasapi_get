from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class Outcome(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.url)


class OutcomeLink(CanvasObject):
    def __str__(self):
        return "Group {} with Outcome {} ({})".format(
            self.outcome_group, self.outcome, self.url
        )

    def context_ref(self):
        if self.context_type == "Course":
            return "courses/{}".format(self.context_id)
        elif self.context_type == "Account":
            return "accounts/{}".format(self.context_id)
        return None

    def get_outcome(self, **kwargs):
        """
        Return the linked outcome

        :calls: `GET /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show>`_

        :returns: Outcome object that was in the OutcomeLink
        :rtype: :class:`canvasapi.outcome.Outcome`
        """
        oid = self.outcome["id"]
        response = self._requester.request(
            "GET", "outcomes/{}".format(oid), _kwargs=combine_kwargs(**kwargs)
        )

        return Outcome(self._requester, response.json())

    def get_outcome_group(self, **kwargs):
        """
        Return the linked outcome group

        :calls: `GET /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :returns: Linked outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        ogid = self.outcome_group["id"]
        response = self._requester.request(
            "GET",
            "{}/outcome_groups/{}".format(self.context_ref(), ogid),
            _kwargs=combine_kwargs(**kwargs),
        )

        return OutcomeGroup(self._requester, response.json())


class OutcomeGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def context_ref(self):
        if self.context_type == "Course":
            return "courses/{}".format(self.context_id)
        elif self.context_type == "Account":
            return "accounts/{}".format(self.context_id)
        elif self.context_type is None:
            return "global"
        return None

    def get_linked_outcomes(self, **kwargs):
        """
        List linked outcomes.

        :calls: `GET /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_

        :returns: Paginated List of Outcomes linked to the group.
        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.outcome.OutcomeLink`
        """
        return PaginatedList(
            OutcomeLink,
            self._requester,
            "GET",
            "{}/outcome_groups/{}/outcomes".format(self.context_ref(), self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_subgroups(self, **kwargs):
        """
        List subgroups.

        :calls: `GET /api/v1/global/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_

        :returns: Paginated List of OutcomeGroups linked to the current group.
        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.outcome.OutcomeGroup`
        """
        return PaginatedList(
            OutcomeGroup,
            self._requester,
            "GET",
            "{}/outcome_groups/{}/subgroups".format(self.context_ref(), self.id),
            {"context_type": self.context_type, "context_id": self.context_id},
            _kwargs=combine_kwargs(**kwargs),
        )


class OutcomeResult(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.id, self.score)
