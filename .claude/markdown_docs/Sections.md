# Sections

# Sections API



API for accessing section information.

### A Section object looks like:

```
{
  // The unique identifier for the section.
  "id": 1,
  // The name of the section.
  "name": "Section A",
  // The sis id of the section. This field is only included if the user has
  // permission to view SIS information.
  "sis_section_id": "s34643",
  // Optional: The integration ID of the section. This field is only included if
  // the user has permission to view SIS information.
  "integration_id": "3452342345",
  // The unique identifier for the SIS import if created through SIS. This field
  // is only included if the user has permission to manage SIS information.
  "sis_import_id": 47,
  // The unique Canvas identifier for the course in which the section belongs
  "course_id": 7,
  // The unique SIS identifier for the course in which the section belongs. This
  // field is only included if the user has permission to view SIS information.
  "sis_course_id": "7",
  // the start date for the section, if applicable
  "start_at": "2012-06-01T00:00:00-06:00",
  // the end date for the section, if applicable
  "end_at": null,
  // Restrict user enrollments to the start and end dates of the section
  "restrict_enrollments_to_section_dates": null,
  // The unique identifier of the original course of a cross-listed section
  "nonxlist_course_id": null,
  // optional: the total number of active and invited students in the section
  "total_students": 13
}
```

## [List course sections](#method.sections.index) [SectionsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### GET /api/v1/courses/:course\_id/sections

**Scope:** 
`url:GET|/api/v1/courses/:course_id/sections`

A paginated list of the list of sections for this course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âstudentsâ: Associations to include with the group. Note: this is only available if you have permission to view users or grades in the course * âavatar\_urlâ: Include the avatar URLs for students returned. * âenrollmentsâ: If âstudentsâ is also included, return the section enrollment for each student * âtotal\_studentsâ: Returns the total amount of active and invited students for the course section * âpassback\_statusâ: Include the grade passback status. * âpermissionsâ: Include whether section grants :manage\_calendar permission to the caller   Allowed values: `students`, `avatar_url`, `enrollments`, `total_students`, `passback_status`, `permissions` |
| search\_term |  | string | When included, searches course sections for the term. Returns only matching results. Term must be at least 2 characters. |

Returns a list of
[Section](sections.html#Section)
objects

## [Create course section](#method.sections.create) [SectionsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### POST /api/v1/courses/:course\_id/sections

**Scope:** 
`url:POST|/api/v1/courses/:course_id/sections`

Creates a new section for this course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_section[name] |  | string | The name of the section |
| course\_section[sis\_section\_id] |  | string | The sis ID of the section. Must have manage\_sis permission to set. This is ignored if caller does not have permission to set. |
| course\_section[integration\_id] |  | string | The integration\_id of the section. Must have manage\_sis permission to set. This is ignored if caller does not have permission to set. |
| course\_section[start\_at] |  | DateTime | Section start date in ISO8601 format, e.g. 2011-01-01T01:00Z |
| course\_section[end\_at] |  | DateTime | Section end date in ISO8601 format. e.g. 2011-01-01T01:00Z |
| course\_section[restrict\_enrollments\_to\_section\_dates] |  | boolean | Set to true to restrict user enrollments to the start and end dates of the section. |
| enable\_sis\_reactivation |  | boolean | When true, will first try to re-activate a deleted section with matching sis\_section\_id if possible. |

Returns a
[Section](sections.html#Section)
object

## [Cross-list a Section](#method.sections.crosslist) [SectionsController#crosslist](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### POST /api/v1/sections/:id/crosslist/:new\_course\_id

**Scope:** 
`url:POST|/api/v1/sections/:id/crosslist/:new_course_id`

Move the Section to another course. The new course may be in a different account (department), but must belong to the same root account (institution).

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |

Returns a
[Section](sections.html#Section)
object

## [De-cross-list a Section](#method.sections.uncrosslist) [SectionsController#uncrosslist](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### DELETE /api/v1/sections/:id/crosslist

**Scope:** 
`url:DELETE|/api/v1/sections/:id/crosslist`

Undo cross-listing of a Section, returning it to its original course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |

Returns a
[Section](sections.html#Section)
object

## [Edit a section](#method.sections.update) [SectionsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### PUT /api/v1/sections/:id

**Scope:** 
`url:PUT|/api/v1/sections/:id`

Modify an existing section.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_section[name] |  | string | The name of the section |
| course\_section[sis\_section\_id] |  | string | The sis ID of the section. Must have manage\_sis permission to set. |
| course\_section[integration\_id] |  | string | The integration\_id of the section. Must have manage\_sis permission to set. |
| course\_section[start\_at] |  | DateTime | Section start date in ISO8601 format, e.g. 2011-01-01T01:00Z |
| course\_section[end\_at] |  | DateTime | Section end date in ISO8601 format. e.g. 2011-01-01T01:00Z |
| course\_section[restrict\_enrollments\_to\_section\_dates] |  | boolean | Set to true to restrict user enrollments to the start and end dates of the section. |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |

Returns a
[Section](sections.html#Section)
object

## [Get section information](#method.sections.show) [SectionsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### GET /api/v1/courses/:course\_id/sections/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/sections/:id`

### GET /api/v1/sections/:id

**Scope:** 
`url:GET|/api/v1/sections/:id`

Gets details about a specific section

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âstudentsâ: Associations to include with the group. Note: this is only available if you have permission to view users or grades in the course * âavatar\_urlâ: Include the avatar URLs for students returned. * âenrollmentsâ: If âstudentsâ is also included, return the section enrollment for each student * âtotal\_studentsâ: Returns the total amount of active and invited students for the course section * âpassback\_statusâ: Include the grade passback status. * âpermissionsâ: Include whether section grants :manage\_calendar permission to the caller   Allowed values: `students`, `avatar_url`, `enrollments`, `total_students`, `passback_status`, `permissions` |

Returns a
[Section](sections.html#Section)
object

## [Delete a section](#method.sections.destroy) [SectionsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sections_controller.rb)

### DELETE /api/v1/sections/:id

**Scope:** 
`url:DELETE|/api/v1/sections/:id`

Delete an existing section. Returns the former Section.

Returns a
[Section](sections.html#Section)
object