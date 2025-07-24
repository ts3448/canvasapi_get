# Moderated Grading

# Moderated Grading API



API for viewing and adding students to the list of people in moderation
for an assignment

API for manipulating provisional grades

Provisional grades are created by using the Submissions API endpoint "Grade or comment on a submission" with `provisional=true`.
They can be viewed by using "List assignment submissions", "Get a single submission", or "List gradeable students" with `include[]=provisional_grades`.
This API performs other operations on provisional grades for use with the Moderated Grading feature.

### A ProvisionalGrade object looks like:

```
{
  // The identifier for the provisional grade
  "provisional_grade_id": 23,
  // The numeric score
  "score": 90,
  // The grade
  "grade": "A-",
  // Whether the grade was applied to the most current submission (false if the
  // student resubmitted after grading)
  "grade_matches_current_submission": true,
  // When the grade was given
  "graded_at": "2015-11-01T00:03:21-06:00",
  // Whether this is the 'final' provisional grade created by the moderator
  "final": false,
  // A link to view this provisional grade in SpeedGrader
  "speedgrader_url": "http://www.example.com/courses/123/gradebook/speed_grader?..."
}
```

## [List students selected for moderation](#method.moderation_set.index) [ModerationSetController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/moderation_set_controller.rb)

### GET /api/v1/courses/:course\_id/assignments/:assignment\_id/moderated\_students

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/moderated_students`

Returns a paginated list of students selected for moderation

Returns a list of
[User](users.html#User)
objects

## [Select students for moderation](#method.moderation_set.create) [ModerationSetController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/moderation_set_controller.rb)

### POST /api/v1/courses/:course\_id/assignments/:assignment\_id/moderated\_students

**Scope:** 
`url:POST|/api/v1/courses/:course_id/assignments/:assignment_id/moderated_students`

Returns an array of users that were selected for moderation

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| student\_ids[] |  | number | user ids for students to select for moderation |

Returns a list of
[User](users.html#User)
objects

## [Bulk select provisional grades](#method.provisional_grades.bulk_select) [ProvisionalGradesController#bulk\_select](https://github.com/instructure/canvas-lms/blob/master/app/controllers/provisional_grades_controller.rb)

### PUT /api/v1/courses/:course\_id/assignments/:assignment\_id/provisional\_grades/bulk\_select

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/bulk_select`

Choose which provisional grades will be received by associated students for an assignment. The caller must be the final grader for the assignment or an admin with :select\_final\_grade rights.

#### Example Response:

#### 

```
[{
  "assignment_id": 867,
  "student_id": 5309,
  "selected_provisional_grade_id": 53669
}]
```

## [Show provisional grade status for a student](#method.provisional_grades.status) [ProvisionalGradesController#status](https://github.com/instructure/canvas-lms/blob/master/app/controllers/provisional_grades_controller.rb)

### GET /api/v1/courses/:course\_id/assignments/:assignment\_id/provisional\_grades/status

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/status`

Tell whether the studentâs submission needs one or more provisional grades.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| student\_id |  | integer | The id of the student to show the status for |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/1/assignments/2/provisional_grades/status?student_id=1'
```

#### Example Response:

#### 

```
{ "needs_provisional_grade": false }
```

## [Select provisional grade](#method.provisional_grades.select) [ProvisionalGradesController#select](https://github.com/instructure/canvas-lms/blob/master/app/controllers/provisional_grades_controller.rb)

### PUT /api/v1/courses/:course\_id/assignments/:assignment\_id/provisional\_grades/:provisional\_grade\_id/select

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/:provisional_grade_id/select`

Choose which provisional grade the student should receive for a submission. The caller must be the final grader for the assignment or an admin with :select\_final\_grade rights.

#### Example Response:

#### 

```
{
  "assignment_id": 867,
  "student_id": 5309,
  "selected_provisional_grade_id": 53669
}
```

## [Publish provisional grades for an assignment](#method.provisional_grades.publish) [ProvisionalGradesController#publish](https://github.com/instructure/canvas-lms/blob/master/app/controllers/provisional_grades_controller.rb)

### POST /api/v1/courses/:course\_id/assignments/:assignment\_id/provisional\_grades/publish

**Scope:** 
`url:POST|/api/v1/courses/:course_id/assignments/:assignment_id/provisional_grades/publish`

Publish the selected provisional grade for all submissions to an assignment. Use the âSelect provisional gradeâ endpoint to choose which provisional grade to publish for a particular submission.

Students not in the moderation set will have their one and only provisional grade published.

WARNING: This is irreversible. This will overwrite existing grades in the gradebook.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/1/assignments/2/provisional_grades/publish' \
     -X POST
```

## [Show provisional grade status for a student](#method.anonymous_provisional_grades.status) [AnonymousProvisionalGradesController#status](https://github.com/instructure/canvas-lms/blob/master/app/controllers/anonymous_provisional_grades_controller.rb)

### GET /api/v1/courses/:course\_id/assignments/:assignment\_id/anonymous\_provisional\_grades/status

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/anonymous_provisional_grades/status`

Determine whether or not the studentâs submission needs one or more provisional grades.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| anonymous\_id |  | string | The id of the student to show the status for |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/1/assignments/2/anonymous_provisional_grades/status?anonymous_id=1'
```

#### Example Response:

#### 

```
{ "needs_provisional_grade": false }
```