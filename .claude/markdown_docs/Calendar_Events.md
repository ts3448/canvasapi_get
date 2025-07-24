# Calendar Events

# Calendar Events API



API for creating, accessing and updating calendar events.

### A CalendarEvent object looks like:

```
{
  // The ID of the calendar event
  "id": 234,
  // The title of the calendar event
  "title": "Paintball Fight!",
  // The start timestamp of the event
  "start_at": "2012-07-19T15:00:00-06:00",
  // The end timestamp of the event
  "end_at": "2012-07-19T16:00:00-06:00",
  // The HTML description of the event
  "description": "<b>It's that time again!</b>",
  // The location name of the event
  "location_name": "Greendale Community College",
  // The address where the event is taking place
  "location_address": "Greendale, Colorado",
  // the context code of the calendar this event belongs to (course, group, user,
  // or account)
  "context_code": "course_123",
  // if specified, it indicates which calendar this event should be displayed on.
  // for example, a section-level event would have the course's context code here,
  // while the section's context code would be returned above)
  "effective_context_code": null,
  // the context name of the calendar this event belongs to (course, user or
  // group)
  "context_name": "Chemistry 101",
  // a comma-separated list of all calendar contexts this event is part of
  "all_context_codes": "course_123,course_456",
  // Current state of the event ('active', 'locked' or 'deleted') 'locked'
  // indicates that start_at/end_at cannot be changed (though the event could be
  // deleted). Normally only reservations or time slots with reservations are
  // locked (see the Appointment Groups API)
  "workflow_state": "active",
  // Whether this event should be displayed on the calendar. Only true for
  // course-level events with section-level child events.
  "hidden": false,
  // Normally null. If this is a reservation (see the Appointment Groups API), the
  // id will indicate the time slot it is for. If this is a section-level event,
  // this will be the course-level parent event.
  "parent_event_id": null,
  // The number of child_events. See child_events (and parent_event_id)
  "child_events_count": 0,
  // Included by default, but may be excluded (see include[] option). If this is a
  // time slot (see the Appointment Groups API) this will be a list of any
  // reservations. If this is a course-level event, this will be a list of
  // section-level events (if any)
  "child_events": null,
  // URL for this calendar event (to update, delete, etc.)
  "url": "https://example.com/api/v1/calendar_events/234",
  // URL for a user to view this event
  "html_url": "https://example.com/calendar?event_id=234&include_contexts=course_123",
  // The date of this event
  "all_day_date": "2012-07-19",
  // Boolean indicating whether this is an all-day event (midnight to midnight)
  "all_day": false,
  // When the calendar event was created
  "created_at": "2012-07-12T10:55:20-06:00",
  // When the calendar event was last updated
  "updated_at": "2012-07-12T10:55:20-06:00",
  // Various Appointment-Group-related fields.These fields are only pertinent to
  // time slots (appointments) and reservations of those time slots. See the
  // Appointment Groups API. The id of the appointment group
  "appointment_group_id": null,
  // The API URL of the appointment group
  "appointment_group_url": null,
  // If the event is a reservation, this a boolean indicating whether it is the
  // current user's reservation, or someone else's
  "own_reservation": false,
  // If the event is a time slot, the API URL for reserving it
  "reserve_url": null,
  // If the event is a time slot, a boolean indicating whether the user has
  // already made a reservation for it
  "reserved": false,
  // The type of participant to sign up for a slot: 'User' or 'Group'
  "participant_type": "User",
  // If the event is a time slot, this is the participant limit
  "participants_per_appointment": null,
  // If the event is a time slot and it has a participant limit, an integer
  // indicating how many slots are available
  "available_slots": null,
  // If the event is a user-level reservation, this will contain the user
  // participant JSON (refer to the Users API).
  "user": null,
  // If the event is a group-level reservation, this will contain the group
  // participant JSON (refer to the Groups API).
  "group": null,
  // Boolean indicating whether this has important dates.
  "important_dates": true,
  // Identifies the recurring event series this event may belong to.
  "series_uuid": null,
  // An iCalendar RRULE for defining how events in a recurring event series
  // repeat.
  "rrule": null,
  // Boolean indicating if is the first event in the series of recurring events.
  "series_head": null,
  // A natural language expression of how events occur in the series.
  "series_natural_language": "Daily 5 times",
  // Boolean indicating whether this has blackout date.
  "blackout_date": true
}
```

### An AssignmentEvent object looks like:

