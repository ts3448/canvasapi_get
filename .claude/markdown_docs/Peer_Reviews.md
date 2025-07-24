# Peer Reviews

# Peer Reviews API



### A PeerReview object looks like:

```
{
  // The assessors user id
  "assessor_id": 23,
  // The id for the asset associated with this Peer Review
  "asset_id": 13,
  // The type of the asset
  "asset_type": "Submission",
  // The id of the Peer Review
  "id": 1,
  // The user id for the owner of the asset
  "user_id": 7,
  // The state of the Peer Review, either 'assigned' or 'completed'
  "workflow_state": "assigned",
  // the User object for the owner of the asset if the user include parameter is
  // provided (see user API) (optional)
  "user": "User",
  // The User object for the assessor if the user include parameter is provided
  // (see user API) (optional)
  "assessor": "User",
  // The submission comments associated with this Peer Review if the
  // submission_comment include parameter is provided (see submissions API)
  // (optional)
  "submission_comments": "SubmissionComment"
}
```

## [Get all Peer Reviews](#method.peer_reviews_api.index) [PeerReviewsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/peer_reviews_api_controller.rb)

### GET /api/v1/courses/:course\_id/assignments/:assignment\_id/peer\_reviews

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews`

### GET /api/v1/sections/:section\_id/assignments/:assignment\_id/peer\_reviews

**Scope:** 
`url:GET|/api/v1/sections/:section_id/assignments/:assignment_id/peer_reviews`

### GET /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:GET|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

### GET /api/v1/sections/:section\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:GET|/api/v1/sections/:section_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

Get a list of all Peer Reviews for this assignment

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Associations to include with the peer review.  Allowed values: `submission_comments`, `user` |

Returns a list of
[PeerReview](peer_reviews.html#PeerReview)
objects

## [Create Peer Review](#method.peer_reviews_api.create) [PeerReviewsApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/peer_reviews_api_controller.rb)

### POST /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:POST|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

### POST /api/v1/sections/:section\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:POST|/api/v1/sections/:section_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

Create a peer review for the assignment

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id | Required | integer | user\_id to assign as reviewer on this assignment |

Returns a
[PeerReview](peer_reviews.html#PeerReview)
object

## [Delete Peer Review](#method.peer_reviews_api.destroy) [PeerReviewsApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/peer_reviews_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

### DELETE /api/v1/sections/:section\_id/assignments/:assignment\_id/submissions/:submission\_id/peer\_reviews

**Scope:** 
`url:DELETE|/api/v1/sections/:section_id/assignments/:assignment_id/submissions/:submission_id/peer_reviews`

Delete a peer review for the assignment

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id | Required | integer | user\_id to delete as reviewer on this assignment |

Returns a
[PeerReview](peer_reviews.html#PeerReview)
object