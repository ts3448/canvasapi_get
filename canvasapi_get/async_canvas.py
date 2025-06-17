"""Async Canvas API client with concurrent pagination support."""

import warnings
from collections.abc import AsyncIterable

from canvasapi_get.account import Account
from canvasapi_get.account_calendar import AccountCalendar
from canvasapi_get.appointment_group import AppointmentGroup
from canvasapi_get.async_paginated_list import AsyncPaginatedList
from canvasapi_get.async_requester import AsyncRequester
from canvasapi_get.calendar_event import CalendarEvent
from canvasapi_get.comm_message import CommMessage
from canvasapi_get.conversation import Conversation
from canvasapi_get.course import Course, CourseNickname
from canvasapi_get.course_epub_export import CourseEpubExport
from canvasapi_get.discussion_topic import DiscussionTopic
from canvasapi_get.exceptions import RequiredFieldMissing
from canvasapi_get.folder import Folder
from canvasapi_get.group import Group, GroupCategory
from canvasapi_get.jwt import JWT
from canvasapi_get.outcome import Outcome, OutcomeGroup
from canvasapi_get.planner import PlannerNote, PlannerOverride
from canvasapi_get.poll import Poll
from canvasapi_get.progress import Progress
from canvasapi_get.section import Section
from canvasapi_get.todo import Todo
from canvasapi_get.user import User
from canvasapi_get.util import combine_kwargs, get_institution_url, obj_or_id


