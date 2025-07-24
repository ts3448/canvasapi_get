# BlockEditorTemplate

# BlockEditorTemplate API



Block Editor Templates are pre-build templates that can be used to create pages.
The BlockEditorTemplate API allows you to create, retrieve, update, and delete templates.

### A BlockEditorTemplate object looks like:

```
{
  // the ID of the page
  "id": 1,
  // name of the template
  "name": "Navigation Bar",
  // description of the template
  "description": "A bar of links to other content",
  // the creation date for the template
  "created_at": "2012-08-06T16:46:33-06:00",
  // the date the template was last updated
  "updated_at": "2012-08-08T14:25:20-06:00",
  // The JSON data that is the template
  "node_tree": null,
  // The version of the editor that created the template
  "editor_version": "1.0",
  // The type of template. One of 'block', 'section', or 'page'
  "template_type": "page",
  // String indicating what state this assignment is in.
  "workflow_state": "unpublished"
}
```

## [List block templates](#method.block_editor_templates_api.index) [BlockEditorTemplatesApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/block_editor_templates_api_controller.rb)

### GET /api/v1/courses/:course\_id/block\_editor\_templates

**Scope:** 
`url:GET|/api/v1/courses/:course_id/block_editor_templates`

A list of the block templates available to the current user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| sort |  | string | Sort results by this field.  Allowed values: `name`, `created_at`, `updated_at` |
| order |  | string | The sorting order. Defaults to âascâ.  Allowed values: `asc`, `desc` |
| drafts |  | boolean | If true, include draft templates. If false or omitted only published templates will be returned. |
| type[] |  | string | What type of templates should be returned.  Allowed values: `page`, `section`, `block` |
| include[] |  | string | no description  Allowed values: `node_tree`, `thumbnail` |

#### Example Request:

#### 

```
curl -H 'Authorization: Bearer <token>' \
     https://<canvas>/api/v1/courses/123/block_editor_templates?sort=name&order=asc&drafts=true
```

Returns a list of
[BlockEditorTemplate](block_editor_template.html#BlockEditorTemplate)
objects