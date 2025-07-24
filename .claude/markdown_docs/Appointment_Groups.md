# Appointment Groups

# Appointment Groups API



API for creating, accessing and updating appointment groups. Appointment groups
provide a way of creating a bundle of time slots that users can sign up for
(e.g. "Office Hours" or "Meet with professor about Final Project"). Both time
slots and reservations of time slots are stored as Calendar Events.

### An Appointment object looks like:

```
// Date and time for an appointment
{
  // The appointment identifier.
  "id": 987,
  // Start time for the appointment
  "start_at": "2012-07-20T15:00:00-06:00",
  // End time for the appointment
  "end_at": "2012-07-20T15:00:00-06:00"
}
```

### An AppointmentGroup object looks like:

```
{
  // The ID of the appointment group
  "id": 543,
  // The title of the appointment group
  "title": "Final Presentation",
  // The start of the first time slot in the appointment group
  "start_at": "2012-07-20T15:00:00-06:00",
  // The end of the last time slot in the appointment group
  "end_at": "2012-07-20T17:00:00-06:00",
  // The text description of the appointment group
  "description": "Es muy importante",
  // The location name of the appointment group
  "location_name": "El Tigre Chino's office",
  // The address of the appointment group's location
  "location_address": "Room 234",
  // The number of participant who have reserved slots (see include[] argument)
  "participant_count": 2,
  // The start and end times of slots reserved by the current user as well as the
  // id of the calendar event for the reservation (see include[] argument)
  "reserved_times": [{"id":987,"start_at":"2012-07-20T15:00:00-06:00","end_at":"2012-07-20T15:00:00-06:00"}],
  // Boolean indicating whether observer users should be able to sign-up for an
  // appointment
  "allow_observer_signup": false,
  // The context codes (i.e. courses) this appointment group belongs to. Only
  // people in these courses will be eligible to sign up.
  "context_codes": ["course_123"],
  // The sub-context codes (i.e. course sections and group categories) this
  // appointment group is restricted to
  "sub_context_codes": [course_section_234],
  // Current state of the appointment group ('pending', 'active' or 'deleted').
  // 'pending' indicates that it has not been published yet and is invisible to
  // participants.
  "workflow_state": "active",
  // Boolean indicating whether the current user needs to sign up for this
  // appointment group (i.e. it's reservable and the
  // min_appointments_per_participant limit has not been met by this user).
  "requiring_action": true,
  // Number of time slots in this appointment group
  "appointments_count": 2,
  // Calendar Events representing the time slots (see include[] argument) Refer to
  // the Calendar Events API for more information
  "appointments": [],
  // Newly created time slots (same format as appointments above). Only returned
  // in Create/Update responses where new time slots have been added
  "new_appointments": [],
  // Maximum number of time slots a user may register for, or null if no limit
  "max_appointments_per_participant": 1,
  // Minimum number of time slots a user must register for. If not set, users do
  // not need to sign up for any time slots
  "min_appointments_per_participant": 1,
  // Maximum number of participants that may register for each time slot, or null
  // if no limit
  "participants_per_appointment": 1,
  // 'private' means participants cannot see who has signed up for a particular
  // time slot, 'protected' means that they can
  "participant_visibility": "private",
  // Indicates how participants sign up for the appointment group, either as
  // individuals ('User') or in student groups ('Group'). Related to
  // sub_context_codes (i.e. 'Group' signups always have a single group category)
  "participant_type": "User",
  // URL for this appointment group (to update, delete, etc.)
  "url": "https://example.com/api/v1/appointment_groups/543",
  // URL for a user to view this appointment group
  "html_url": "http://example.com/appointment_groups/1",
  // When the appointment group was created
  "created_at": "2012-07-13T10:55:20-06:00",
  // When the appointment group was last updated
  "updated_at": "2012-07-13T10:55:20-06:00"
}
```

## [List appointment groups](#method.appointment_groups.index) [AppointmentGroupsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### GET /api/v1/appointment\_groups

**Scope:** 
`url:GET|/api/v1/appointment_groups`

