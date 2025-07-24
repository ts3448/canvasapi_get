# PollSubmissions

# PollSubmissions API



Manage submissions for polls

### A PollSubmission object looks like:

```
{
  // The unique identifier for the poll submission.
  "id": 1023,
  // The unique identifier of the poll choice chosen for this submission.
  "poll_choice_id": 155,
  // the unique identifier of the user who submitted this poll submission.
  "user_id": 4555,
  // The date and time the poll submission was submitted.
  "created_at": "2013-11-07T13:16:18Z"
}
```

## [Get a single poll submission](#method.polling/poll_submissions.show) [Polling::PollSubmissionsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_submissions_controller.rb)

### GET /api/v1/polls/:poll\_id/poll\_sessions/:poll\_session\_id/poll\_submissions/:id

**Scope:** 
`url:GET|/api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions/:id`

Returns the poll submission with the given id

#### Example Response:

#### 

```
{
  "poll_submissions": [PollSubmission]
}
```

## [Create a single poll submission](#method.polling/poll_submissions.create) [Polling::PollSubmissionsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/polling/poll_submissions_controller.rb)

### POST /api/v1/polls/:poll\_id/poll\_sessions/:poll\_session\_id/poll\_submissions

**Scope:** 
`url:POST|/api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions`

Create a new poll submission for this poll session

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| poll\_submissions[][poll\_choice\_id] | Required | integer | The chosen poll choice for this submission. |

#### Example Response:

#### 

```
{
  "poll_submissions": [PollSubmission]
}
```