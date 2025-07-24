# Notification Preferences

# Notification Preferences API



API for managing notification preferences

### A NotificationPreference object looks like:

```
{
  "href": "https://canvas.instructure.com/users/1/communication_channels/email/student@example.edu/notification_preferences/new_announcement",
  // The notification this preference belongs to
  "notification": "new_announcement",
  // The category of that notification
  "category": "announcement",
  // How often to send notifications to this communication channel for the given
  // notification. Possible values are 'immediately', 'daily', 'weekly', and
  // 'never'
  "frequency": "daily"
}
```

## [List preferences](#method.notification_preferences.index) [NotificationPreferencesController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### GET /api/v1/users/:user\_id/communication\_channels/:communication\_channel\_id/notification\_preferences

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels/:communication_channel_id/notification_preferences`

### GET /api/v1/users/:user\_id/communication\_channels/:type/:address/notification\_preferences

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels/:type/:address/notification_preferences`

Fetch all preferences for the given communication channel

Returns a list of
[NotificationPreference](notification_preferences.html#NotificationPreference)
objects

## [List of preference categories](#method.notification_preferences.category_index) [NotificationPreferencesController#category\_index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### GET /api/v1/users/:user\_id/communication\_channels/:communication\_channel\_id/notification\_preference\_categories

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels/:communication_channel_id/notification_preference_categories`

Fetch all notification preference categories for the given communication channel

## [Get a preference](#method.notification_preferences.show) [NotificationPreferencesController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### GET /api/v1/users/:user\_id/communication\_channels/:communication\_channel\_id/notification\_preferences/:notification

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels/:communication_channel_id/notification_preferences/:notification`

### GET /api/v1/users/:user\_id/communication\_channels/:type/:address/notification\_preferences/:notification

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels/:type/:address/notification_preferences/:notification`

Fetch the preference for the given notification for the given communication channel

Returns a
[NotificationPreference](notification_preferences.html#NotificationPreference)
object

## [Update a preference](#method.notification_preferences.update) [NotificationPreferencesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### PUT /api/v1/users/self/communication\_channels/:communication\_channel\_id/notification\_preferences/:notification

**Scope:** 
`url:PUT|/api/v1/users/self/communication_channels/:communication_channel_id/notification_preferences/:notification`

### PUT /api/v1/users/self/communication\_channels/:type/:address/notification\_preferences/:notification

**Scope:** 
`url:PUT|/api/v1/users/self/communication_channels/:type/:address/notification_preferences/:notification`

Change the preference for a single notification for a single communication channel

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| notification\_preferences[frequency] | Required | string | The desired frequency for this notification |

## [Update preferences by category](#method.notification_preferences.update_preferences_by_category) [NotificationPreferencesController#update\_preferences\_by\_category](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### PUT /api/v1/users/self/communication\_channels/:communication\_channel\_id/notification\_preference\_categories/:category

**Scope:** 
`url:PUT|/api/v1/users/self/communication_channels/:communication_channel_id/notification_preference_categories/:category`

Change the preferences for multiple notifications based on the category for a single communication channel

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| category |  | string | The name of the category. Must be parameterized (e.g. The category âCourse Contentâ should be âcourse\_contentâ) |
| notification\_preferences[frequency] | Required | string | The desired frequency for each notification in the category |

## [Update multiple preferences](#method.notification_preferences.update_all) [NotificationPreferencesController#update\_all](https://github.com/instructure/canvas-lms/blob/master/app/controllers/notification_preferences_controller.rb)

### PUT /api/v1/users/self/communication\_channels/:communication\_channel\_id/notification\_preferences

**Scope:** 
`url:PUT|/api/v1/users/self/communication_channels/:communication_channel_id/notification_preferences`

### PUT /api/v1/users/self/communication\_channels/:type/:address/notification\_preferences

**Scope:** 
`url:PUT|/api/v1/users/self/communication_channels/:type/:address/notification_preferences`

Change the preferences for multiple notifications for a single communication channel at once

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| notification\_preferences[<X>][frequency] | Required | string | The desired frequency for <X> notification |