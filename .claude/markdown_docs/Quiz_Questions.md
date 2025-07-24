# Quiz Questions

# Quiz Questions API



### A QuizQuestion object looks like:

```
{
  // The ID of the quiz question.
  "id": 1,
  // The ID of the Quiz the question belongs to.
  "quiz_id": 2,
  // The order in which the question will be retrieved and displayed.
  "position": 1,
  // The name of the question.
  "question_name": "Prime Number Identification",
  // The type of the question.
  "question_type": "multiple_choice_question",
  // The text of the question.
  "question_text": "Which of the following is NOT a prime number?",
  // The maximum amount of points possible received for getting this question
  // correct.
  "points_possible": 5,
  // The comments to display if the student answers the question correctly.
  "correct_comments": "That's correct!",
  // The comments to display if the student answers incorrectly.
  "incorrect_comments": "Unfortunately, that IS a prime number.",
  // The comments to display regardless of how the student answered.
  "neutral_comments": "Goldbach's conjecture proposes that every even integer greater than 2 can be expressed as the sum of two prime numbers.",
  // An array of available answers to display to the student.
  "answers": null
}
```

### An Answer object looks like:

```
{
  // The unique identifier for the answer.  Do not supply if this answer is part
  // of a new question
  "id": 6656,
  // The text of the answer.
  "answer_text": "Constantinople",
  // An integer to determine correctness of the answer. Incorrect answers should
  // be 0, correct answers should be 100.
  "answer_weight": 100,
  // Specific contextual comments for a particular answer.
  "answer_comments": "Remember to check your spelling prior to submitting this answer.",
  // Used in missing word questions.  The text to follow the missing word
  "text_after_answers": " is the capital of Utah.",
  // Used in matching questions.  The static value of the answer that will be
  // displayed on the left for students to match for.
  "answer_match_left": "Salt Lake City",
  // Used in matching questions. The correct match for the value given in
  // answer_match_left.  Will be displayed in a dropdown with the other
  // answer_match_right values..
  "answer_match_right": "Utah",
  // Used in matching questions. A list of distractors, delimited by new lines (
  // ) that will be seeded with all the answer_match_right values.
  "matching_answer_incorrect_matches": "Nevada
  California
  Washington",
  // Used in numerical questions.  Values can be 'exact_answer', 'range_answer',
  // or 'precision_answer'.
  "numerical_answer_type": "exact_answer",
  // Used in numerical questions of type 'exact_answer'.  The value the answer
  // should equal.
  "exact": 42,
  // Used in numerical questions of type 'exact_answer'. The margin of error
  // allowed for the student's answer.
  "margin": 4,
  // Used in numerical questions of type 'precision_answer'.  The value the answer
  // should equal.
  "approximate": 1234600000.0,
  // Used in numerical questions of type 'precision_answer'. The numerical
  // precision that will be used when comparing the student's answer.
  "precision": 4,
  // Used in numerical questions of type 'range_answer'. The start of the allowed
  // range (inclusive).
  "start": 1,
  // Used in numerical questions of type 'range_answer'. The end of the allowed
  // range (inclusive).
  "end": 10,
  // Used in fill in multiple blank and multiple dropdowns questions.
  "blank_id": 1170
}
```

## [List questions in a quiz or a submission](#method.quizzes/quiz_questions.index) [Quizzes::QuizQuestionsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_questions_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes/:quiz\_id/questions

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes/:quiz_id/questions`

Returns the paginated list of QuizQuestions in this quiz.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz\_submission\_id |  | integer | If specified, the endpoint will return the questions that were presented for that submission. This is useful if the quiz has been modified after the submission was created and the latest quiz versionâs set of questions does not match the submissionâs. NOTE: you must specify quiz\_submission\_attempt as well if you specify this parameter. |
| quiz\_submission\_attempt |  | integer | The attempt of the submission you want the questions for. |

Returns a list of
[QuizQuestion](quiz_questions.html#QuizQuestion)
objects

## [Get a single quiz question](#method.quizzes/quiz_questions.show) [Quizzes::QuizQuestionsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_questions_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes/:quiz\_id/questions/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id`

