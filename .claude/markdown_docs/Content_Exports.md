# Content Exports

# Content Exports API



API for exporting courses and course content

### A ContentExport object looks like:

```
{
  // the unique identifier for the export
  "id": 101,
  // the date and time this export was requested
  "created_at": "2014-01-01T00:00:00Z",
  // the type of content migration: 'common_cartridge' or 'qti'
  "export_type": "common_cartridge",
  // attachment api object for the export package (not present before the export
  // completes or after it becomes unavailable for download.)
  "attachment": {"url":"https:\/\/example.com\/api\/v1\/attachments\/789?download_frd=1\u0026verifier=bG9sY2F0cyEh"},
  // The api endpoint for polling the current progress
  "progress_url": "https://example.com/api/v1/progress/4",
  // The ID of the user who started the export
  "user_id": 4,
  // Current state of the content migration: created exporting exported failed
  "workflow_state": "exported"
}
```

## [List content exports](#method.content_exports_api.index) [ContentExportsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_exports_api_controller.rb)

### GET /api/v1/courses/:course\_id/content\_exports

**Scope:** 
`url:GET|/api/v1/courses/:course_id/content_exports`

### GET /api/v1/groups/:group\_id/content\_exports

**Scope:** 
`url:GET|/api/v1/groups/:group_id/content_exports`

### GET /api/v1/users/:user\_id/content\_exports

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_exports`

A paginated list of the past and pending content export jobs for a course, group, or user. Exports are returned newest first.

Returns a list of
[ContentExport](content_exports.html#ContentExport)
objects

## [Show content export](#method.content_exports_api.show) [ContentExportsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_exports_api_controller.rb)

### GET /api/v1/courses/:course\_id/content\_exports/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/content_exports/:id`

### GET /api/v1/groups/:group\_id/content\_exports/:id

**Scope:** 
`url:GET|/api/v1/groups/:group_id/content_exports/:id`

### GET /api/v1/users/:user\_id/content\_exports/:id

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_exports/:id`

Get information about a single content export.

Returns a
[ContentExport](content_exports.html#ContentExport)
object

## [Export content](#method.content_exports_api.create) [ContentExportsApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_exports_api_controller.rb)

### POST /api/v1/courses/:course\_id/content\_exports

**Scope:** 
`url:POST|/api/v1/courses/:course_id/content_exports`

### POST /api/v1/groups/:group\_id/content\_exports

**Scope:** 
`url:POST|/api/v1/groups/:group_id/content_exports`

### POST /api/v1/users/:user\_id/content\_exports

**Scope:** 
`url:POST|/api/v1/users/:user_id/content_exports`

Begin a content export job for a course, group, or user.

You can use the [Progress API](progress.html#method.progress.show "Progress API") to track the progress of the export. The migrationâs progress is linked to with the *progress\_url* value.

When the export completes, use the [Show content export](content_exports.html#method.content_exports_api.show "Show content export") endpoint to retrieve a download URL for the exported content.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| export\_type | Required | string | âcommon\_cartridgeâ  Export the contents of the course in the Common Cartridge (.imscc) format  âqtiâ  Export quizzes from a course in the QTI format  âzipâ  Export files from a course, group, or user in a zip file  Allowed values: `common_cartridge`, `qti`, `zip` |
| skip\_notifications |  | boolean | Donât send the notifications about the export to the user. Default: false |
| select |  | Hash | The select parameter allows exporting specific data. The keys are object types like âfilesâ, âfoldersâ, âpagesâ, etc. The value for each key is a list of object ids. An id can be an integer or a string.  Multiple object types can be selected in the same call. However, not all object types are valid for every export\_type. Common Cartridge supports all object types. Zip and QTI only support the object types as described below.  âfoldersâ  Also supported for zip export\_type.  âfilesâ  Also supported for zip export\_type.  âquizzesâ  Also supported for qti export\_type.  Allowed values: `folders`, `files`, `attachments`, `quizzes`, `assignments`, `announcements`, `calendar_events`, `discussion_topics`, `modules`, `module_items`, `pages`, `rubrics` |

Returns a
[ContentExport](content_exports.html#ContentExport)
object