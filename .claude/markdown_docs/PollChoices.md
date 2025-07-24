# PollChoices

# PollChoices API



Manage choices for polls

### A PollChoice object looks like:

```
{
  // The unique identifier for the poll choice.
  "id": 1023,
  // The id of the poll this poll choice belongs to.
  "poll_id": 1779,
  // Specifies whether or not this poll choice is a 'correct' choice.
  "is_correct": true,
  // The text of the poll choice.
  "text": "Choice A",
  // The order of the poll choice in relation to it's sibling poll choices.
  "position": 1
}
```

## [List poll choices in a poll](#method.polling/poll_choices.index) [Polling::PollChoicesController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_choices_controller.rb)

### GET /api/v1/polls/:poll\_id/poll\_choices

**Scope:** 
`url:GET|/api/v1/polls/:poll_id/poll_choices`

Returns the paginated list of PollChoices in this poll.

#### Example Response:

#### 

```
{
  "poll_choices": [PollChoice]
}
```

## [Get a single poll choice](#method.polling/poll_choices.show) [Polling::PollChoicesController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_choices_controller.rb)

### GET /api/v1/polls/:poll\_id/poll\_choices/:id

**Scope:** 
`url:GET|/api/v1/polls/:poll_id/poll_choices/:id`

Returns the poll choice with the given id

#### Example Response:

#### 

```
{
  "poll_choices": [PollChoice]
}
```

## [Create a single poll choice](#method.polling/poll_choices.create) [Polling::PollChoicesController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_choices_controller.rb)

### POST /api/v1/polls/:poll\_id/poll\_choices

**Scope:** 
`url:POST|/api/v1/polls/:poll_id/poll_choices`

Create a new poll choice for this poll

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| poll\_choices[][text] | Required | string | The descriptive text of the poll choice. |
| poll\_choices[][is\_correct] |  | boolean | Whether this poll choice is considered correct or not. Defaults to false. |
| poll\_choices[][position] |  | integer | The order this poll choice should be returned in the context itâs sibling poll choices. |

#### Example Response:

#### 

```
{
  "poll_choices": [PollChoice]
}
```

## [Update a single poll choice](#method.polling/poll_choices.update) [Polling::PollChoicesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_choices_controller.rb)

### PUT /api/v1/polls/:poll\_id/poll\_choices/:id

**Scope:** 
`url:PUT|/api/v1/polls/:poll_id/poll_choices/:id`

Update an existing poll choice for this poll

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| poll\_choices[][text] | Required | string | The descriptive text of the poll choice. |
| poll\_choices[][is\_correct] |  | boolean | Whether this poll choice is considered correct or not. Defaults to false. |
| poll\_choices[][position] |  | integer | The order this poll choice should be returned in the context itâs sibling poll choices. |

#### Example Response:

#### 

```
{
  "poll_choices": [PollChoice]
}
```

## [Delete a poll choice](#method.polling/poll_choices.destroy) [Polling::PollChoicesController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_choices_controller.rb)

### DELETE /api/v1/polls/:poll\_id/poll\_choices/:id

**Scope:** 
`url:DELETE|/api/v1/polls/:poll_id/poll_choices/:id`

**204 No Content** response code is returned if the deletion was successful.