class AsyncCanvas:
    """
    Async Canvas API client with concurrent pagination support.

    This class provides async methods for accessing Canvas API endpoints
    with intelligent concurrent pagination that respects rate limits.
    """

    def __init__(
        self,
        base_url: str,
        access_token: str,
        base_concurrency: int = 3,
        max_concurrency: int = 10,
    ):
        """
        Initialize the async Canvas client.

        Args:
            base_url: The base URL of the Canvas instance's API.
            access_token: The API key to authenticate requests with.
            base_concurrency: Default number of concurrent requests.
            max_concurrency: Maximum number of concurrent requests.

        Raises:
            ValueError: If base_url contains API version or is invalid.
        """
        if "api/v1" in base_url:
            raise ValueError(
                "`base_url` should not specify an API version. Remove trailing /api/v1/"
            )

        if "http://" in base_url:
            warnings.warn(
                "Canvas may respond unexpectedly when making requests to HTTP "
                "URLs. If possible, please use HTTPS.",
                UserWarning,
            )

        if not base_url.strip():
            warnings.warn(
                "Canvas needs a valid URL, please provide a non-blank `base_url`.",
                UserWarning,
            )

        if "://" not in base_url:
            warnings.warn(
                "An invalid `base_url` for the Canvas API Instance was used. "
                "Please provide a valid HTTP or HTTPS URL if possible.",
                UserWarning,
            )

        # Clean inputs
        access_token = access_token.strip()
        base_url = get_institution_url(base_url)

        self.__requester = AsyncRequester(
            base_url,
            access_token,
            base_concurrency=base_concurrency,
            max_concurrency=max_concurrency,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        await self.__requester.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.__requester.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self.__requester.close()

    async def get_accounts(self, **kwargs) -> AsyncIterable[Account]:
        """
        List accounts that the current user can view or manage.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Account objects.
        """
        paginated_list = AsyncPaginatedList(
            Account,
            self.__requester,
            "GET",
            "accounts",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_account_calendars(self, **kwargs) -> AsyncIterable[AccountCalendar]:
        """
        Returns a paginated list of account calendars available to the user.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of AccountCalendar objects.
        """
        paginated_list = AsyncPaginatedList(
            AccountCalendar,
            self.__requester,
            "GET",
            "account_calendars",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_announcements(
        self, context_codes: list, **kwargs
    ) -> AsyncIterable[DiscussionTopic]:
        """
        List announcements.

        Args:
            context_codes: Course ID(s) or Course objects to request announcements from.
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of DiscussionTopic objects.

        Raises:
            RequiredFieldMissing: If context_codes is empty or invalid.
        """
        if type(context_codes) is not list or len(context_codes) == 0:
            raise RequiredFieldMissing("context_codes need to be passed as a list")

        if isinstance(context_codes[0], str) and "course_" in context_codes[0]:
            kwargs["context_codes"] = context_codes
        else:
            course_ids = [
                obj_or_id(course_id, "context_codes", (Course,))
                for course_id in context_codes
            ]
            kwargs["context_codes"] = [
                f"course_{course_id}" for course_id in course_ids
            ]

        paginated_list = AsyncPaginatedList(
            DiscussionTopic,
            self.__requester,
            "GET",
            "announcements",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_appointment_groups(self, **kwargs) -> AsyncIterable[AppointmentGroup]:
        """
        List appointment groups.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of AppointmentGroup objects.
        """
        paginated_list = AsyncPaginatedList(
            AppointmentGroup,
            self.__requester,
            "GET",
            "appointment_groups",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_calendar_events(self, **kwargs) -> AsyncIterable[CalendarEvent]:
        """
        List calendar events.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of CalendarEvent objects.
        """
        paginated_list = AsyncPaginatedList(
            CalendarEvent,
            self.__requester,
            "GET",
            "calendar_events",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_comm_messages(
        self, user: User | int, **kwargs
    ) -> AsyncIterable[CommMessage]:
        """
        Retrieve a paginated list of messages sent to a user.

        Args:
            user: The User object or user ID.
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of CommMessage objects.
        """
        kwargs["user_id"] = obj_or_id(user, "user", (User,))

        paginated_list = AsyncPaginatedList(
            CommMessage,
            self.__requester,
            "GET",
            "comm_messages",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_conversations(self, **kwargs) -> AsyncIterable[Conversation]:
        """
        Return list of conversations for the current user, most recent ones first.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Conversation objects.
        """
        paginated_list = AsyncPaginatedList(
            Conversation,
            self.__requester,
            "GET",
            "conversations",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_course_accounts(self, **kwargs) -> AsyncIterable[Account]:
        """
        List accounts that the current user can view through their admin course enrollments.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Account objects.
        """
        paginated_list = AsyncPaginatedList(
            Account,
            self.__requester,
            "GET",
            "course_accounts",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_course_nicknames(self, **kwargs) -> AsyncIterable[CourseNickname]:
        """
        Return all course nicknames set by the current account.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of CourseNickname objects.
        """
        paginated_list = AsyncPaginatedList(
            CourseNickname,
            self.__requester,
            "GET",
            "users/self/course_nicknames",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_courses(self, **kwargs) -> AsyncIterable[Course]:
        """
        Return a list of active courses for the current user.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Course objects.
        """
        paginated_list = AsyncPaginatedList(
            Course,
            self.__requester,
            "GET",
            "courses",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_epub_exports(self, **kwargs) -> AsyncIterable[CourseEpubExport]:
        """
        Return a list of epub exports for the associated course.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of CourseEpubExport objects.
        """
        paginated_list = AsyncPaginatedList(
            CourseEpubExport,
            self.__requester,
            "GET",
            "epub_exports",
            _root="courses",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_group_participants(
        self, appointment_group: AppointmentGroup | int, **kwargs
    ) -> AsyncIterable[Group]:
        """
        List student group participants in this appointment group.

        Args:
            appointment_group: The AppointmentGroup object or ID.
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Group objects.
        """
        appointment_group_id = obj_or_id(
            appointment_group, "appointment_group", (AppointmentGroup,)
        )

        paginated_list = AsyncPaginatedList(
            Group,
            self.__requester,
            "GET",
            f"appointment_groups/{appointment_group_id}/groups",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_planner_notes(self, **kwargs) -> AsyncIterable[PlannerNote]:
        """
        Retrieve the paginated list of planner notes.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of PlannerNote objects.
        """
        paginated_list = AsyncPaginatedList(
            PlannerNote,
            self.__requester,
            "GET",
            "planner_notes",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_planner_overrides(self, **kwargs) -> AsyncIterable[PlannerOverride]:
        """
        Retrieve a list of planner overrides for the current user.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of PlannerOverride objects.
        """
        paginated_list = AsyncPaginatedList(
            PlannerOverride,
            self.__requester,
            "GET",
            "planner/overrides",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_polls(self, **kwargs) -> AsyncIterable[Poll]:
        """
        Returns a paginated list of polls for the current user.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Poll objects.
        """
        paginated_list = AsyncPaginatedList(
            Poll,
            self.__requester,
            "GET",
            "polls",
            _root="polls",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_todo_items(self, **kwargs) -> AsyncIterable[Todo]:
        """
        Return the current user's list of todo items.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of Todo objects.
        """
        paginated_list = AsyncPaginatedList(
            Todo,
            self.__requester,
            "GET",
            "users/self/todo",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_user_participants(
        self, appointment_group: AppointmentGroup | int, **kwargs
    ) -> AsyncIterable[User]:
        """
        List user participants in this appointment group.

        Args:
            appointment_group: The AppointmentGroup object or ID.
            **kwargs: Additional parameters for the request.

        Returns:
            Async iterable of User objects.
        """
        appointment_group_id = obj_or_id(
            appointment_group, "appointment_group", (AppointmentGroup,)
        )

        paginated_list = AsyncPaginatedList(
            User,
            self.__requester,
            "GET",
            f"appointment_groups/{appointment_group_id}/users",
            **kwargs,
        )
        await paginated_list.fetch_all()
        return paginated_list

    async def get_rate_limit_stats(self) -> dict:
        """
        Get current rate limiting statistics.

        Returns:
            Dictionary containing rate limit and coordination statistics.
        """
        return await self.__requester.get_rate_limit_stats()

    async def reset_rate_limit_stats(self) -> None:
        """Reset rate limiting statistics to initial state."""
        await self.__requester.reset_rate_limit_stats()
