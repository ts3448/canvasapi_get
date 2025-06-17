from canvasapi.canvas_object import CanvasObject
from canvasapi.notification_preference import NotificationPreference
from canvasapi.util import combine_kwargs


class CommunicationChannel(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.address, self.id)

    def get_preference(self, notification, **kwargs):
        """
        Fetch the preference for the given notification for the given
        communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/ \
                :communication_channel_id/notification_preferences/:notification \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.show>`_

        :param notification: The name of the notification.
        :type notification: str
        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        response = self._requester.request(
            "GET",
            "users/{}/communication_channels/{}/notification_preferences/{}".format(
                self.user_id, self.id, notification
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        data = response.json()["notification_preferences"][0]
        return NotificationPreference(self._requester, data)

    def get_preference_categories(self, **kwargs):
        """
        Fetch all notification preference categories for the given communication
        channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/ \
                :communication_channel_id/notification_preference_categories \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.category_index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            "GET",
            "users/{}/communication_channels/{}/notification_preference_categories".format(
                self.user_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()["categories"]

    def get_preferences(self, **kwargs):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:communication_channel_id/ \
                notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            "GET",
            "users/{}/communication_channels/{}/notification_preferences".format(
                self.user_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()["notification_preferences"]