Retrieve the paginated list of appointment groups that can be reserved or managed by the current user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| scope |  | string | Defaults to âreservableâ  Allowed values: `reservable`, `manageable` |
| context\_codes[] |  | string | Array of context codes used to limit returned results. |
| include\_past\_appointments |  | boolean | Defaults to false. If true, includes past appointment groups |
| include[] |  | string | Array of additional information to include.  âappointmentsâ  calendar event time slots for this appointment group  âchild\_eventsâ  reservations of those time slots  âparticipant\_countâ  number of reservations  âreserved\_timesâ  the event id, start time and end time of reservations the current user has made)  âall\_context\_codesâ  all context codes associated with this appointment group  Allowed values: `appointments`, `child_events`, `participant_count`, `reserved_times`, `all_context_codes` |

## [Create an appointment group](#method.appointment_groups.create) [AppointmentGroupsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### POST /api/v1/appointment\_groups

**Scope:** 
`url:POST|/api/v1/appointment_groups`

Create and return a new appointment group. If new\_appointments are specified, the response will return a new\_appointments array (same format as appointments array, see âList appointment groupsâ action)

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| appointment\_group[context\_codes][] | Required | string | Array of context codes (courses, e.g. course\_1) this group should be linked to (1 or more). Users in the course(s) with appropriate permissions will be able to sign up for this appointment group. |
| appointment\_group[sub\_context\_codes][] |  | string | Array of sub context codes (course sections or a single group category) this group should be linked to. Used to limit the appointment group to particular sections. If a group category is specified, students will sign up in groups and the participant\_type will be âGroupâ instead of âUserâ. |
| appointment\_group[title] | Required | string | Short title for the appointment group. |
| appointment\_group[description] |  | string | Longer text description of the appointment group. |
| appointment\_group[location\_name] |  | string | Location name of the appointment group. |
| appointment\_group[location\_address] |  | string | Location address. |
| appointment\_group[publish] |  | boolean | Indicates whether this appointment group should be published (i.e. made available for signup). Once published, an appointment group cannot be unpublished. Defaults to false. |
| appointment\_group[participants\_per\_appointment] |  | integer | Maximum number of participants that may register for each time slot. Defaults to null (no limit). |
| appointment\_group[min\_appointments\_per\_participant] |  | integer | Minimum number of time slots a user must register for. If not set, users do not need to sign up for any time slots. |
| appointment\_group[max\_appointments\_per\_participant] |  | integer | Maximum number of time slots a user may register for. |
| appointment\_group[new\_appointments][X][] |  | string | Nested array of start time/end time pairs indicating time slots for this appointment group. Refer to the example request. |
| appointment\_group[participant\_visibility] |  | string | âprivateâ  participants cannot see who has signed up for a particular time slot  âprotectedâ  participants can see who has signed up. Defaults to âprivateâ.  Allowed values: `private`, `protected` |
| appointment\_group[allow\_observer\_signup] |  | boolean | Whether observer users can sign-up for an appointment. Defaults to false. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/appointment_groups.json' \
     -X POST \
     -F 'appointment_group[context_codes][]=course_123' \
     -F 'appointment_group[sub_context_codes][]=course_section_234' \
     -F 'appointment_group[title]=Final Presentation' \
     -F 'appointment_group[participants_per_appointment]=1' \
     -F 'appointment_group[min_appointments_per_participant]=1' \
     -F 'appointment_group[max_appointments_per_participant]=1' \
     -F 'appointment_group[new_appointments][0][]=2012-07-19T21:00:00Z' \
     -F 'appointment_group[new_appointments][0][]=2012-07-19T22:00:00Z' \
     -F 'appointment_group[new_appointments][1][]=2012-07-19T22:00:00Z' \
     -F 'appointment_group[new_appointments][1][]=2012-07-19T23:00:00Z' \
     -H "Authorization: Bearer <token>"
