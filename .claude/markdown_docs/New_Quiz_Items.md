# New Quiz Items

# New Quiz Items API



API for accessing and building items inside a New Quiz. To interact with the quiz itself,
see the [New Quizzes API](/doc/api/new_quizzes.html).

Glossary:

**Quiz Items** can be among several types as described here. For now, all types can be retrieved (GET), but some types are
restricted to only that functionality.

**QuestionItem**: question items are the various question types allowed for Quizzes. These question types can be
created, updated, retrieved, and deleted with the API. See the Appendix for more details.

**StimulusItem**: stimulus items are quiz items that define a stimulus that can have associated questions attached to
it. For now, stimulus items can only be retrieved with the API. They must be created and updated via the UI.

**BankItem**: bank items are quiz questions or other items that are part of an item bank. For now, bank items can only
be retrieved with the API. They must be created and updated via the UI.

**BankEntry**: bank entry items allow for a random selection of items from an associated bank to be included in the
quiz. For now, bank items can only be retrieved with the API. They must be created and updated via the UI.

### A QuizItem object looks like:

```
// Individual items within a quiz, whether they're questions, stimuli, banked
// content, or question banks.
{
  // the ID of the quiz item
  "id": "35",
  // the position of the item within the quiz. The first item in a quiz is given
  // position 1.
  "position": 2,
  // the number of points available to score on this item
  "points_possible": 10.0,
  // the type of the item. One of 'Item', 'Stimulus', 'BankEntry', or 'Bank'.
  "entry_type": "Item",
  // whether the current user can edit the item -- used internally, no need to set
  "entry_editable": true,
  // the ID of the stimulus that this item is associated with. null if not
  // associated with any stimuli.
  "stimulus_quiz_entry_id": "3",
  // status of the item. one of 'mutable' or 'immutable'.  Used internally, no
  // need to set
  "status": "mutable",
  // additional properties for the item (currently only populated by items with a
  // BankItem entry)
  "properties": null,
  // the specific data associated with the quiz item.  These items can be either a
  // QuestionItem, StimulusItem, BankEntryItem, or BankItem, depending on
  // entry_type, and are defined
  // separately
  "entry": null
}
```

### A QuestionItem object looks like:

```
{
  // the question title
  "title": "Linear Algebra 1-104",
  // the question content (can include html for rich content)
  "item_body": "<p>What is 3 + 6?</p>",
  // type of calculator the user will have access to during the question ('none',
  // basic' or 'scientific')
  "calculator_type": "none",
  // correct, incorrect, and general feedback for the question (see
  // QuestionFeedback)
  "feedback": null,
  // can be thought of as the question type. One of 'multi-answer', 'matching',
  // 'categorization',
  // 'file-upload', 'formula', 'ordering', 'rich-fill-blank', 'hot-spot',
  // 'choice', 'numeric', 'true-false',
  // 'essay', or 'fill-blank' (deprecated). See Appendix: Question Types for more
  // info about each type.
  "interaction_type_slug": "essay",
  // an object that contains the question data. See Appendix: Question Types for
  // more info about this field.
  "interaction_data": null,
  // an object that contains additional properties for some question types. See
  // Appendix: Question Types for more info about this field.
  "properties": null,
  // describes how to score the question. See Appendix: Question Types for more
  // info about this field.
  "scoring_data": null,
  // feedback provided for each answer (rich content, only available on 'choice'
  // question types)
  "answer_feedback": {"5595b4c2-7dd6-447f-b8f1-9b6d0e0c287a":"\u003cp\u003eClose, but in this case...\u003c\/p\u003e"},
  // the algorithm used to score the question. See Appendix: Question Types for
  // more info about this field.
  "scoring_algorithm": "AllOrNothing"
}
```

### A StimulusItem object looks like:

```
{
  // stimulus title
  "title": "Consider the following image",
  // stimulus content (rich content)
  "body": "<img src=... />",
  // additional stimulus instructions
  "instructions": "Some instructions...",
  // optional URL; not visible to students
  "source_url": "https://example.com",
  // where the stimulus appears relative to questions ('top' or 'left')
  "orientation": "left",
  // if the stimulus is treated as a passage (text - no question block)
  "passage": false
}
```

