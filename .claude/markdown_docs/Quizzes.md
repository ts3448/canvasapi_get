# Quizzes

# Quizzes API



### A Quiz object looks like:

```
{
  // the ID of the quiz
  "id": 5,
  // the title of the quiz
  "title": "Hamlet Act 3 Quiz",
  // the HTTP/HTTPS URL to the quiz
  "html_url": "http://canvas.example.edu/courses/1/quizzes/2",
  // a url suitable for loading the quiz in a mobile webview.  it will persiste
  // the headless session and, for quizzes in public courses, will force the user
  // to login
  "mobile_url": "http://canvas.example.edu/courses/1/quizzes/2?persist_healdess=1&force_user=1",
  // A url that can be visited in the browser with a POST request to preview a
  // quiz as the teacher. Only present when the user may grade
  "preview_url": "http://canvas.example.edu/courses/1/quizzes/2/take?preview=1",
  // the description of the quiz
  "description": "This is a quiz on Act 3 of Hamlet",
  // type of quiz possible values: 'practice_quiz', 'assignment', 'graded_survey',
  // 'survey'
  "quiz_type": "assignment",
  // the ID of the quiz's assignment group:
  "assignment_group_id": 3,
  // quiz time limit in minutes
  "time_limit": 5,
  // shuffle answers for students?
  "shuffle_answers": false,
  // let students see their quiz responses? possible values: null, 'always',
  // 'until_after_last_attempt'
  "hide_results": "always",
  // show which answers were correct when results are shown? only valid if
  // hide_results=null
  "show_correct_answers": true,
  // restrict the show_correct_answers option above to apply only to the last
  // submitted attempt of a quiz that allows multiple attempts. only valid if
  // show_correct_answers=true and allowed_attempts > 1
  "show_correct_answers_last_attempt": true,
  // when should the correct answers be visible by students? only valid if
  // show_correct_answers=true
  "show_correct_answers_at": "2013-01-23T23:59:00-07:00",
  // prevent the students from seeing correct answers after the specified date has
  // passed. only valid if show_correct_answers=true
  "hide_correct_answers_at": "2013-01-23T23:59:00-07:00",
  // prevent the students from seeing their results more than once (right after
  // they submit the quiz)
  "one_time_results": true,
  // which quiz score to keep (only if allowed_attempts != 1) possible values:
  // 'keep_highest', 'keep_latest'
  "scoring_policy": "keep_highest",
  // how many times a student can take the quiz -1 = unlimited attempts
  "allowed_attempts": 3,
  // show one question at a time?
  "one_question_at_a_time": false,
  // the number of questions in the quiz
  "question_count": 12,
  // The total point value given to the quiz
  "points_possible": 20,
  // lock questions after answering? only valid if one_question_at_a_time=true
  "cant_go_back": false,
  // access code to restrict quiz access
  "access_code": "2beornot2be",
  // IP address or range that quiz access is limited to
  "ip_filter": "123.123.123.123",
  // when the quiz is due
  "due_at": "2013-01-23T23:59:00-07:00",
  // when to lock the quiz
  "lock_at": null,
  // when to unlock the quiz
  "unlock_at": "2013-01-21T23:59:00-07:00",
  // whether the quiz has a published or unpublished draft state.
  "published": true,
  // Whether the assignment's 'published' state can be changed to false. Will be
  // false if there are student submissions for the quiz.
  "unpublishable": true,
  // Whether or not this is locked for the user.
  "locked_for_user": false,
  // (Optional) Information for the user about the lock. Present when
  // locked_for_user is true.
  "lock_info": null,
  // (Optional) An explanation of why this is locked for the user. Present when
  // locked_for_user is true.
  "lock_explanation": "This quiz is locked until September 1 at 12:00am",
  // Link to SpeedGrader for this quiz. Will not be present if quiz is unpublished
  "speedgrader_url": "http://canvas.instructure.com/courses/1/speed_grader?assignment_id=1",
  // Link to endpoint to send extensions for this quiz.
  "quiz_extensions_url": "http://canvas.instructure.com/courses/1/quizzes/2/quiz_extensions",
  // Permissions the user has for the quiz
  "permissions": null,
  // list of due dates for the quiz
  "all_dates": null,
  // Current version number of the quiz
  "version_number": 3,
  // List of question types in the quiz
  "question_types": ["multiple_choice", "essay"],
  // Whether survey submissions will be kept anonymous (only applicable to
  // 'graded_survey', 'survey' quiz types)
  "anonymous_submissions": false
}
```

### A QuizPermissions object looks like:

```
// Permissions the user has for the quiz
{
  // whether the user can view the quiz
  "read": true,
  // whether the user may submit a submission for the quiz
  "submit": true,
  // whether the user may create a new quiz
  "create": true,
  // whether the user may edit, update, or delete the quiz
  "manage": true,
  // whether the user may view quiz statistics for this quiz
  "read_statistics": true,
  // whether the user may review grades for all quiz submissions for this quiz
  "review_grades": true,
  // whether the user may update the quiz
  "update": true
}
```

## [List quizzes in a course](#method.quizzes/quizzes_api.index) [Quizzes::QuizzesApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes`