Returns the quiz question with the given id

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id | Required | integer | The quiz question unique identifier. |

Returns a
[QuizQuestion](quiz_questions.html#QuizQuestion)
object

## [Create a single quiz question](#method.quizzes/quiz_questions.create) [Quizzes::QuizQuestionsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_questions_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes/:quiz\_id/questions

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes/:quiz_id/questions`

Create a new quiz question for this quiz

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| question[question\_name] |  | string | The name of the question. |
| question[question\_text] |  | string | The text of the question. |
| question[quiz\_group\_id] |  | integer | The id of the quiz group to assign the question to. |
| question[question\_type] |  | string | The type of question. Multiple optional fields depend upon the type of question to be used.  Allowed values: `calculated_question`, `essay_question`, `file_upload_question`, `fill_in_multiple_blanks_question`, `matching_question`, `multiple_answers_question`, `multiple_choice_question`, `multiple_dropdowns_question`, `numerical_question`, `short_answer_question`, `text_only_question`, `true_false_question` |
| question[position] |  | integer | The order in which the question will be displayed in the quiz in relation to other questions. |
| question[points\_possible] |  | integer | The maximum amount of points received for answering this question correctly. |
| question[correct\_comments] |  | string | The comment to display if the student answers the question correctly. |
| question[incorrect\_comments] |  | string | The comment to display if the student answers incorrectly. |
| question[neutral\_comments] |  | string | The comment to display regardless of how the student answered. |
| question[text\_after\_answers] |  | string | no description |
| question[answers] |  | [Answer] | no description |

Returns a
[QuizQuestion](quiz_questions.html#QuizQuestion)
object

## [Update an existing quiz question](#method.quizzes/quiz_questions.update) [Quizzes::QuizQuestionsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_questions_controller.rb)

### PUT /api/v1/courses/:course\_id/quizzes/:quiz\_id/questions/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id`

Updates an existing quiz question for this quiz

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz\_id | Required | integer | The associated quizâs unique identifier. |
| id | Required | integer | The quiz questionâs unique identifier. |
| question[question\_name] |  | string | The name of the question. |
| question[question\_text] |  | string | The text of the question. |
| question[quiz\_group\_id] |  | integer | The id of the quiz group to assign the question to. |
| question[question\_type] |  | string | The type of question. Multiple optional fields depend upon the type of question to be used.  Allowed values: `calculated_question`, `essay_question`, `file_upload_question`, `fill_in_multiple_blanks_question`, `matching_question`, `multiple_answers_question`, `multiple_choice_question`, `multiple_dropdowns_question`, `numerical_question`, `short_answer_question`, `text_only_question`, `true_false_question` |
| question[position] |  | integer | The order in which the question will be displayed in the quiz in relation to other questions. |
| question[points\_possible] |  | integer | The maximum amount of points received for answering this question correctly. |
| question[correct\_comments] |  | string | The comment to display if the student answers the question correctly. |
| question[incorrect\_comments] |  | string | The comment to display if the student answers incorrectly. |
| question[neutral\_comments] |  | string | The comment to display regardless of how the student answered. |
| question[text\_after\_answers] |  | string | no description |
| question[answers] |  | [Answer] | no description |

Returns a
[QuizQuestion](quiz_questions.html#QuizQuestion)
object

## [Delete a quiz question](#method.quizzes/quiz_questions.destroy) [Quizzes::QuizQuestionsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_questions_controller.rb)

### DELETE /api/v1/courses/:course\_id/quizzes/:quiz\_id/questions/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id`

**204 No Content** response code is returned if the deletion was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz\_id | Required | integer | The associated quizâs unique identifier |
| id | Required | integer | The quiz questionâs unique identifier |