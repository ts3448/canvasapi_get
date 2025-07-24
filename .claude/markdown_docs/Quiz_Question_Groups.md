# Quiz Question Groups

# Quiz Question Groups API



API for accessing information on quiz question groups

### A QuizGroup object looks like:

```
{
  // The ID of the question group.
  "id": 1,
  // The ID of the Quiz the question group belongs to.
  "quiz_id": 2,
  // The name of the question group.
  "name": "Fraction questions",
  // The number of questions to pick from the group to display to the student.
  "pick_count": 3,
  // The amount of points allotted to each question in the group.
  "question_points": 10,
  // The ID of the Assessment question bank to pull questions from.
  "assessment_question_bank_id": 2,
  // The order in which the question group will be retrieved and displayed.
  "position": 1
}
```

## [Get a single quiz group](#method.quizzes/quiz_groups.show) [Quizzes::QuizGroupsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_groups_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes/:quiz\_id/groups/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id`

Returns details of the quiz group with the given id.

Returns a
[QuizGroup](quiz_question_groups.html#QuizGroup)
object

## [Create a question group](#method.quizzes/quiz_groups.create) [Quizzes::QuizGroupsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_groups_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes/:quiz\_id/groups

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes/:quiz_id/groups`

Create a new question group for this quiz

**201 Created** response code is returned if the creation was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz\_groups[][name] |  | string | The name of the question group. |
| quiz\_groups[][pick\_count] |  | integer | The number of questions to randomly select for this group. |
| quiz\_groups[][question\_points] |  | integer | The number of points to assign to each question in the group. |
| quiz\_groups[][assessment\_question\_bank\_id] |  | integer | The id of the assessment question bank to pull questions from. |

#### Example Response:

#### 

```
{
  "quiz_groups": [QuizGroup]
}
```

## [Update a question group](#method.quizzes/quiz_groups.update) [Quizzes::QuizGroupsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_groups_controller.rb)

### PUT /api/v1/courses/:course\_id/quizzes/:quiz\_id/groups/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id`

Update a question group

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| quiz\_groups[][name] |  | string | The name of the question group. |
| quiz\_groups[][pick\_count] |  | integer | The number of questions to randomly select for this group. |
| quiz\_groups[][question\_points] |  | integer | The number of points to assign to each question in the group. |

#### Example Response:

#### 

```
{
  "quiz_groups": [QuizGroup]
}
```

## [Delete a question group](#method.quizzes/quiz_groups.destroy) [Quizzes::QuizGroupsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_groups_controller.rb)

### DELETE /api/v1/courses/:course\_id/quizzes/:quiz\_id/groups/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id`

Delete a question group

<b>204 No Content<b> response code is returned if the deletion was successful.

## [Reorder question groups](#method.quizzes/quiz_groups.reorder) [Quizzes::QuizGroupsController#reorder](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_groups_controller.rb)

### POST /api/v1/courses/:course\_id/quizzes/:quiz\_id/groups/:id/reorder

**Scope:** 
`url:POST|/api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id/reorder`

Change the order of the quiz questions within the group

<b>204 No Content<b> response code is returned if the reorder was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| order[][id] | Required | integer | The associated itemâs unique identifier |
| order[][type] |  | string | The type of item is always âquestionâ for a group  Allowed values: `question` |