Returns the paginated list of Quizzes in this course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| search\_term |  | string | The partial title of the quizzes to match and return. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/quizzes \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[Quiz](quizzes.html#Quiz)
objects

## [Get a single quiz](#method.quizzes/quizzes_api.show) [Quizzes::QuizzesApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes/:id`

Returns the quiz with the given id.

Returns a
[Quiz](quizzes.html#Quiz)
object

## [Create a quiz](#method.quizzes/quizzes_api.create) [Quizzes::QuizzesApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes`

Create a new quiz for this course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz[title] | Required | string | The quiz title. |
| quiz[description] |  | string | A description of the quiz. |
| quiz[quiz\_type] |  | string | The type of quiz.  Allowed values: `practice_quiz`, `assignment`, `graded_survey`, `survey` |
| quiz[assignment\_group\_id] |  | integer | The assignment group id to put the assignment in. Defaults to the top assignment group in the course. Only valid if the quiz is graded, i.e. if quiz\_type is âassignmentâ or âgraded\_surveyâ. |
| quiz[time\_limit] |  | integer | Time limit to take this quiz, in minutes. Set to null for no time limit. Defaults to null. |
| quiz[shuffle\_answers] |  | boolean | If true, quiz answers for multiple choice questions will be randomized for each student. Defaults to false. |
| quiz[hide\_results] |  | string | Dictates whether or not quiz results are hidden from students. If null, students can see their results after any attempt. If âalwaysâ, students can never see their results. If âuntil\_after\_last\_attemptâ, students can only see results after their last attempt. (Only valid if allowed\_attempts > 1). Defaults to null.  Allowed values: `always`, `until_after_last_attempt` |
| quiz[show\_correct\_answers] |  | boolean | Only valid if hide\_results=null If false, hides correct answers from students when quiz results are viewed. Defaults to true. |
| quiz[show\_correct\_answers\_last\_attempt] |  | boolean | Only valid if show\_correct\_answers=true and allowed\_attempts > 1 If true, hides correct answers from students when quiz results are viewed until they submit the last attempt for the quiz. Defaults to false. |
| quiz[show\_correct\_answers\_at] |  | DateTime | Only valid if show\_correct\_answers=true If set, the correct answers will be visible by students only after this date, otherwise the correct answers are visible once the student hands in their quiz submission. |
| quiz[hide\_correct\_answers\_at] |  | DateTime | Only valid if show\_correct\_answers=true If set, the correct answers will stop being visible once this date has passed. Otherwise, the correct answers will be visible indefinitely. |
| quiz[allowed\_attempts] |  | integer | Number of times a student is allowed to take a quiz. Set to -1 for unlimited attempts. Defaults to 1. |
| quiz[scoring\_policy] |  | string | Required and only valid if allowed\_attempts > 1. Scoring policy for a quiz that students can take multiple times. Defaults to âkeep\_highestâ.  Allowed values: `keep_highest`, `keep_latest` |
| quiz[one\_question\_at\_a\_time] |  | boolean | If true, shows quiz to student one question at a time. Defaults to false. |
| quiz[cant\_go\_back] |  | boolean | Only valid if one\_question\_at\_a\_time=true If true, questions are locked after answering. Defaults to false. |
| quiz[access\_code] |  | string | Restricts access to the quiz with a password. For no access code restriction, set to null. Defaults to null. |
| quiz[ip\_filter] |  | string | Restricts access to the quiz to computers in a specified IP range. Filters can be a comma-separated list of addresses, or an address followed by a mask  Examples:   ``` "192.168.217.1" "192.168.217.1/24" "192.168.217.1/255.255.255.0"  ```   For no IP filter restriction, set to null. Defaults to null. |
| quiz[due\_at] |  | DateTime | The day/time the quiz is due. Accepts times in ISO 8601 format, e.g. 2011-10-21T18:48Z. |
| quiz[lock\_at] |  | DateTime | The day/time the quiz is locked for students. Accepts times in ISO 8601 format, e.g. 2011-10-21T18:48Z. |
| quiz[unlock\_at] |  | DateTime | The day/time the quiz is unlocked for students. Accepts times in ISO 8601 format, e.g. 2011-10-21T18:48Z. |
| quiz[published] |  | boolean | Whether the quiz should have a draft state of published or unpublished. NOTE: If students have started taking the quiz, or there are any submissions for the quiz, you may not unpublish a quiz and will recieve an error. |
| quiz[one\_time\_results] |  | boolean | Whether students should be prevented from viewing their quiz results past the first time (right after they turn the quiz in.) Only valid if âhide\_resultsâ is not set to âalwaysâ. Defaults to false. |
| quiz[only\_visible\_to\_overrides] |  | boolean | Whether this quiz is only visible to overrides (Only useful if âdifferentiated assignmentsâ account setting is on) Defaults to false. |

Returns a
[Quiz](quizzes.html#Quiz)
object

## [Edit a quiz](#method.quizzes/quizzes_api.update) [Quizzes::QuizzesApiController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### PUT /api/v1/courses/:course\_id/quizzes/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/quizzes/:id`

Modify an existing quiz. See the documentation for quiz creation.

Additional arguments:

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz[notify\_of\_update] |  | boolean | If true, notifies users that the quiz has changed. Defaults to true |

Returns a
[Quiz](quizzes.html#Quiz)
object

## [Delete a quiz](#method.quizzes/quizzes_api.destroy) [Quizzes::QuizzesApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/quizzes/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/quizzes/:id`

## [Reorder quiz items](#method.quizzes/quizzes_api.reorder) [Quizzes::QuizzesApiController#reorder](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes/:id/reorder

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes/:id/reorder`

Change order of the quiz questions or groups within the quiz

**204 No Content** response code is returned if the reorder was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| order[][id] | Required | integer | The associated itemâs unique identifier |
| order[][type] |  | string | The type of item is either âquestionâ or âgroupâ  Allowed values: `question`, `group` |

## [Validate quiz access code](#method.quizzes/quizzes_api.validate_access_code) [Quizzes::QuizzesApiController#validate\_access\_code](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quizzes_api_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes/:id/validate\_access\_code

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes/:id/validate_access_code`

Accepts an access code and returns a boolean indicating whether that access code is correct

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| access\_code | Required | string | The access code being validated |