```

## [Get a single appointment group](#method.appointment_groups.show) [AppointmentGroupsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### GET /api/v1/appointment\_groups/:id

**Scope:** 
`url:GET|/api/v1/appointment_groups/:id`

Returns information for a single appointment group

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Array of additional information to include. See include[] argument of âList appointment groupsâ action.  âchild\_eventsâ  reservations of time slots time slots  âappointmentsâ  will always be returned  âall\_context\_codesâ  all context codes associated with this appointment group  Allowed values: `child_events`, `appointments`, `all_context_codes` |

## [Update an appointment group](#method.appointment_groups.update) [AppointmentGroupsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### PUT /api/v1/appointment\_groups/:id

**Scope:** 
`url:PUT|/api/v1/appointment_groups/:id`

Update and return an appointment group. If new\_appointments are specified, the response will return a new\_appointments array (same format as appointments array, see âList appointment groupsâ action).

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| appointment\_group[context\_codes][] | Required | string | Array of context codes (courses, e.g. course\_1) this group should be linked to (1 or more). Users in the course(s) with appropriate permissions will be able to sign up for this appointment group. |
| appointment\_group[sub\_context\_codes][] |  | string | Array of sub context codes (course sections or a single group category) this group should be linked to. Used to limit the appointment group to particular sections. If a group category is specified, students will sign up in groups and the participant\_type will be âGroupâ instead of âUserâ. |
| appointment\_group[title] |  | string | Short title for the appointment group. |
| appointment\_group[description] |  | string | Longer text description of the appointment group. |
| appointment\_group[location\_name] |  | string | Location name of the appointment group. |
| appointment\_group[location\_address] |  | string | Location address. |
| appointment\_group[publish] |  | boolean | Indicates whether this appointment group should be published (i.e. made available for signup). Once published, an appointment group cannot be unpublished. Defaults to false. |
| appointment\_group[participants\_per\_appointment] |  | integer | Maximum number of participants that may register for each time slot. Defaults to null (no limit). |
| appointment\_group[min\_appointments\_per\_participant] |  | integer | Minimum number of time slots a user must register for. If not set, users do not need to sign up for any time slots. |
| appointment\_group[max\_appointments\_per\_participant] |  | integer | Maximum number of time slots a user may register for. |
| appointment\_group[new\_appointments][X][] |  | string | Nested array of start time/end time pairs indicating time slots for this appointment group. Refer to the example request. |
| appointment\_group[participant\_visibility] |  | string | âprivateâ  participants cannot see who has signed up for a particular time slot  âprotectedâ  participants can see who has signed up. Defaults to âprivateâ.  Allowed values: `private`, `protected` |
| appointment\_group[allow\_observer\_signup] |  | boolean | Whether observer users can sign-up for an appointment. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/appointment_groups/543.json' \
     -X PUT \
     -F 'appointment_group[publish]=1' \
     -H "Authorization: Bearer <token>"
```

## [Delete an appointment group](#method.appointment_groups.destroy) [AppointmentGroupsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### DELETE /api/v1/appointment\_groups/:id

**Scope:** 
`url:DELETE|/api/v1/appointment_groups/:id`

Delete an appointment group (and associated time slots and reservations) and return the deleted group

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| cancel\_reason |  | string | Reason for deleting/canceling the appointment group. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/appointment_groups/543.json' \
     -X DELETE \
     -F 'cancel_reason=El Tigre Chino got fired' \
     -H "Authorization: Bearer <token>"
```

## [List user participants](#method.appointment_groups.users) [AppointmentGroupsController#users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### GET /api/v1/appointment\_groups/:id/users

**Scope:** 
`url:GET|/api/v1/appointment_groups/:id/users`

A paginated list of users that are (or may be) participating in this appointment group. Refer to the Users API for the response fields. Returns no results for appointment groups with the âGroupâ participant\_type.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| registration\_status |  | string | Limits results to the a given participation status, defaults to âallâ  Allowed values: `all`, `registered`, `registered` |

## [List student group participants](#method.appointment_groups.groups) [AppointmentGroupsController#groups](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### GET /api/v1/appointment\_groups/:id/groups

**Scope:** 
`url:GET|/api/v1/appointment_groups/:id/groups`

A paginated list of student groups that are (or may be) participating in this appointment group. Refer to the Groups API for the response fields. Returns no results for appointment groups with the âUserâ participant\_type.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| registration\_status |  | string | Limits results to the a given participation status, defaults to âallâ  Allowed values: `all`, `registered`, `registered` |

## [Get next appointment](#method.appointment_groups.next_appointment) [AppointmentGroupsController#next\_appointment](https://github.com/instructure/canvas-lms/blob/master/app/controllers/appointment_groups_controller.rb)

### GET /api/v1/appointment\_groups/next\_appointment

**Scope:** 
`url:GET|/api/v1/appointment_groups/next_appointment`

Return the next appointment available to sign up for. The appointment is returned in a one-element array. If no future appointments are available, an empty array is returned.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| appointment\_group\_ids[] |  | string | List of ids of appointment groups to search. |

Returns a list of
[CalendarEvent](calendar_events.html#CalendarEvent)
objects