### A BankEntryItem object looks like:

```
{
  // the type of the item. Either 'Item' or 'Stimulus'.
  "entry_type": "Item",
  // whether the banked item is archived
  "archived": false,
  // the item (either a QuestionItem or StimulusItem, depending on entry_type)
  "entry": null
}
```

### A BankItem object looks like:

```
{
  // the title of the bank
  "title": "Linear Algebra 1-1",
  // whether the bank is archived
  "archived": false,
  // the number of items in the bank, including stimuli
  "entry_count": 20,
  // the number of items in the bank, excluding stimuli
  "item_entry_count": 18
}
```

### An ItemProperties object looks like:

```
{
  // for items with a BankItem entry - the number of items to randomly select from
  // the bank. null if all items should be included.
  "sample_num": 5
}
```

### A QuestionFeedback object looks like:

```
{
  // general feedback to show regardless of answer (rich content)
  "neutral": "<p>That was a hard one.</p>",
  // feedback to show if the question is answered correctly (rich content)
  "correct": "<p>Nice work!</p>",
  // feedback to show if the question is answered incorrectly (rich content)
  "incorrect": "<p>Remember to start by...</p>"
}
```

## [Get a quiz item](#method.new_quizzes/quiz_items_api.show)

### GET /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items/:item\_id

**Scope:** 
`url:GET|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items/:item_id`

Get details about a single item in a new quiz.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | The id of the assignment associated with the quiz. |
| item\_id | Required | integer | The id of the item associated with the quiz. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/12/items/123' \
      -H 'Authorization: Bearer <token>'
```

Returns a
[QuizItem](new_quiz_items.html#QuizItem)
object

## [List quiz items](#method.new_quizzes/quiz_items_api.index)

### GET /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items

**Scope:** 
`url:GET|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items`

Get a list of items in a new quiz.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | no description |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/1/items' \
     -H 'Authorization Bearer <token>'
```

Returns a list of
[QuizItem](new_quiz_items.html#QuizItem)
objects

## [Create a quiz item](#method.new_quizzes/quiz_items_api.create)

### POST /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items

**Scope:** 
`url:POST|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items`

Create a quiz item in a new quiz. Only `QuestionItem` types can be created.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | The id of the assignment associated with the quiz. |
| item[position] |  | integer | The position of the item within the quiz. |
| item[points\_possible] |  | number | The number of points available to score on this item. Must be positive. |
| item[entry\_type] | Required | string | The type of the item.  Allowed values: `Item` |
| item[entry][title] |  | string | The question title. |
| item[entry][item\_body] | Required | string | The question stem (rich content). |
| item[entry][calculator\_type] |  | string | Type of calculator the user will have access to during the question.  Allowed values: `none`, `basic`, `scientific` |
| item[entry][feedback][neutral] |  | string | General feedback to show regardless of answer (rich content). |
| item[entry][feedback][correct] |  | string | Feedback to show if the question is answered correctly (rich content). |
| item[entry][feedback][incorrect] |  | string | Feedback to show if the question is answered incorrectly (rich content). |
| item[entry][interaction\_type\_slug] | Required | string | The type of question. One of âmulti-answerâ, âmatchingâ, âcategorizationâ, âfile-uploadâ, âformulaâ, âorderingâ, ârich-fill-blankâ, âhot-spotâ, âchoiceâ, ânumericâ, âtrue-falseâ, or âessayâ. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about each type. |
| item[entry][interaction\_data] | Required | Object | An object that contains the question data. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][properties] |  | Object | An object that contains additional properties for some question types. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][scoring\_data] | Required | Object | An object that describes how to score the question. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][answer\_feedback] |  | Object | Feedback provided for each answer (rich content, only available on âchoiceâ question types). |
| item[entry][scoring\_algorithm] | Required | string | The algorithm used to score the question. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/12/items' \
     -X POST \
     -H 'Authorization Bearer <token>' \
     -d 'item[position]=1' \
     -d 'item[points_possible]=25.0' \
     -d 'item[properties]={}' \
     -d 'item[entry_type]=Item' \
     -d 'item[entry][title]=Question 1' \
     -d 'item[entry][feedback][correct]=good job!' \
     -d 'item[entry][calculator_type]=none' \
     -d 'item[entry][interaction_data][word_limit_enabled]=true' \
     -d 'item[entry][item_body]=<p>What is 3 ^ 6?</p>' \
     -d 'item[entry][interaction_type_slug]=essay' \
     -d 'item[entry][scoring_data][value]=' \
     -d 'item[entry][scoring_algorithm]=None'
