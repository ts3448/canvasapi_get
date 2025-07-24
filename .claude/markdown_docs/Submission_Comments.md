# Submission Comments

# Submission Comments API



This API can be used to edit and delete submission comments.

## [Edit a submission comment](#method.submission_comments_api.update) [SubmissionCommentsApiController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/submission_comments_api_controller.rb)

### PUT /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:user\_id/comments/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/:id`

Edit the given submission comment.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| comment |  | string | If this argument is present, edit the text of a comment. |

Returns a
[SubmissionComment](submissions.html#SubmissionComment)
object

## [Delete a submission comment](#method.submission_comments_api.destroy) [SubmissionCommentsApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/submission_comments_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:user\_id/comments/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/:id`

Delete the given submission comment.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/assignments/<assignment_id>/submissions/<user_id>/comments/<id> \
     -X DELETE \
     -H 'Authorization: Bearer <token>'
```

Returns a
[SubmissionComment](submissions.html#SubmissionComment)
object

## [Upload a file](#method.submission_comments_api.create_file) [SubmissionCommentsApiController#create\_file](https://github.com/instructure/canvas-lms/blob/master/app/controllers/submission_comments_api_controller.rb)

### POST /api/v1/courses/:course\_id/assignments/:assignment\_id/submissions/:user\_id/comments/files

**Scope:** 
`url:POST|/api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files`

Upload a file to attach to a submission comment

See the [File Upload Documentation](file_uploads.html "File Upload Documentation") for details on the file upload workflow.

The final step of the file upload workflow will return the attachment data, including the new file id. The caller can then PUT the file\_id to the submission API to attach it to a comment