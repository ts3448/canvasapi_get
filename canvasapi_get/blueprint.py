from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class BlueprintTemplate(CanvasObject):
    def __str__(self):
        return "{}".format(self.id)

    def get_associated_courses(self, **kwargs):
        """
        Return a list of courses associated with the given blueprint.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id/ \
        associated_courses \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.associated_courses>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.course.Course`
        """
        from canvasapi.course import Course

        return PaginatedList(
            Course,
            self._requester,
            "GET",
            "courses/{}/blueprint_templates/{}/associated_courses".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_unsynced_changes(self, **kwargs):
        """
        Return changes made to associated courses of a blueprint course.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id/unsynced_changes \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses\
        /master_templates.unsynced_changes>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.blueprint.ChangeRecord`
        """

        return PaginatedList(
            ChangeRecord,
            self._requester,
            "GET",
            "courses/{}/blueprint_templates/{}/unsynced_changes".format(
                self.course_id, self.id
            ),
            kwargs=combine_kwargs(**kwargs),
        )

    def list_blueprint_migrations(self, **kwargs):
        """
        Return a paginated list of migrations for the template.

        :calls: `GET api/v1/courses/:course_id/blueprint_templates/:template_id/migrations \
         <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
         master_courses/master_templates.migrations_index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.blueprint.BlueprintMigration`
        """

        return PaginatedList(
            BlueprintMigration,
            self._requester,
            "GET",
            "courses/{}/blueprint_templates/{}/migrations".format(
                self.course_id, self.id
            ),
            {"course_id": self.course_id},
            kwargs=combine_kwargs(**kwargs),
        )

    def show_blueprint_migration(self, migration, **kwargs):
        """
        Return the status of a blueprint migration.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id\
        /migrations/:id\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/\
        master_templates.migrations_show>`_

        :param migration: migration id or object
        :type migration: int or :class:`canvasapi.blueprint.BlueprintMigration`

        :rtype: :class:`canvasapi.blueprint.BlueprintMigration`
        """

        migration_id = obj_or_id(migration, "migration", (BlueprintMigration,))
        response = self._requester.request(
            "GET",
            "courses/{}/blueprint_templates/{}/migrations/{}".format(
                self.course_id, self.id, migration_id
            ),
            kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})
        return BlueprintMigration(self._requester, response_json)


class BlueprintMigration(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.id, self.template_id)

    def get_details(self, **kwargs):
        """
        Return the changes that were made in a blueprint migration.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id\
        /migrations/:id/details\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.migration_details>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.blueprint.ChangeRecord`
        """

        return PaginatedList(
            ChangeRecord,
            self._requester,
            "GET",
            "courses/{}/blueprint_templates/{}/migrations/{}/details".format(
                self.course_id, self.template_id, self.id
            ),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_import_details(self, **kwargs):
        """
        Return changes that were made to a course with a blueprint.

        :calls: `GET /api/v1/courses/:course_id/blueprint_subscriptions/\
        :subscription_id/migrations/:id/details\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.import_details>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.blueprint.ChangeRecord`
        """

        return PaginatedList(
            ChangeRecord,
            self._requester,
            "GET",
            "courses/{}/blueprint_subscriptions/{}/migrations/{}/details".format(
                self.course_id, self.subscription_id, self.id
            ),
            kwargs=combine_kwargs(**kwargs),
        )


class ChangeRecord(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.asset_id, self.asset_name)


class BlueprintSubscription(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.id, self.template_id)

    def list_blueprint_imports(self, **kwargs):
        """
        Return a list of migrations imported into a course associated with a blueprint.

        :calls: `GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/\
        migrations\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.imports_index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.blueprint.BlueprintMigration`
        """

        return PaginatedList(
            BlueprintMigration,
            self._requester,
            "GET",
            "courses/{}/blueprint_subscriptions/{}/migrations".format(
                self.course_id, self.id
            ),
            {"course_id": self.id},
            kwargs=combine_kwargs(**kwargs),
        )

    def show_blueprint_import(self, migration, **kwargs):
        """
        Return the status of an import into a course associated with a blueprint.

        :calls: `GET /api/v1/courses/:course_id/blueprint_subscriptions/:subscription_id/\
        migrations/:id\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.imports_show>`_

        :param migration: migration id or object
        :type migration: int or :class:`canvasapi.blueprint.BlueprintMigration`

        :rtype: :class:`canvasapi.blueprint.BlueprintMigration`
        """

        migration_id = obj_or_id(migration, "migration", (BlueprintMigration,))
        response = self._requester.request(
            "GET",
            "courses/{}/blueprint_subscriptions/{}/migrations/{}".format(
                self.course_id, self.id, migration_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})
        return BlueprintMigration(self._requester, response_json)