```
{
  // A synthetic ID for the assignment
  "id": "assignment_987",
  // The title of the assignment
  "title": "Essay",
  // The due_at timestamp of the assignment
  "start_at": "2012-07-19T23:59:00-06:00",
  // The due_at timestamp of the assignment
  "end_at": "2012-07-19T23:59:00-06:00",
  // The HTML description of the assignment
  "description": "<b>Write an essay. Whatever you want.</b>",
  // the context code of the (course) calendar this assignment belongs to
  "context_code": "course_123",
  // Current state of the assignment ('published' or 'deleted')
  "workflow_state": "published",
  // URL for this assignment (note that updating/deleting should be done via the
  // Assignments API)
  "url": "https://example.com/api/v1/calendar_events/assignment_987",
  // URL for a user to view this assignment
  "html_url": "http://example.com/courses/123/assignments/987",
  // The due date of this assignment
  "all_day_date": "2012-07-19",
  // Boolean indicating whether this is an all-day event (e.g. assignment due at
  // midnight)
  "all_day": true,
  // When the assignment was created
  "created_at": "2012-07-12T10:55:20-06:00",
  // When the assignment was last updated
  "updated_at": "2012-07-12T10:55:20-06:00",
  // The full assignment JSON data (See the Assignments API)
  "assignment": null,
  // The list of AssignmentOverrides that apply to this event (See the Assignments
  // API). This information is useful for determining which students or sections
  // this assignment-due event applies to.
  "assignment_overrides": null,
  // Boolean indicating whether this has important dates.
  "important_dates": true,
  // An iCalendar RRULE for defining how events in a recurring event series
  // repeat.
  "rrule": "FREQ=DAILY;INTERVAL=1;COUNT=5",
  // Trueif this is the first event in the series of recurring events.
  "series_head": null,
  // A natural language expression of how events occur in the series.
  "series_natural_language": "Daily 5 times"
}
```

## [List calendar events](#method.calendar_events_api.index) [CalendarEventsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### GET /api/v1/calendar\_events

**Scope:** 
`url:GET|/api/v1/calendar_events`

Retrieve the paginated list of calendar events or assignments for the current user

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| type |  | string | Defaults to âeventâ  Allowed values: `event`, `assignment`, `sub_assignment` |
| start\_date |  | Date | Only return events since the start\_date (inclusive). Defaults to today. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. |
| end\_date |  | Date | Only return events before the end\_date (inclusive). Defaults to start\_date. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. If end\_date is the same as start\_date, then only events on that day are returned. |
| undated |  | boolean | Defaults to false (dated events only). If true, only return undated events and ignore start\_date and end\_date. |
| all\_events |  | boolean | Defaults to false (uses start\_date, end\_date, and undated criteria). If true, all events are returned, ignoring start\_date, end\_date, and undated criteria. |
| context\_codes[] |  | string | List of context codes of courses, groups, users, or accounts whose events you want to see. If not specified, defaults to the current user (i.e personal calendar, no course/group events). Limited to 10 context codes, additional ones are ignored. The format of this field is the context type, followed by an underscore, followed by the context id. For example: course\_42 |
| excludes[] |  | Array | Array of attributes to exclude. Possible values are âdescriptionâ, âchild\_eventsâ and âassignmentâ |
| includes[] |  | Array | Array of optional attributes to include. Possible values are âweb\_conferenceâ and âseries\_natural\_languageâ |
| important\_dates |  | boolean | Defaults to false. If true, only events with important dates set to true will be returned. |
| blackout\_date |  | boolean | Defaults to false. If true, only events with blackout date set to true will be returned. |