```

Returns a
[QuizItem](new_quiz_items.html#QuizItem)
object

## [Update a quiz item](#method.new_quizzes/quiz_items_api.update)

### PATCH /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items/:item\_id

**Scope:** 
`url:PATCH|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items/:item_id`

Update a single quiz item in a new quiz. Only `QuestionItem` types can be updated.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | The id of the assignment associated with the quiz. |
| item\_id | Required | integer | The id of the item associated with the quiz. |
| item[position] |  | integer | The position of the item within the quiz. |
| item[points\_possible] |  | number | The number of points available to score on this item. Must be positive. |
| item[entry\_type] |  | string | The type of the item.  Allowed values: `Item` |
| item[entry][title] |  | string | The question title. |
| item[entry][item\_body] |  | string | The question stem (rich content). |
| item[entry][calculator\_type] |  | string | Type of calculator the user will have access to during the question.  Allowed values: `none`, `basic`, `scientific` |
| item[entry][feedback][neutral] |  | string | General feedback to show regardless of answer (rich content). |
| item[entry][feedback][correct] |  | string | Feedback to show if the question is answered correctly (rich content). |
| item[entry][feedback][incorrect] |  | string | Feedback to show if the question is answered incorrectly (rich content). |
| item[entry][interaction\_type\_slug] |  | string | The type of question. One of âmulti-answerâ, âmatchingâ, âcategorizationâ, âfile-uploadâ, âformulaâ, âorderingâ, ârich-fill-blankâ, âhot-spotâ, âchoiceâ, ânumericâ, âtrue-falseâ, or âessayâ. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about each type. |
| item[entry][interaction\_data] |  | Object | An object that contains the question data. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][properties] |  | Object | An object that contains additional properties for some question types. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][scoring\_data] |  | Object | An object that describes how to score the question. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |
| item[entry][answer\_feedback] |  | Object | Feedback provided for each answer (rich content, only available on âchoiceâ question types). |
| item[entry][scoring\_algorithm] |  | string | The algorithm used to score the question. See [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more info about this field. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/12/items/145' \
     -X PATCH \
     -H 'Authorization Bearer <token>' \
     -d 'item[points_possible]=25.0' \
     -d 'item[entry][title]=Question 1' \
     -d 'item[entry][calculator_type]=scientific'
```

Returns a
[QuizItem](new_quiz_items.html#QuizItem)
object

## [Delete a quiz item](#method.new_quizzes/quiz_items_api.destroy)

### DELETE /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items/:item\_id

**Scope:** 
`url:DELETE|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items/:item_id`

Delete a single quiz item in a new quiz.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | The id of the assignment associated with the quiz. |
| item\_id | Required | integer | The id of the item associated with the quiz. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/12/items/123' \
     -X DELETE \
     -H 'Authorization: Bearer <token>'
```

Returns a
[QuizItem](new_quiz_items.html#QuizItem)
object

## [Get items media\_upload\_url](#method.new_quizzes/quiz_items_api.media_upload_url)

### GET /api/quiz/v1/courses/:course\_id/quizzes/:assignment\_id/items/media\_upload\_url

**Scope:** 
`url:GET|/api/quiz/v1/courses/:course_id/quizzes/:assignment_id/items/media_upload_url`

Get a url for uploading media for use in hot-spot question types. See the hot-spot question type in the [Appendix: Question Types](new_quiz_items.html#Question+Types-appendix "Appendix: Question Types") for more details about using this endpoint.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id | Required | integer | no description |
| assignment\_id | Required | integer | no description |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/quiz/v1/courses/1/quizzes/1/items/media_upload_url' \
     -H 'Authorization Bearer <token>'
```

#### Example Response:

#### 

```
{ "url": "http://s3_upload_url" }
```