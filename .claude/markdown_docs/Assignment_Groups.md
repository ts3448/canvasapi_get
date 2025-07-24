# Assignment Groups

# Assignment Groups API



API for accessing Assignment Group and Assignment information.

### A GradingRules object looks like:

```
{
  // Number of lowest scores to be dropped for each user.
  "drop_lowest": 1,
  // Number of highest scores to be dropped for each user.
  "drop_highest": 1,
  // Assignment IDs that should never be dropped.
  "never_drop": [33, 17, 24]
}
```

### An AssignmentGroup object looks like:

```
{
  // the id of the Assignment Group
  "id": 1,
  // the name of the Assignment Group
  "name": "group2",
  // the position of the Assignment Group
  "position": 7,
  // the weight of the Assignment Group
  "group_weight": 20,
  // the sis source id of the Assignment Group
  "sis_source_id": "1234",
  // the integration data of the Assignment Group
  "integration_data": {"5678":"0954"},
  // the assignments in this Assignment Group (see the Assignment API for a
  // detailed list of fields)
  "assignments": [],
  // the grading rules that this Assignment Group has
  "rules": null
}
```

## [List assignment groups](#method.assignment_groups.index) [AssignmentGroupsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/assignment_groups_controller.rb)

### GET /api/v1/courses/:course\_id/assignment\_groups

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignment_groups`

Returns the paginated list of assignment groups for the current context. The returned groups are sorted by their position field.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Associations to include with the group. âdiscussion\_topicâ, âall\_datesâ, âcan\_editâ, âassignment\_visibilityâ & âsubmissionâ are only valid if âassignmentsâ is also included. âscore\_statisticsâ requires that the âassignmentsâ and âsubmissionâ options are included. The âassignment\_visibilityâ option additionally requires that the Differentiated Assignments course feature be turned on. If âobserved\_usersâ is passed along with âassignmentsâ and âsubmissionâ, submissions for observed users will also be included as an array.  Allowed values: `assignments`, `discussion_topic`, `all_dates`, `assignment_visibility`, `overrides`, `submission`, `observed_users`, `can_edit`, `score_statistics` |
| assignment\_ids[] |  | string | If âassignmentsâ are included, optionally return only assignments having their ID in this array. This argument may also be passed as a comma separated string. |
| exclude\_assignment\_submission\_types[] |  | string | If âassignmentsâ are included, those with the specified submission types will be excluded from the assignment groups.  Allowed values: `online_quiz`, `discussion_topic`, `wiki_page`, `external_tool` |
| override\_assignment\_dates |  | boolean | Apply assignment overrides for each assignment, defaults to true. |
| grading\_period\_id |  | integer | The id of the grading period in which assignment groups are being requested (Requires grading periods to exist.) |
| scope\_assignments\_to\_student |  | boolean | If true, all assignments returned will apply to the current user in the specified grading period. If assignments apply to other students in the specified grading period, but not the current user, they will not be returned. (Requires the grading\_period\_id argument and grading periods to exist. In addition, the current user must be a student.) |

Returns a list of
[AssignmentGroup](assignment_groups.html#AssignmentGroup)
objects

## [Get an Assignment Group](#method.assignment_groups_api.show) [AssignmentGroupsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/assignment_groups_api_controller.rb)

### GET /api/v1/courses/:course\_id/assignment\_groups/:assignment\_group\_id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignment_groups/:assignment_group_id`

Returns the assignment group with the given id.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Associations to include with the group. âdiscussion\_topicâ and âassignment\_visibilityâ and âsubmissionâ are only valid if âassignmentsâ is also included. âscore\_statisticsâ is only valid if âsubmissionâ and âassignmentsâ are also included. The âassignment\_visibilityâ option additionally requires that the Differentiated Assignments course feature be turned on.  Allowed values: `assignments`, `discussion_topic`, `assignment_visibility`, `submission`, `score_statistics` |
| override\_assignment\_dates |  | boolean | Apply assignment overrides for each assignment, defaults to true. |
| grading\_period\_id |  | integer | The id of the grading period in which assignment groups are being requested (Requires grading periods to exist on the account) |

Returns an
[AssignmentGroup](assignment_groups.html#AssignmentGroup)
object

## [Create an Assignment Group](#method.assignment_groups_api.create) [AssignmentGroupsApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/assignment_groups_api_controller.rb)

### POST /api/v1/courses/:course\_id/assignment\_groups

**Scope:** 
`url:POST|/api/v1/courses/:course_id/assignment_groups`

Create a new assignment group for this course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The assignment groupâs name |
| position |  | integer | The position of this assignment group in relation to the other assignment groups |
| group\_weight |  | number | The percent of the total grade that this assignment group represents |
| sis\_source\_id |  | string | The sis source id of the Assignment Group |
| integration\_data |  | Object | The integration data of the Assignment Group |

Returns an
[AssignmentGroup](assignment_groups.html#AssignmentGroup)
object

## [Edit an Assignment Group](#method.assignment_groups_api.update) [AssignmentGroupsApiController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/assignment_groups_api_controller.rb)

### PUT /api/v1/courses/:course\_id/assignment\_groups/:assignment\_group\_id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/assignment_groups/:assignment_group_id`

Modify an existing Assignment Group.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The assignment groupâs name |
| position |  | integer | The position of this assignment group in relation to the other assignment groups |
| group\_weight |  | number | The percent of the total grade that this assignment group represents |
| sis\_source\_id |  | string | The sis source id of the Assignment Group |
| integration\_data |  | Object | The integration data of the Assignment Group |
| rules |  | string | The grading rules that are applied within this assignment group See the Assignment Group object definition for format |

Returns an
[AssignmentGroup](assignment_groups.html#AssignmentGroup)
object

## [Destroy an Assignment Group](#method.assignment_groups_api.destroy) [AssignmentGroupsApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/assignment_groups_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/assignment\_groups/:assignment\_group\_id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/assignment_groups/:assignment_group_id`

Deletes the assignment group with the given id.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| move\_assignments\_to |  | integer | The ID of an active Assignment Group to which the assignments that are currently assigned to the destroyed Assignment Group will be assigned. NOTE: If this argument is not provided, any assignments in this Assignment Group will be deleted. |

Returns an
[AssignmentGroup](assignment_groups.html#AssignmentGroup)
object