Returns a list of
[CalendarEvent](calendar_events.html#CalendarEvent)
objects

## [List calendar events for a user](#method.calendar_events_api.user_index) [CalendarEventsApiController#user\_index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### GET /api/v1/users/:user\_id/calendar\_events

**Scope:** 
`url:GET|/api/v1/users/:user_id/calendar_events`

Retrieve the paginated list of calendar events or assignments for the specified user. To view calendar events for a user other than yourself, you must either be an observer of that user or an administrator.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| type |  | string | Defaults to âeventâ  Allowed values: `event`, `assignment` |
| start\_date |  | Date | Only return events since the start\_date (inclusive). Defaults to today. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. |
| end\_date |  | Date | Only return events before the end\_date (inclusive). Defaults to start\_date. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. If end\_date is the same as start\_date, then only events on that day are returned. |
| undated |  | boolean | Defaults to false (dated events only). If true, only return undated events and ignore start\_date and end\_date. |
| all\_events |  | boolean | Defaults to false (uses start\_date, end\_date, and undated criteria). If true, all events are returned, ignoring start\_date, end\_date, and undated criteria. |
| context\_codes[] |  | string | List of context codes of courses, groups, users, or accounts whose events you want to see. If not specified, defaults to the current user (i.e personal calendar, no course/group events). Limited to 10 context codes, additional ones are ignored. The format of this field is the context type, followed by an underscore, followed by the context id. For example: course\_42 |
| excludes[] |  | Array | Array of attributes to exclude. Possible values are âdescriptionâ, âchild\_eventsâ and âassignmentâ |
| submission\_types[] |  | Array | When type is âassignmentâ, specifies the allowable submission types for returned assignments. Ignored if type is not âassignmentâ or if exclude\_submission\_types is provided. |
| exclude\_submission\_types[] |  | Array | When type is âassignmentâ, specifies the submission types to be excluded from the returned assignments. Ignored if type is not âassignmentâ. |
| includes[] |  | Array | Array of optional attributes to include. Possible values are âweb\_conferenceâ and âseries\_natural\_languageâ |
| important\_dates |  | boolean | Defaults to false If true, only events with important dates set to true will be returned. |
| blackout\_date |  | boolean | Defaults to false If true, only events with blackout date set to true will be returned. |

Returns a list of
[CalendarEvent](calendar_events.html#CalendarEvent)
objects

## [Create a calendar event](#method.calendar_events_api.create) [CalendarEventsApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### POST /api/v1/calendar\_events

**Scope:** 
`url:POST|/api/v1/calendar_events`

Create and return a new calendar event

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| calendar\_event[context\_code] | Required | string | Context code of the course, group, user, or account whose calendar this event should be added to. |
| calendar\_event[title] |  | string | Short title for the calendar event. |
| calendar\_event[description] |  | string | Longer HTML description of the event. |
| calendar\_event[start\_at] |  | DateTime | Start date/time of the event. |
| calendar\_event[end\_at] |  | DateTime | End date/time of the event. |
| calendar\_event[location\_name] |  | string | Location name of the event. |
| calendar\_event[location\_address] |  | string | Location address |
| calendar\_event[time\_zone\_edited] |  | string | Time zone of the user editing the event. Allowed time zones are [IANA time zones](http://www.iana.org/time-zones "IANA time zones") or friendlier [Ruby on Rails time zones](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html "Ruby on Rails time zones"). |
| calendar\_event[all\_day] |  | boolean | When true event is considered to span the whole day and times are ignored. |
| calendar\_event[child\_event\_data][X][start\_at] |  | DateTime | Section-level start time(s) if this is a course event. X can be any identifier, provided that it is consistent across the start\_at, end\_at and context\_code |
| calendar\_event[child\_event\_data][X][end\_at] |  | DateTime | Section-level end time(s) if this is a course event. |
| calendar\_event[child\_event\_data][X][context\_code] |  | string | Context code(s) corresponding to the section-level start and end time(s). |
| calendar\_event[duplicate][count] |  | number | Number of times to copy/duplicate the event. Count cannot exceed 200. |
| calendar\_event[duplicate][interval] |  | number | Defaults to 1 if duplicate âcount` is set. The interval between the duplicated events. |
| calendar\_event[duplicate][frequency] |  | string | Defaults to âweeklyâ. The frequency at which to duplicate the event  Allowed values: `daily`, `weekly`, `monthly` |
| calendar\_event[duplicate][append\_iterator] |  | boolean | Defaults to false. If set to âtrue`, an increasing counter number will be appended to the event title when the event is duplicated. (e.g. Event 1, Event 2, Event 3, etc) |
| calendar\_event[rrule] |  | string | The recurrence rule to create a series of recurring events. Its value is the [iCalendar RRULE](https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html "iCalendar RRULE") defining how the event repeats. Unending series not supported. |
| calendar\_event[blackout\_date] |  | boolean | If the blackout\_date is true, this event represents a holiday or some other special day that does not count in course pacing. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events.json' \
     -X POST \
     -F 'calendar_event[context_code]=course_123' \
     -F 'calendar_event[title]=Paintball Fight!' \
     -F 'calendar_event[start_at]=2012-07-19T21:00:00Z' \
     -F 'calendar_event[end_at]=2012-07-19T22:00:00Z' \
     -H "Authorization: Bearer <token>"
```

## [Get a single calendar event or assignment](#method.calendar_events_api.show) [CalendarEventsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### GET /api/v1/calendar\_events/:id

**Scope:** 
`url:GET|/api/v1/calendar_events/:id`

## [Reserve a time slot](#method.calendar_events_api.reserve) [CalendarEventsApiController#reserve](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### POST /api/v1/calendar\_events/:id/reservations

**Scope:** 
`url:POST|/api/v1/calendar_events/:id/reservations`

### POST /api/v1/calendar\_events/:id/reservations/:participant\_id

**Scope:** 
`url:POST|/api/v1/calendar_events/:id/reservations/:participant_id`

Reserves a particular time slot and return the new reservation

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| participant\_id |  | string | User or group id for whom you are making the reservation (depends on the participant type). Defaults to the current user (or userâs candidate group). |
| comments |  | string | Comments to associate with this reservation |
| cancel\_existing |  | boolean | Defaults to false. If true, cancel any previous reservation(s) for this participant and appointment group. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events/345/reservations.json' \
     -X POST \
     -F 'cancel_existing=true' \
     -H "Authorization: Bearer <token>"
```

## [Update a calendar event](#method.calendar_events_api.update) [CalendarEventsApiController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### PUT /api/v1/calendar\_events/:id

**Scope:** 
`url:PUT|/api/v1/calendar_events/:id`

Update and return a calendar event

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| calendar\_event[context\_code] |  | string | Context code of the course, group, user, or account to move this event to. Scheduler appointments and events with section-specific times cannot be moved between calendars. |
| calendar\_event[title] |  | string | Short title for the calendar event. |
| calendar\_event[description] |  | string | Longer HTML description of the event. |
| calendar\_event[start\_at] |  | DateTime | Start date/time of the event. |
| calendar\_event[end\_at] |  | DateTime | End date/time of the event. |
| calendar\_event[location\_name] |  | string | Location name of the event. |
| calendar\_event[location\_address] |  | string | Location address |
| calendar\_event[time\_zone\_edited] |  | string | Time zone of the user editing the event. Allowed time zones are [IANA time zones](http://www.iana.org/time-zones "IANA time zones") or friendlier [Ruby on Rails time zones](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html "Ruby on Rails time zones"). |
| calendar\_event[all\_day] |  | boolean | When true event is considered to span the whole day and times are ignored. |
| calendar\_event[child\_event\_data][X][start\_at] |  | DateTime | Section-level start time(s) if this is a course event. X can be any identifier, provided that it is consistent across the start\_at, end\_at and context\_code |
| calendar\_event[child\_event\_data][X][end\_at] |  | DateTime | Section-level end time(s) if this is a course event. |
| calendar\_event[child\_event\_data][X][context\_code] |  | string | Context code(s) corresponding to the section-level start and end time(s). |
| calendar\_event[rrule] |  | string | Valid if the event whose ID is in the URL is part of a series. This defines the shape of the recurring event series after itâs updated. Its value is the iCalendar RRULE. Unending series are not supported. |
| which |  | string | Valid if the event whose ID is in the URL is part of a series. Update just the event whose ID is in in the URL, all events in the series, or the given event and all those following. Some updates may create a new series. For example, changing the start time of this and all following events from the middle of a series.  Allowed values: `one`, `all`, `following` |
| calendar\_event[blackout\_date] |  | boolean | If the blackout\_date is true, this event represents a holiday or some other special day that does not count in course pacing. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events/234' \
     -X PUT \
     -F 'calendar_event[title]=Epic Paintball Fight!' \
     -H "Authorization: Bearer <token>"
```

## [Delete a calendar event](#method.calendar_events_api.destroy) [CalendarEventsApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### DELETE /api/v1/calendar\_events/:id

**Scope:** 
`url:DELETE|/api/v1/calendar_events/:id`

Delete an event from the calendar and return the deleted event

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| cancel\_reason |  | string | Reason for deleting/canceling the event. |
| which |  | string | Valid if the event whose ID is in the URL is part of a series. Delete just the event whose ID is in in the URL, all events in the series, or the given event and all those following.  Allowed values: `one`, `all`, `following` |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events/234' \
     -X DELETE \
     -F 'cancel_reason=Greendale layed off the janitorial staff :(' \
     -F 'which=following'
     -H "Authorization: Bearer <token>"
```

## [Save enabled account calendars](#method.calendar_events_api.save_enabled_account_calendars) [CalendarEventsApiController#save\_enabled\_account\_calendars](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### POST /api/v1/calendar\_events/save\_enabled\_account\_calendars

**Scope:** 
`url:POST|/api/v1/calendar_events/save_enabled_account_calendars`

Creates and updates the enabled\_account\_calendars and mark\_feature\_as\_seen user preferences

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| mark\_feature\_as\_seen |  | boolean | Flag to mark account calendars feature as seen |
| enabled\_account\_calendars[] |  | Array | An array of account Ids to remember in the calendars list of the user |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events/save_enabled_account_calendars' \
     -X POST \
     -F 'mark_feature_as_seen=true' \
     -F 'enabled_account_calendars[]=1' \
     -F 'enabled_account_calendars[]=2' \
     -H "Authorization: Bearer <token>"
```

## [Set a course timetable](#method.calendar_events_api.set_course_timetable) [CalendarEventsApiController#set\_course\_timetable](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### POST /api/v1/courses/:course\_id/calendar\_events/timetable

**Scope:** 
`url:POST|/api/v1/courses/:course_id/calendar_events/timetable`

Creates and updates âtimetableâ events for a course. Can automaticaly generate a series of calendar events based on simple schedules (e.g. âMonday and Wednesday at 2:00pmâ )

Existing timetable events for the course and course sections will be updated if they still are part of the timetable. Otherwise, they will be deleted.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| timetables[course\_section\_id][] |  | Array | An array of timetable objects for the course section specified by course\_section\_id. If course\_section\_id is set to âallâ, events will be created for the entire course. |
| timetables[course\_section\_id][][weekdays] |  | string | A comma-separated list of abbreviated weekdays (Mon-Monday, Tue-Tuesday, Wed-Wednesday, Thu-Thursday, Fri-Friday, Sat-Saturday, Sun-Sunday) |
| timetables[course\_section\_id][][start\_time] |  | string | Time to start each event at (e.g. â9:00 amâ) |
| timetables[course\_section\_id][][end\_time] |  | string | Time to end each event at (e.g. â9:00 amâ) |
| timetables[course\_section\_id][][location\_name] |  | string | A location name to set for each event |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/calendar_events/timetable' \
     -X POST \
     -F 'timetables[all][][weekdays]=Mon,Wed,Fri' \
     -F 'timetables[all][][start_time]=11:00 am' \
     -F 'timetables[all][][end_time]=11:50 am' \
     -F 'timetables[all][][location_name]=Room 237' \
     -H "Authorization: Bearer <token>"
```

## [Get course timetable](#method.calendar_events_api.get_course_timetable) [CalendarEventsApiController#get\_course\_timetable](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### GET /api/v1/courses/:course\_id/calendar\_events/timetable

**Scope:** 
`url:GET|/api/v1/courses/:course_id/calendar_events/timetable`

Returns the last timetable set by the [Set a course timetable](calendar_events.html#method.calendar_events_api.set_course_timetable "Set a course timetable") endpoint

## [Create or update events directly for a course timetable](#method.calendar_events_api.set_course_timetable_events) [CalendarEventsApiController#set\_course\_timetable\_events](https://github.com/instructure/canvas-lms/blob/master/app/controllers/calendar_events_api_controller.rb)

### POST /api/v1/courses/:course\_id/calendar\_events/timetable\_events

**Scope:** 
`url:POST|/api/v1/courses/:course_id/calendar_events/timetable_events`

Creates and updates âtimetableâ events for a course or course section. Similar to [setting a course timetable](calendar_events.html#method.calendar_events_api.set_course_timetable "setting a course timetable"), but instead of generating a list of events based on a timetable schedule, this endpoint expects a complete list of events.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_section\_id |  | string | Events will be created for the course section specified by course\_section\_id. If not present, events will be created for the entire course. |
| events[] |  | Array | An array of event objects to use. |
| events[][start\_at] |  | DateTime | Start time for the event |
| events[][end\_at] |  | DateTime | End time for the event |
| events[][location\_name] |  | string | Location name for the event |
| events[][code] |  | string | A unique identifier that can be used to update the event at a later time If one is not specified, an identifier will be generated based on the start and end times |
| events[][title] |  | string | Title for the meeting. If not present, will default to the associated courseâs name |