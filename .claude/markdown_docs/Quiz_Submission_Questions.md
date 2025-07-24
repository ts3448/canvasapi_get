# Quiz Submission Questions

# Quiz Submission Questions API



API for answering and flagging questions in a quiz-taking session.

### A QuizSubmissionQuestion object looks like:

```
{
  // The ID of the QuizQuestion this answer is for.
  "id": 1,
  // Whether this question is flagged.
  "flagged": true,
  // The provided answer (if any) for this question. The format of this parameter
  // depends on the type of the question, see the Appendix for more information.
  "answer": null,
  // The possible answers for this question when those possible answers are
  // necessary.  The presence of this parameter is dependent on permissions.
  "answers": null
}
```

## [Get all quiz submission questions.](#method.quizzes/quiz_submission_questions.index) [Quizzes::QuizSubmissionQuestionsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_submission_questions_controller.rb)

### GET /api/v1/quiz\_submissions/:quiz\_submission\_id/questions

**Scope:** 
`url:GET|/api/v1/quiz_submissions/:quiz_submission_id/questions`

Get a list of all the question records for this quiz submission.

**200 OK** response code is returned if the request was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Associations to include with the quiz submission question.  Allowed values: `quiz_question` |

#### Example Response:

#### 

```
{
  "quiz_submission_questions": [QuizSubmissionQuestion]
}
```

## [Answering questions](#method.quizzes/quiz_submission_questions.answer) [Quizzes::QuizSubmissionQuestionsController#answer](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_submission_questions_controller.rb)

### POST /api/v1/quiz\_submissions/:quiz\_submission\_id/questions

**Scope:** 
`url:POST|/api/v1/quiz_submissions/:quiz_submission_id/questions`

Provide or update an answer to one or more QuizQuestions.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| attempt | Required | integer | The attempt number of the quiz submission being taken. Note that this must be the latest attempt index, as questions for earlier attempts can not be modified. |
| validation\_token | Required | string | The unique validation token you received when the Quiz Submission was created. |
| access\_code |  | string | Access code for the Quiz, if any. |
| quiz\_questions[] |  | QuizSubmissionQuestion | Set of question IDs and the answer value.  See [Appendix: Question Answer Formats](quiz_submission_questions.html#Question+Answer+Formats-appendix "Appendix: Question Answer Formats") for the accepted answer formats for each question type. |

#### Example Request:

#### 

```
{
  "attempt": 1,
  "validation_token": "YOUR_VALIDATION_TOKEN",
  "access_code": null,
  "quiz_questions": [{
    "id": "1",
    "answer": "Hello World!"
  }, {
    "id": "2",
    "answer": 42.0
  }]
}
```

Returns a list of
[QuizSubmissionQuestion](quiz_submission_questions.html#QuizSubmissionQuestion)
objects

## [Get a formatted student numerical answer.](#method.quizzes/quiz_submission_questions.formatted_answer) [Quizzes::QuizSubmissionQuestionsController#formatted\_answer](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_submission_questions_controller.rb)

### GET /api/v1/quiz\_submissions/:quiz\_submission\_id/questions/:id/formatted\_answer

**Scope:** 
`url:GET|/api/v1/quiz_submissions/:quiz_submission_id/questions/:id/formatted_answer`

Matches the intended behavior of the UI when a numerical answer is entered and returns the resulting formatted number

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| answer | Required | Numeric | no description |

#### Example Response:

#### 

```
{
  "formatted_answer": 12.1234
}
```

## [Flagging a question.](#method.quizzes/quiz_submission_questions.flag) [Quizzes::QuizSubmissionQuestionsController#flag](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_submission_questions_controller.rb)

### PUT /api/v1/quiz\_submissions/:quiz\_submission\_id/questions/:id/flag

**Scope:** 
`url:PUT|/api/v1/quiz_submissions/:quiz_submission_id/questions/:id/flag`

Set a flag on a quiz question to indicate that you want to return to it later.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| attempt | Required | integer | The attempt number of the quiz submission being taken. Note that this must be the latest attempt index, as questions for earlier attempts can not be modified. |
| validation\_token | Required | string | The unique validation token you received when the Quiz Submission was created. |
| access\_code |  | string | Access code for the Quiz, if any. |

#### Example Request:

#### 

```
{
  "attempt": 1,
  "validation_token": "YOUR_VALIDATION_TOKEN",
  "access_code": null
}
```

## [Unflagging a question.](#method.quizzes/quiz_submission_questions.unflag) [Quizzes::QuizSubmissionQuestionsController#unflag](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_submission_questions_controller.rb)

### PUT /api/v1/quiz\_submissions/:quiz\_submission\_id/questions/:id/unflag

**Scope:** 
`url:PUT|/api/v1/quiz_submissions/:quiz_submission_id/questions/:id/unflag`

Remove the flag that you previously set on a quiz question after youâve returned to it.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| attempt | Required | integer | The attempt number of the quiz submission being taken. Note that this must be the latest attempt index, as questions for earlier attempts can not be modified. |
| validation\_token | Required | string | The unique validation token you received when the Quiz Submission was created. |
| access\_code |  | string | Access code for the Quiz, if any. |

#### Example Request:

#### 

```
{
  "attempt": 1,
  "validation_token": "YOUR_VALIDATION_TOKEN",
  "access_code": null
}
```