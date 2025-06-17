from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.collaboration import Collaboration
from canvasapi_get.discussion_topic import DiscussionTopic
from canvasapi_get.folder import Folder
from canvasapi_get.license import License
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.tab import Tab
from canvasapi_get.util import combine_kwargs, obj_or_id


class Group(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_activity_stream_summary(self, **kwargs):
        """
        Return a summary of the current user's global activity stream.

        :calls: `GET /api/v1/groups/:group_id/activity_stream/summary \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.activity_stream_summary>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "groups/{}/activity_stream/summary".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_assignment_override(self, assignment):
        """
        Return override for the specified assignment for this group.

        :param assignment: The assignment to get an override for
        :type assignment: :class:`canvasapi_get.assignment.Assignment` or int

        :calls: `GET /api/v1/groups/:group_id/assignments/:assignment_id/override \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.group_alias>`_

        :rtype: :class:`canvasapi_get.assignment.AssignmentOverride`
        """
        from canvasapi_get.assignment import Assignment, AssignmentOverride

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            "GET", "groups/{}/assignments/{}/override".format(self.id, assignment_id)
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return AssignmentOverride(self._requester, response_json)

    def get_collaborations(self, **kwargs):
        """
        Return a list of collaborations for a given course ID.

        :calls: `GET /api/v1/groups/:group_id/collaborations \
        <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index>`_

        :rtype: :class:`canvasapi_get.collaboration.Collaboration`
        """
        return PaginatedList(
            Collaboration,
            self._requester,
            "GET",
            "groups/{}/collaborations".format(self.id),
            _root="collaborations",
            kwargs=combine_kwargs(**kwargs),
        )

    def get_content_export(self, content_export, **kwargs):
        """
        Return information about a single content export.

        :calls: `GET /api/v1/groups/:group_id/content_exports/:id\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show>`_

        :param content_export: The object or ID of the content export to show.
        :type content_export: int or :class:`canvasapi_get.content_export.ContentExport`

        :rtype: :class:`canvasapi_get.content_export.ContentExport`
        """
        from canvasapi_get.content_export import ContentExport

        export_id = obj_or_id(content_export, "content_export", (ContentExport,))

        response = self._requester.request(
            "GET",
            "groups/{}/content_exports/{}".format(self.id, export_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return ContentExport(self._requester, response.json())

    def get_content_exports(self, **kwargs):
        """
        Return a paginated list of the past and pending content export jobs for a group.

        :calls: `GET /api/v1/groups/:group_id/content_exports\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.content_export.ContentExport`
        """
        from canvasapi_get.content_export import ContentExport

        return PaginatedList(
            ContentExport,
            self._requester,
            "GET",
            "groups/{}/content_exports".format(self.id),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_content_migration(self, content_migration, **kwargs):
        """
        Retrive a content migration by its ID

        :calls: `GET /api/v1/groups/:group_id/content_migrations/:id \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show>`_

        :param content_migration: The object or ID of the content migration to retrieve.
        :type content_migration: int, str or :class:`canvasapi_get.content_migration.ContentMigration`

        :rtype: :class:`canvasapi_get.content_migration.ContentMigration`
        """
        from canvasapi_get.content_migration import ContentMigration

        migration_id = obj_or_id(
            content_migration, "content_migration", (ContentMigration,)
        )

        response = self._requester.request(
            "GET",
            "groups/{}/content_migrations/{}".format(self.id, migration_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"group_id": self.id})

        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs):
        """
        List content migrations that the current account can view or manage.

        :calls: `GET /api/v1/groups/:group_id/content_migrations/ \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.content_migration.ContentMigration`
        """
        from canvasapi_get.content_migration import ContentMigration

        return PaginatedList(
            ContentMigration,
            self._requester,
            "GET",
            "groups/{}/content_migrations".format(self.id),
            {"group_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_discussion_topic(self, topic, **kwargs):
        """
        Return data on an individual discussion topic.

        :calls: `GET /api/v1/groups/:group_id/discussion_topics/:topic_id \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi_get.discussion_topic.DiscussionTopic` or int

        :rtype: :class:`canvasapi_get.discussion_topic.DiscussionTopic`
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            "GET",
            "groups/{}/discussion_topics/{}".format(self.id, topic_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"group_id": self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_discussion_topics(self, **kwargs):
        """
        Returns the paginated list of discussion topics for this course or group.

        :calls: `GET /api/v1/groups/:group_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.discussion_topic.DiscussionTopic`
        """

        return PaginatedList(
            DiscussionTopic,
            self._requester,
            "GET",
            "groups/{}/discussion_topics".format(self.id),
            {"group_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_external_feeds(self):
        """
        Returns the list of External Feeds this group.

        :calls: `GET /api/v1/groups/:group_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.external_feed.ExternalFeed`
        """
        from canvasapi_get.external_feed import ExternalFeed

        return PaginatedList(
            ExternalFeed,
            self._requester,
            "GET",
            "groups/{}/external_feeds".format(self.id),
        )

    def get_file(self, file, **kwargs):
        """
        Return the standard attachment json object for a file.

        :calls: `GET /api/v1/groups/:group_id/files/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

        :param file: The object or ID of the file to retrieve.
        :type file: :class:`canvasapi_get.file.File` or int

        :rtype: :class:`canvasapi_get.file.File`
        """
        from canvasapi_get.file import File

        file_id = obj_or_id(file, "file", (File,))

        response = self._requester.request(
            "GET",
            "groups/{}/files/{}".format(self.id, file_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return File(self._requester, response.json())

    def get_file_quota(self, **kwargs):
        """
        Returns the total and used storage quota for the group.

        :calls: `GET /api/v1/groups/:group_id/files/quota \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_quota>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "groups/{}/files/quota".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_files(self, **kwargs):
        """
        Returns the paginated list of files for the group.

        :calls: `GET /api/v1/groups/:group_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.file.File`
        """
        from canvasapi_get.file import File

        return PaginatedList(
            File,
            self._requester,
            "GET",
            "groups/{}/files".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_folder(self, folder, **kwargs):
        """
        Returns the details for a group's folder

        :calls: `GET /api/v1/groups/:group_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi_get.folder.Folder` or int

        :rtype: :class:`canvasapi_get.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self._requester.request(
            "GET",
            "groups/{}/folders/{}".format(self.id, folder_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Folder(self._requester, response.json())

    def get_folders(self):
        """
        Returns the paginated list of all folders for the given group. This will be returned as a
        flat list containing all subfolders as well.

        :calls: `GET /api/v1/groups/:group_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.folder.Folder`
        """
        return PaginatedList(
            Folder, self._requester, "GET", "groups/{}/folders".format(self.id)
        )

    def get_full_discussion_topic(self, topic, **kwargs):
        """
        Return a cached structure of the discussion topic.

        :calls: `GET /api/v1/groups/:group_id/discussion_topics/:topic_id/view \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi_get.discussion_topic.DiscussionTopic` or int

        :rtype: dict
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            "GET",
            "groups/{}/discussion_topics/{}/view".format(self.id, topic_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_licenses(self, **kwargs):
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the group scope

        :calls: `GET /api/v1/groups/:group_id/content_licenses \
        <https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.license.License`
        """

        return PaginatedList(
            License,
            self._requester,
            "GET",
            "groups/{}/content_licenses".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_membership(self, user, membership_type, **kwargs):
        """
        List users in a group.

        :calls: `GET /api/v1/groups/:group_id/users/:user_id \
            <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

            or `GET /api/v1/groups/:group_id/memberships/:membership_id
            <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

        :param user: list of user ids
        :type user: :class:`canvasapi_get.user.User` or int

        :rtype: :class:`canvasapi_get.group.GroupMembership`
        """
        from canvasapi_get.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "groups/{}/{}/{}".format(self.id, membership_type, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return GroupMembership(self._requester, response.json())

    def get_memberships(self, **kwargs):
        """
        List users in a group.

        :calls: `GET /api/v1/groups/:group_id/memberships \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.group.GroupMembership`
        """
        return PaginatedList(
            GroupMembership,
            self._requester,
            "GET",
            "groups/{}/memberships".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_migration_systems(self, **kwargs):
        """
        Return a list of migration systems.

        :calls: `GET /api/v1/groups/:group_id/content_migrations/migrators \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.content_migration.Migrator`
        """
        from canvasapi_get.content_migration import Migrator

        return PaginatedList(
            Migrator,
            self._requester,
            "GET",
            "groups/{}/content_migrations/migrators".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_page(self, url, **kwargs):
        """
        Retrieve the contents of a wiki page.

        :calls: `GET /api/v1/groups/:group_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_

        :param url: The url for the page.
        :type url: str
        :returns: The specified page.
        :rtype: :class:`canvasapi_get.groups.Group`
        """
        from canvasapi_get.course import Page

        response = self._requester.request(
            "GET",
            "groups/{}/pages/{}".format(self.id, url),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"group_id": self.id})

        return Page(self._requester, page_json)

    def get_pages(self, **kwargs):
        """
        List the wiki pages associated with a group.

        :calls: `GET /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.page.Page`
        """
        from canvasapi_get.course import Page

        return PaginatedList(
            Page,
            self._requester,
            "GET",
            "groups/{}/pages".format(self.id),
            {"group_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_tabs(self, **kwargs):
        """
        List available tabs for a group.
        Returns a list of navigation tabs available in the current context.

        :calls: `GET /api/v1/groups/:group_id/tabs \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.tab.Tab`
        """
        return PaginatedList(
            Tab,
            self._requester,
            "GET",
            "groups/{}/tabs".format(self.id),
            {"group_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_users(self, **kwargs):
        """
        List users in a group.

        :calls: `GET /api/v1/groups/:group_id/users \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.users>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.user.User`
        """
        from canvasapi_get.user import User

        return PaginatedList(
            User,
            self._requester,
            "GET",
            "groups/{}/users".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def resolve_path(self, full_path=None, **kwargs):
        """
        Returns the paginated list of all of the folders in the given
        path starting at the group root folder. Returns root folder if called
        with no arguments.

        :calls: `GET /api/v1/groups/group_id/folders/by_path/*full_path \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path>`_

        :param full_path: Full path to resolve, relative to group root.
        :type full_path: string

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.folder.Folder`
        """

        if full_path:
            return PaginatedList(
                Folder,
                self._requester,
                "GET",
                "groups/{0}/folders/by_path/{1}".format(self.id, full_path),
                _kwargs=combine_kwargs(**kwargs),
            )
        else:
            return PaginatedList(
                Folder,
                self._requester,
                "GET",
                "groups/{0}/folders/by_path".format(self.id),
                _kwargs=combine_kwargs(**kwargs),
            )

    def show_front_page(self, **kwargs):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`canvasapi_get.group.Group`
        """
        from canvasapi_get.course import Page

        response = self._requester.request(
            "GET",
            "groups/{}/front_page".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"group_id": self.id})

        return Page(self._requester, page_json)


class GroupMembership(CanvasObject):
    def __str__(self):
        return "{} - {} ({})".format(self.user_id, self.group_id, self.id)


class GroupCategory(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def get_groups(self):
        """
        List groups in group category.

        :calls: `GET /api/v1/group_categories/:group_category_id/groups \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.group.Group`
        """
        return PaginatedList(
            Group, self._requester, "GET", "group_categories/{}/groups".format(self.id)
        )

    def get_users(self, **kwargs):
        """
        List users in group category.

        :calls: `GET /api/v1/group_categories/:group_category_id/users \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users>`_

        :rtype: :class:`canvasapi_get.paginated_list.PaginatedList` of
            :class:`canvasapi_get.user.User`
        """
        from canvasapi_get.user import User

        return PaginatedList(
            User,
            self._requester,
            "GET",
            "group_categories/{}/users".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
