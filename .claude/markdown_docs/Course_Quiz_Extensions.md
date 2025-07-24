# Course Quiz Extensions

# Course Quiz Extensions API



API for setting extensions on student quiz submissions at the course level

### A CourseQuizExtension object looks like:

```
{
  // The ID of the Student that needs the quiz extension.
  "user_id": 3,
  // Number of times the student is allowed to re-take the quiz over the
  // multiple-attempt limit.
  "extra_attempts": 1,
  // Amount of extra time allowed for the quiz submission, in minutes.
  "extra_time": 60,
  // The student can take the quiz even if it's locked for everyone else
  "manually_unlocked": true,
  // The time at which the quiz submission will be overdue, and be flagged as a
  // late submission.
  "end_at": "2013-11-07T13:16:18Z"
}
```

## [Set extensions for student quiz submissions](#method.quizzes/course_quiz_extensions.create) [Quizzes::CourseQuizExtensionsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/course_quiz_extensions_controller.rb)

### POST /api/v1/courses/:course\_id/quiz\_extensions

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quiz_extensions`

**Responses**

* **200 OK** if the request was successful
* **403 Forbidden** if you are not allowed to extend quizzes for this course

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id | Required | integer | The ID of the user we want to add quiz extensions for. |
| extra\_attempts |  | integer | Number of times the student is allowed to re-take the quiz over the multiple-attempt limit. This is limited to 1000 attempts or less. |
| extra\_time |  | integer | The number of extra minutes to allow for all attempts. This will add to the existing time limit on the submission. This is limited to 10080 minutes (1 week) |
| manually\_unlocked |  | boolean | Allow the student to take the quiz even if itâs locked for everyone else. |
| extend\_from\_now |  | integer | The number of minutes to extend the quiz from the current time. This is mutually exclusive to extend\_from\_end\_at. This is limited to 1440 minutes (24 hours) |
| extend\_from\_end\_at |  | integer | The number of minutes to extend the quiz beyond the quizâs current ending time. This is mutually exclusive to extend\_from\_now. This is limited to 1440 minutes (24 hours) |

#### Example Request:

#### 

```
{
  "quiz_extensions": [{
    "user_id": 3,
    "extra_attempts": 2,
    "extra_time": 20,
    "manually_unlocked": true
  },{
    "user_id": 2,
    "extra_attempts": 2,
    "extra_time": 20,
    "manually_unlocked": false
  }]
}
```

#### 

```
{
  "quiz_extensions": [{
    "user_id": 3,
    "extend_from_now": 20
  }]
}
```

#### Example Response:

#### 

```
{
  "quiz_extensions": [QuizExtension]
}
```