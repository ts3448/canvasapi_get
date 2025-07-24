# Courses

# Courses API



API for accessing course information.

### A Term object looks like:

```
{
  "id": 1,
  "name": "Default Term",
  "start_at": "2012-06-01T00:00:00-06:00",
  "end_at": null
}
```

### A CourseProgress object looks like:

```
{
  // total number of requirements from all modules
  "requirement_count": 10,
  // total number of requirements the user has completed from all modules
  "requirement_completed_count": 1,
  // url to next module item that has an unmet requirement. null if the user has
  // completed the course or the current module does not require sequential
  // progress
  "next_requirement_url": "http://localhost/courses/1/modules/items/2",
  // date the course was completed. null if the course has not been completed by
  // this user
  "completed_at": "2013-06-01T00:00:00-06:00"
}
```

### A Course object looks like:

```
{
  // the unique identifier for the course
  "id": 370663,
  // the SIS identifier for the course, if defined. This field is only included if
  // the user has permission to view SIS information.
  "sis_course_id": null,
  // the UUID of the course
  "uuid": "WvAHhY5FINzq5IyRIJybGeiXyFkG3SqHUPb7jZY5",
  // the integration identifier for the course, if defined. This field is only
  // included if the user has permission to view SIS information.
  "integration_id": null,
  // the unique identifier for the SIS import. This field is only included if the
  // user has permission to manage SIS information.
  "sis_import_id": 34,
  // the full name of the course. If the requesting user has set a nickname for
  // the course, the nickname will be shown here.
  "name": "InstructureCon 2012",
  // the course code
  "course_code": "INSTCON12",
  // the actual course name. This field is returned only if the requesting user
  // has set a nickname for the course.
  "original_name": "InstructureCon-2012-01",
  // the current state of the course, also known as âstatusâ.  The value will be
  // one of the following values: 'unpublished', 'available', 'completed', or
  // 'deleted'.  NOTE: When fetching a singular course that has a 'deleted'
  // workflow state value, an error will be returned with a message of 'The
  // specified resource does not exist.'
  "workflow_state": "available",
  // the account associated with the course
  "account_id": 81259,
  // the root account associated with the course
  "root_account_id": 81259,
  // the enrollment term associated with the course
  "enrollment_term_id": 34,
  // A list of grading periods associated with the course
  "grading_periods": null,
  // the grading standard associated with the course
  "grading_standard_id": 25,
  // the grade_passback_setting set on the course
  "grade_passback_setting": "nightly_sync",
  // the date the course was created.
  "created_at": "2012-05-01T00:00:00-06:00",
  // the start date for the course, if applicable
  "start_at": "2012-06-01T00:00:00-06:00",
  // the end date for the course, if applicable
  "end_at": "2012-09-01T00:00:00-06:00",
  // the course-set locale, if applicable
  "locale": "en",
  // A list of enrollments linking the current user to the course. for student
  // enrollments, grading information may be included if include[]=total_scores
  "enrollments": null,
  // optional: the total number of active and invited students in the course
  "total_students": 32,
  // course calendar
  "calendar": null,
  // the type of page that users will see when they first visit the course -
  // 'feed': Recent Activity Dashboard - 'wiki': Wiki Front Page - 'modules':
  // Course Modules/Sections Page - 'assignments': Course Assignments List -
  // 'syllabus': Course Syllabus Page other types may be added in the future
  "default_view": "feed",
  // optional: user-generated HTML for the course syllabus
  "syllabus_body": "<p>syllabus html goes here</p>",
  // optional: the number of submissions needing grading returned only if the
  // current user has grading rights and include[]=needs_grading_count
  "needs_grading_count": 17,
  // optional: the enrollment term object for the course returned only if
  // include[]=term
  "term": null,
  // optional: information on progress through the course returned only if
  // include[]=course_progress
  "course_progress": null,
  // weight final grade based on assignment group percentages
  "apply_assignment_group_weights": true,
  // optional: the permissions the user has for the course. returned only for a
  // single course and include[]=permissions
  "permissions": {"create_discussion_topic":true,"create_announcement":true},
  "is_public": true,
  "is_public_to_auth_users": true,
  "public_syllabus": true,
  "public_syllabus_to_auth": true,
  // optional: the public description of the course
  "public_description": "Come one, come all to InstructureCon 2012!",
  "storage_quota_mb": 5,
  "storage_quota_used_mb": 5,
  "hide_final_grades": false,
  "license": "Creative Commons",
  "allow_student_assignment_edits": false,
  "allow_wiki_comments": false,
  "allow_student_forum_attachments": false,
  "open_enrollment": true,
  "self_enrollment": false,
  "restrict_enrollments_to_course_dates": false,
  "course_format": "online",
  // optional: this will be true if this user is currently prevented from viewing
  // the course because of date restriction settings
  "access_restricted_by_date": false,
  // The course's IANA time zone name.
  "time_zone": "America/Denver",
  // optional: whether the course is set as a Blueprint Course (blueprint fields
  // require the Blueprint Courses feature)
  "blueprint": true,
  // optional: Set of restrictions applied to all locked course objects
  "blueprint_restrictions": {"content":true,"points":true,"due_dates":false,"availability_dates":false},
  // optional: Sets of restrictions differentiated by object type applied to
  // locked course objects
  "blueprint_restrictions_by_object_type": {"assignment":{"content":true,"points":true},"wiki_page":{"content":true}},
  // optional: whether the course is set as a template (requires the Course
  // Templates feature)
  "template": true
}
```

### A CalendarLink object looks like:

```
{
  // The URL of the calendar in ICS format
  "ics": "https://canvas.instructure.com/feeds/calendars/course_abcdef.ics"
}
```

## [List your courses](#method.courses.index) [CoursesController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses

**Scope:** 
`url:GET|/api/v1/courses`

Returns the paginated list of active courses for the current user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| enrollment\_type |  | string | When set, only return courses where the user is enrolled as this type. For example, set to âteacherâ to return only courses where the user is enrolled as a Teacher. This argument is ignored if enrollment\_role is given.  Allowed values: `teacher`, `student`, `ta`, `observer`, `designer` |
| enrollment\_role |  | string | Deprecated When set, only return courses where the user is enrolled with the specified course-level role. This can be a role created with the [Add Role API](roles.html#method.role_overrides.add_role "Add Role API") or a base role type of âStudentEnrollmentâ, âTeacherEnrollmentâ, âTaEnrollmentâ, âObserverEnrollmentâ, or âDesignerEnrollmentâ. |
| enrollment\_role\_id |  | integer | When set, only return courses where the user is enrolled with the specified course-level role. This can be a role created with the [Add Role API](roles.html#method.role_overrides.add_role "Add Role API") or a built\_in role type of âStudentEnrollmentâ, âTeacherEnrollmentâ, âTaEnrollmentâ, âObserverEnrollmentâ, or âDesignerEnrollmentâ. |
| enrollment\_state |  | string | When set, only return courses where the user has an enrollment with the given state. This will respect section/course/term date overrides.  Allowed values: `active`, `invited_or_pending`, `completed` |
| exclude\_blueprint\_courses |  | boolean | When set, only return courses that are not configured as blueprint courses. |
| include[] |  | string | * âneeds\_grading\_countâ: Optional information to include with each Course. When needs\_grading\_count is given, and the current user has grading rights, the total number of submissions needing grading for all assignments is returned. * âsyllabus\_bodyâ: Optional information to include with each Course. When syllabus\_body is given the user-generated html for the course syllabus is returned. * âpublic\_descriptionâ: Optional information to include with each Course. When public\_description is given the user-generated text for the course public description is returned. * âtotal\_scoresâ: Optional information to include with each Course. When total\_scores is given, any student enrollments will also include the fields âcomputed\_current\_scoreâ, âcomputed\_final\_scoreâ, âcomputed\_current\_gradeâ, and âcomputed\_final\_gradeâ, as well as (if the user has permission) âunposted\_current\_scoreâ, âunposted\_final\_scoreâ, âunposted\_current\_gradeâ, and âunposted\_final\_gradeâ (see Enrollment documentation for more information on these fields). This argument is ignored if the course is configured to hide final grades. * âcurrent\_grading\_period\_scoresâ: Optional information to include with each Course. When current\_grading\_period\_scores is given and total\_scores is given, any student enrollments will also include the fields âhas\_grading\_periodsâ, âtotals\_for\_all\_grading\_periods\_optionâ, âcurrent\_grading\_period\_titleâ, âcurrent\_grading\_period\_idâ, current\_period\_computed\_current\_scoreâ, âcurrent\_period\_computed\_final\_scoreâ, âcurrent\_period\_computed\_current\_gradeâ, and âcurrent\_period\_computed\_final\_gradeâ, as well as (if the user has permission) âcurrent\_period\_unposted\_current\_scoreâ, âcurrent\_period\_unposted\_final\_scoreâ, âcurrent\_period\_unposted\_current\_gradeâ, and âcurrent\_period\_unposted\_final\_gradeâ (see Enrollment documentation for more information on these fields). In addition, when this argument is passed, the course will have a âhas\_grading\_periodsâ attribute on it. This argument is ignored if the total\_scores argument is not included. If the course is configured to hide final grades, the following fields are not returned: âtotals\_for\_all\_grading\_periods\_optionâ, âcurrent\_period\_computed\_current\_scoreâ, âcurrent\_period\_computed\_final\_scoreâ, âcurrent\_period\_computed\_current\_gradeâ, âcurrent\_period\_computed\_final\_gradeâ, âcurrent\_period\_unposted\_current\_scoreâ, âcurrent\_period\_unposted\_final\_scoreâ, âcurrent\_period\_unposted\_current\_gradeâ, and âcurrent\_period\_unposted\_final\_gradeâ * âgrading\_periodsâ: Optional information to include with each Course. When grading\_periods is given, a list of the grading periods associated with each course is returned. * âtermâ: Optional information to include with each Course. When term is given, the information for the enrollment term for each course is returned. * âaccountâ: Optional information to include with each Course. When account is given, the account json for each course is returned. * âcourse\_progressâ: Optional information to include with each Course. When course\_progress is given, each course will include a âcourse\_progressâ object with the fields: ârequirement\_countâ, an integer specifying the total number of requirements in the course, ârequirement\_completed\_countâ, an integer specifying the total number of requirements in this course that have been completed, and ânext\_requirement\_urlâ, a string url to the next requirement item, and âcompleted\_atâ, the date the course was completed (null if incomplete). ânext\_requirement\_urlâ will be null if all requirements have been completed or the current module does not require sequential progress. âcourse\_progressâ will return an error message if the course is not module based or the user is not enrolled as a student in the course. * âsectionsâ: Section enrollment information to include with each Course. Returns an array of hashes containing the section ID (id), section name (name), start and end dates (start\_at, end\_at), as well as the enrollment type (enrollment\_role, e.g. âStudentEnrollmentâ). * âstorage\_quota\_used\_mbâ: The amount of storage space used by the files in this course * âtotal\_studentsâ: Optional information to include with each Course. Returns an integer for the total amount of active and invited students. * âpassback\_statusâ: Include the grade passback\_status * âfavoritesâ: Optional information to include with each Course. Indicates if the user has marked the course as a favorite course. * âteachersâ: Teacher information to include with each Course. Returns an array of hashes containing the [UserDisplay](users.html#UserDisplay "UserDisplay") information for each teacher in the course. * âobserved\_usersâ: Optional information to include with each Course. Will include data for observed users if the current user has an observer enrollment. * âtabsâ: Optional information to include with each Course. Will include the list of tabs configured for each course. See the [List available tabs API](tabs.html#method.tabs.index "List available tabs API") for more information. * âcourse\_imageâ: Optional information to include with each Course. Returns course image url if a course image has been set. * âbanner\_imageâ: Optional information to include with each Course. Returns course banner image url if the course is a Canvas for Elementary subject and a banner image has been set. * âconcludedâ: Optional information to include with each Course. Indicates whether the course has been concluded, taking course and term dates into account. * âpost\_manuallyâ: Optional information to include with each Course. Returns true if the course post policy is set to Manually post grades. Returns false if the the course post policy is set to Automatically post grades.   Allowed values: `needs_grading_count`, `syllabus_body`, `public_description`, `total_scores`, `current_grading_period_scores`, `grading_periods`, `term`, `account`, `course_progress`, `sections`, `storage_quota_used_mb`, `total_students`, `passback_status`, `favorites`, `teachers`, `observed_users`, `course_image`, `banner_image`, `concluded`, `post_manually` |
| state[] |  | string | If set, only return courses that are in the given state(s). By default, âavailableâ is returned for students and observers, and anything except âdeletedâ, for all other enrollment types  Allowed values: `unpublished`, `available`, `completed`, `deleted` |

Returns a list of
[Course](courses.html#Course)
objects

## [List courses for a user](#method.courses.user_index) [CoursesController#user\_index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/users/:user\_id/courses

**Scope:** 
`url:GET|/api/v1/users/:user_id/courses`

Returns a paginated list of active courses for this user. To view the course list for a user other than yourself, you must be either an observer of that user or an administrator.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âneeds\_grading\_countâ: Optional information to include with each Course. When needs\_grading\_count is given, and the current user has grading rights, the total number of submissions needing grading for all assignments is returned. * âsyllabus\_bodyâ: Optional information to include with each Course. When syllabus\_body is given the user-generated html for the course syllabus is returned. * âpublic\_descriptionâ: Optional information to include with each Course. When public\_description is given the user-generated text for the course public description is returned. * âtotal\_scoresâ: Optional information to include with each Course. When total\_scores is given, any student enrollments will also include the fields âcomputed\_current\_scoreâ, âcomputed\_final\_scoreâ, âcomputed\_current\_gradeâ, and âcomputed\_final\_gradeâ (see Enrollment documentation for more information on these fields). This argument is ignored if the course is configured to hide final grades. * âcurrent\_grading\_period\_scoresâ: Optional information to include with each Course. When current\_grading\_period\_scores is given and total\_scores is given, any student enrollments will also include the fields âhas\_grading\_periodsâ, âtotals\_for\_all\_grading\_periods\_optionâ, âcurrent\_grading\_period\_titleâ, âcurrent\_grading\_period\_idâ, current\_period\_computed\_current\_scoreâ, âcurrent\_period\_computed\_final\_scoreâ, âcurrent\_period\_computed\_current\_gradeâ, and âcurrent\_period\_computed\_final\_gradeâ, as well as (if the user has permission) âcurrent\_period\_unposted\_current\_scoreâ, âcurrent\_period\_unposted\_final\_scoreâ, âcurrent\_period\_unposted\_current\_gradeâ, and âcurrent\_period\_unposted\_final\_gradeâ (see Enrollment documentation for more information on these fields). In addition, when this argument is passed, the course will have a âhas\_grading\_periodsâ attribute on it. This argument is ignored if the course is configured to hide final grades or if the total\_scores argument is not included. * âgrading\_periodsâ: Optional information to include with each Course. When grading\_periods is given, a list of the grading periods associated with each course is returned. * âtermâ: Optional information to include with each Course. When term is given, the information for the enrollment term for each course is returned. * âaccountâ: Optional information to include with each Course. When account is given, the account json for each course is returned. * âcourse\_progressâ: Optional information to include with each Course. When course\_progress is given, each course will include a âcourse\_progressâ object with the fields: ârequirement\_countâ, an integer specifying the total number of requirements in the course, ârequirement\_completed\_countâ, an integer specifying the total number of requirements in this course that have been completed, and ânext\_requirement\_urlâ, a string url to the next requirement item, and âcompleted\_atâ, the date the course was completed (null if incomplete). ânext\_requirement\_urlâ will be null if all requirements have been completed or the current module does not require sequential progress. âcourse\_progressâ will return an error message if the course is not module based or the user is not enrolled as a student in the course. * âsectionsâ: Section enrollment information to include with each Course. Returns an array of hashes containing the section ID (id), section name (name), start and end dates (start\_at, end\_at), as well as the enrollment type (enrollment\_role, e.g. âStudentEnrollmentâ). * âstorage\_quota\_used\_mbâ: The amount of storage space used by the files in this course * âtotal\_studentsâ: Optional information to include with each Course. Returns an integer for the total amount of active and invited students. * âpassback\_statusâ: Include the grade passback\_status * âfavoritesâ: Optional information to include with each Course. Indicates if the user has marked the course as a favorite course. * âteachersâ: Teacher information to include with each Course. Returns an array of hashes containing the [UserDisplay](users.html#UserDisplay "UserDisplay") information for each teacher in the course. * âobserved\_usersâ: Optional information to include with each Course. Will include data for observed users if the current user has an observer enrollment. * âtabsâ: Optional information to include with each Course. Will include the list of tabs configured for each course. See the [List available tabs API](tabs.html#method.tabs.index "List available tabs API") for more information. * âcourse\_imageâ: Optional information to include with each Course. Returns course image url if a course image has been set. * âbanner\_imageâ: Optional information to include with each Course. Returns course banner image url if the course is a Canvas for Elementary subject and a banner image has been set. * âconcludedâ: Optional information to include with each Course. Indicates whether the course has been concluded, taking course and term dates into account. * âpost\_manuallyâ: Optional information to include with each Course. Returns true if the course post policy is set to âManuallyâ. Returns false if the the course post policy is set to âAutomaticallyâ.   Allowed values: `needs_grading_count`, `syllabus_body`, `public_description`, `total_scores`, `current_grading_period_scores`, `grading_periods`, `term`, `account`, `course_progress`, `sections`, `storage_quota_used_mb`, `total_students`, `passback_status`, `favorites`, `teachers`, `observed_users`, `course_image`, `banner_image`, `concluded`, `post_manually` |
| state[] |  | string | If set, only return courses that are in the given state(s). By default, âavailableâ is returned for students and observers, and anything except âdeletedâ, for all other enrollment types  Allowed values: `unpublished`, `available`, `completed`, `deleted` |
| enrollment\_state |  | string | When set, only return courses where the user has an enrollment with the given state. This will respect section/course/term date overrides.  Allowed values: `active`, `invited_or_pending`, `completed` |
| homeroom |  | boolean | If set, only return homeroom courses. |
| account\_id |  | string | If set, only include courses associated with this account |

Returns a list of
[Course](courses.html#Course)
objects

## [Get user progress](#method.courses.user_progress) [CoursesController#user\_progress](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/users/:user\_id/progress

**Scope:** 
`url:GET|/api/v1/courses/:course_id/users/:user_id/progress`

Return progress information for the user and course

You can supply `self` as the user\_id to query your own progress in a course. To query another userâs progress, you must be a teacher in the course, an administrator, or a linked observer of the user.

Returns a
[CourseProgress](courses.html#CourseProgress)
object

## [Create a new course](#method.courses.create) [CoursesController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### POST /api/v1/accounts/:account\_id/courses

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/courses`

Create a new course

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course[name] |  | string | The name of the course. If omitted, the course will be named âUnnamed Course.â |
| course[course\_code] |  | string | The course code for the course. |
| course[start\_at] |  | DateTime | Course start date in ISO8601 format, e.g. 2011-01-01T01:00Z This value is ignored unless ârestrict\_enrollments\_to\_course\_datesâ is set to true. |
| course[end\_at] |  | DateTime | Course end date in ISO8601 format. e.g. 2011-01-01T01:00Z This value is ignored unless ârestrict\_enrollments\_to\_course\_datesâ is set to true. |
| course[license] |  | string | The name of the licensing. Should be one of the following abbreviations (a descriptive name is included in parenthesis for reference):   * âprivateâ (Private Copyrighted) * âcc\_by\_nc\_ndâ (CC Attribution Non-Commercial No Derivatives) * âcc\_by\_nc\_saâ (CC Attribution Non-Commercial Share Alike) * âcc\_by\_ncâ (CC Attribution Non-Commercial) * âcc\_by\_ndâ (CC Attribution No Derivatives) * âcc\_by\_saâ (CC Attribution Share Alike) * âcc\_byâ (CC Attribution) * âpublic\_domainâ (Public Domain). |
| course[is\_public] |  | boolean | Set to true if course is public to both authenticated and unauthenticated users. |
| course[is\_public\_to\_auth\_users] |  | boolean | Set to true if course is public only to authenticated users. |
| course[public\_syllabus] |  | boolean | Set to true to make the course syllabus public. |
| course[public\_syllabus\_to\_auth] |  | boolean | Set to true to make the course syllabus public for authenticated users. |
| course[public\_description] |  | string | A publicly visible description of the course. |
| course[allow\_student\_wiki\_edits] |  | boolean | If true, students will be able to modify the course wiki. |
| course[allow\_wiki\_comments] |  | boolean | If true, course members will be able to comment on wiki pages. |
| course[allow\_student\_forum\_attachments] |  | boolean | If true, students can attach files to forum posts. |
| course[open\_enrollment] |  | boolean | Set to true if the course is open enrollment. |
| course[self\_enrollment] |  | boolean | Set to true if the course is self enrollment. |
| course[restrict\_enrollments\_to\_course\_dates] |  | boolean | Set to true to restrict user enrollments to the start and end dates of the course. This value must be set to true in order to specify a course start date and/or end date. |
| course[term\_id] |  | string | The unique ID of the term to create to course in. |
| course[sis\_course\_id] |  | string | The unique SIS identifier. |
| course[integration\_id] |  | string | The unique Integration identifier. |
| course[hide\_final\_grades] |  | boolean | If this option is set to true, the totals in student grades summary will be hidden. |
| course[apply\_assignment\_group\_weights] |  | boolean | Set to true to weight final grade based on assignment groups percentages. |
| course[time\_zone] |  | string | The time zone for the course. Allowed time zones are [IANA time zones](http://www.iana.org/time-zones "IANA time zones") or friendlier [Ruby on Rails time zones](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html "Ruby on Rails time zones"). |
| offer |  | boolean | If this option is set to true, the course will be available to students immediately. |
| enroll\_me |  | boolean | Set to true to enroll the current user as the teacher. |
| course[default\_view] |  | string | The type of page that users will see when they first visit the course   * âfeedâ Recent Activity Dashboard * âmodulesâ Course Modules/Sections Page * âassignmentsâ Course Assignments List * âsyllabusâ Course Syllabus Page   other types may be added in the future  Allowed values: `feed`, `wiki`, `modules`, `syllabus`, `assignments` |
| course[syllabus\_body] |  | string | The syllabus body for the course |
| course[grading\_standard\_id] |  | integer | The grading standard id to set for the course. If no value is provided for this argument the current grading\_standard will be un-set from this course. |
| course[grade\_passback\_setting] |  | string | Optional. The grade\_passback\_setting for the course. Only ânightly\_syncâ, âdisabledâ, and â are allowed |
| course[course\_format] |  | string | Optional. Specifies the format of the course. (Should be âon\_campusâ, âonlineâ, or âblendedâ) |
| course[post\_manually] |  | boolean | Default is false. When true, all grades in the course must be posted manually, and will not be automatically posted. When false, all grades in the course will be automatically posted. |
| enable\_sis\_reactivation |  | boolean | When true, will first try to re-activate a deleted course with matching sis\_course\_id if possible. |

Returns a
[Course](courses.html#Course)
object

## [Upload a file](#method.courses.create_file) [CoursesController#create\_file](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### POST /api/v1/courses/:course\_id/files

**Scope:** 
`url:POST|/api/v1/courses/:course_id/files`

Upload a file to the course.

This API endpoint is the first step in uploading a file to a course. See the [File Upload Documentation](file_uploads.html "File Upload Documentation") for details on the file upload workflow.

Only those with the âManage Filesâ permission on a course can upload files to the course. By default, this is Teachers, TAs and Designers.

## [List students](#method.courses.students) [CoursesController#students](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/students

**Scope:** 
`url:GET|/api/v1/courses/:course_id/students`

Returns the paginated list of students enrolled in this course.

DEPRECATED: Please use the [course users](courses.html#method.courses.users "course users") endpoint and pass âstudentâ as the enrollment\_type.

Returns a list of
[User](users.html#User)
objects

## [List users in course](#method.courses.users) [CoursesController#users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/users

**Scope:** 
`url:GET|/api/v1/courses/:course_id/users`

### GET /api/v1/courses/:course\_id/search\_users

**Scope:** 
`url:GET|/api/v1/courses/:course_id/search_users`

Returns the paginated list of users in this course. And optionally the userâs enrollments in the course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| search\_term |  | string | The partial name or full ID of the users to match and return in the results list. |
| sort |  | string | When set, sort the results of the search based on the given field.  Allowed values: `username`, `last_login`, `email`, `sis_id` |
| enrollment\_type[] |  | string | When set, only return users where the user is enrolled as this type. âstudent\_viewâ implies include[]=test\_student. This argument is ignored if enrollment\_role is given.  Allowed values: `teacher`, `student`, `student_view`, `ta`, `observer`, `designer` |
| enrollment\_role |  | string | Deprecated When set, only return users enrolled with the specified course-level role. This can be a role created with the [Add Role API](roles.html#method.role_overrides.add_role "Add Role API") or a base role type of âStudentEnrollmentâ, âTeacherEnrollmentâ, âTaEnrollmentâ, âObserverEnrollmentâ, or âDesignerEnrollmentâ. |
| enrollment\_role\_id |  | integer | When set, only return courses where the user is enrolled with the specified course-level role. This can be a role created with the [Add Role API](roles.html#method.role_overrides.add_role "Add Role API") or a built\_in role id with type âStudentEnrollmentâ, âTeacherEnrollmentâ, âTaEnrollmentâ, âObserverEnrollmentâ, or âDesignerEnrollmentâ. |
| include[] |  | string | * âenrollmentsâ:   Optionally include with each Course the userâs current and invited enrollments. If the user is enrolled as a student, and the account has permission to manage or view all grades, each enrollment will include a âgradesâ key with âcurrent\_scoreâ, âfinal\_scoreâ, âcurrent\_gradeâ and âfinal\_gradeâ values.   * âlockedâ: Optionally include whether an enrollment is locked. * âavatar\_urlâ: Optionally include avatar\_url. * âbioâ: Optionally include each userâs bio. * âtest\_studentâ: Optionally include the courseâs Test Student,   if present. Default is to not include Test Student.   * âcustom\_linksâ: Optionally include plugin-supplied custom links for each student,   such as analytics information   * âcurrent\_grading\_period\_scoresâ: if enrollments is included as   well as this directive, the scores returned in the enrollment will be for the current grading period if there is one. A âgrading\_period\_idâ value will also be included with the scores. if grading\_period\_id is nil there is no current grading period and the score is a total score.   * âuuidâ: Optionally include the users uuid   Allowed values: `enrollments`, `locked`, `avatar_url`, `test_student`, `bio`, `custom_links`, `current_grading_period_scores`, `uuid` |
| user\_id |  | string | If this parameter is given and it corresponds to a user in the course, the `page` parameter will be ignored and the page containing the specified user will be returned instead. |
| user\_ids[] |  | integer | If included, the course users set will only include users with IDs specified by the param. Note: this will not work in conjunction with the âuser\_idâ argument but multiple user\_ids can be included. |
| enrollment\_state[] |  | string | When set, only return users where the enrollment workflow state is of one of the given types. âactiveâ and âinvitedâ enrollments are returned by default.  Allowed values: `active`, `invited`, `rejected`, `completed`, `inactive` |

Returns a list of
[User](users.html#User)
objects

## [List recently logged in students](#method.courses.recent_students) [CoursesController#recent\_students](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/recent\_students

**Scope:** 
`url:GET|/api/v1/courses/:course_id/recent_students`

Returns the paginated list of users in this course, ordered by how recently they have logged in. The records include the âlast\_loginâ field which contains a timestamp of the last time that user logged into canvas. The querying user must have the âView usage reportsâ permission.

#### Example Request:

#### 

```
curl -H 'Authorization: Bearer <token>' \
     https://<canvas>/api/v1/courses/<course_id>/recent_users
```

Returns a list of
[User](users.html#User)
objects

## [Get single user](#method.courses.user) [CoursesController#user](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/users/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/users/:id`

Return information on a single user.

Accepts the same include[] parameters as the :users: action, and returns a single user with the same fields as that action.

Returns an
[User](users.html#User)
object

## [Search for content share users](#method.courses.content_share_users) [CoursesController#content\_share\_users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/content\_share\_users

**Scope:** 
`url:GET|/api/v1/courses/:course_id/content_share_users`

Returns a paginated list of users you can share content with. Requires the content share feature and the user must have the manage content permission for the course.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| search\_term | Required | string | Term used to find users. Will search available share users with the search term in their name. |

#### Example Request:

#### 

```
curl -H 'Authorization: Bearer <token>' \
     https://<canvas>/api/v1/courses/<course_id>/content_share_users \
     -d 'search_term=smith'
```

Returns a list of
[User](users.html#User)
objects

## [Preview processed html](#method.courses.preview_html) [CoursesController#preview\_html](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### POST /api/v1/courses/:course\_id/preview\_html

**Scope:** 
`url:POST|/api/v1/courses/:course_id/preview_html`

Preview html content processed for this course

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| html |  | string | The html content to process |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/preview_html \
     -F 'html=<p><badhtml></badhtml>processed html</p>' \
     -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{
  "html": "<p>processed html</p>"
}
```

## [Course activity stream](#method.courses.activity_stream) [CoursesController#activity\_stream](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/activity\_stream

**Scope:** 
`url:GET|/api/v1/courses/:course_id/activity_stream`

Returns the current userâs course-specific activity stream, paginated.

For full documentation, see the API documentation for the user activity stream, in the user api.

## [Course activity stream summary](#method.courses.activity_stream_summary) [CoursesController#activity\_stream\_summary](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/activity\_stream/summary

**Scope:** 
`url:GET|/api/v1/courses/:course_id/activity_stream/summary`

Returns a summary of the current userâs course-specific activity stream.

For full documentation, see the API documentation for the user activity stream summary, in the user api.

## [Course TODO items](#method.courses.todo_items) [CoursesController#todo\_items](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/todo

**Scope:** 
`url:GET|/api/v1/courses/:course_id/todo`

Returns the current userâs course-specific todo items.

For full documentation, see the API documentation for the user todo items, in the user api.

## [Delete/Conclude a course](#method.courses.destroy) [CoursesController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### DELETE /api/v1/courses/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:id`

Delete or conclude an existing course

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| event | Required | string | The action to take on the course.  Allowed values: `delete`, `conclude` |

#### Example Response:

#### 

```
{ "delete": "true" }
```

## [Get course settings](#method.courses.api_settings) [CoursesController#api\_settings](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/settings

**Scope:** 
`url:GET|/api/v1/courses/:course_id/settings`

Returns some of a courseâs settings.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/settings \
  -X GET \
  -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{
  "allow_student_discussion_topics": true,
  "allow_student_forum_attachments": false,
  "allow_student_discussion_editing": true,
  "grading_standard_enabled": true,
  "grading_standard_id": 137,
  "allow_student_organized_groups": true,
  "hide_final_grades": false,
  "hide_distribution_graphs": false,
  "hide_sections_on_course_users_page": false,
  "lock_all_announcements": true,
  "usage_rights_required": false,
  "homeroom_course": false,
  "default_due_time": "23:59:59",
  "conditional_release": false
}
```

## [Update course settings](#method.courses.update_settings) [CoursesController#update\_settings](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### PUT /api/v1/courses/:course\_id/settings

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/settings`

Can update the following course settings:

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| allow\_final\_grade\_override |  | boolean | Let student final grades for a grading period or the total grades for the course be overridden |
| allow\_student\_discussion\_topics |  | boolean | Let students create discussion topics |
| allow\_student\_forum\_attachments |  | boolean | Let students attach files to discussions |
| allow\_student\_discussion\_editing |  | boolean | Let students edit or delete their own discussion replies |
| allow\_student\_organized\_groups |  | boolean | Let students organize their own groups |
| allow\_student\_discussion\_reporting |  | boolean | Let students report offensive discussion content |
| allow\_student\_anonymous\_discussion\_topics |  | boolean | Let students create anonymous discussion topics |
| filter\_speed\_grader\_by\_student\_group |  | boolean | Filter SpeedGrader to only the selected student group |
| hide\_final\_grades |  | boolean | Hide totals in student grades summary |
| hide\_distribution\_graphs |  | boolean | Hide grade distribution graphs from students |
| hide\_sections\_on\_course\_users\_page |  | boolean | Disallow students from viewing students in sections they do not belong to |
| lock\_all\_announcements |  | boolean | Disable comments on announcements |
| usage\_rights\_required |  | boolean | Copyright and license information must be provided for files before they are published. |
| restrict\_student\_past\_view |  | boolean | Restrict students from viewing courses after end date |
| restrict\_student\_future\_view |  | boolean | Restrict students from viewing courses before start date |
| show\_announcements\_on\_home\_page |  | boolean | Show the most recent announcements on the Course home page (if a Wiki, defaults to five announcements, configurable via home\_page\_announcement\_limit). Canvas for Elementary subjects ignore this setting. |
| home\_page\_announcement\_limit |  | integer | Limit the number of announcements on the home page if enabled via show\_announcements\_on\_home\_page |
| syllabus\_course\_summary |  | boolean | Show the course summary (list of assignments and calendar events) on the syllabus page. Default is true. |
| default\_due\_time |  | string | Set the default due time for assignments. This is the time that will be pre-selected in the Canvas user interface when setting a due date for an assignment. It does not change when any existing assignment is due. It should be given in 24-hour HH:MM:SS format. The default is â23:59:59â. Use âinheritâ to inherit the account setting. |
| conditional\_release |  | boolean | Enable or disable individual learning paths for students based on assessment |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/settings \
  -X PUT \
  -H 'Authorization: Bearer <token>' \
  -d 'allow_student_discussion_topics=false'
```

## [Return test student for course](#method.courses.student_view_student) [CoursesController#student\_view\_student](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/student\_view\_student

**Scope:** 
`url:GET|/api/v1/courses/:course_id/student_view_student`

Returns information for a test student in this course. Creates a test student if one does not already exist for the course. The caller must have permission to access the courseâs student view.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/student_view_student \
  -X GET \
  -H 'Authorization: Bearer <token>'
```

Returns an
[User](users.html#User)
object

## [Get a single course](#method.courses.show) [CoursesController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:id

**Scope:** 
`url:GET|/api/v1/courses/:id`

### GET /api/v1/accounts/:account\_id/courses/:id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/courses/:id`

Return information on a single course.

Accepts the same include[] parameters as the list action plus:

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âall\_coursesâ: Also search recently deleted courses. * âpermissionsâ: Include permissions the current user has for the course. * âobserved\_usersâ: Include observed users in the enrollments * âcourse\_imageâ: Include course image url if a course image has been set * âbanner\_imageâ: Include course banner image url if the course is a Canvas for Elementary subject and a banner image has been set * âconcludedâ: Optional information to include with Course. Indicates whether the course has been concluded, taking course and term dates into account. * âlti\_context\_idâ: Include course LTI tool id. * âpost\_manuallyâ: Include course post policy. If the post policy is manually post grades, the value will be true. If the post policy is automatically post grades, the value will be false.   Allowed values: `needs_grading_count`, `syllabus_body`, `public_description`, `total_scores`, `current_grading_period_scores`, `term`, `account`, `course_progress`, `sections`, `storage_quota_used_mb`, `total_students`, `passback_status`, `favorites`, `teachers`, `observed_users`, `all_courses`, `permissions`, `course_image`, `banner_image`, `concluded`, `lti_context_id`, `post_manually` |
| teacher\_limit |  | integer | The maximum number of teacher enrollments to show. If the course contains more teachers than this, instead of giving the teacher enrollments, the count of teachers will be given under a *teacher\_count* key. |

Returns a
[Course](courses.html#Course)
object

## [Update a course](#method.courses.update) [CoursesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### PUT /api/v1/courses/:id

**Scope:** 
`url:PUT|/api/v1/courses/:id`

Update an existing course.

Arguments are the same as Courses#create, with a few exceptions (enroll\_me).

If a user has content management rights, but not full course editing rights, the only attribute editable through this endpoint will be âsyllabus\_bodyâ

If an account has set prevent\_course\_availability\_editing\_by\_teachers, a teacher cannot change [course](start_at), [course](conclude_at), or [course](restrict_enrollments_to_course_dates) here.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course[account\_id] |  | integer | The unique ID of the account to move the course to. |
| course[name] |  | string | The name of the course. If omitted, the course will be named âUnnamed Course.â |
| course[course\_code] |  | string | The course code for the course. |
| course[start\_at] |  | DateTime | Course start date in ISO8601 format, e.g. 2011-01-01T01:00Z This value is ignored unless ârestrict\_enrollments\_to\_course\_datesâ is set to true, or the course is already published. |
| course[end\_at] |  | DateTime | Course end date in ISO8601 format. e.g. 2011-01-01T01:00Z This value is ignored unless ârestrict\_enrollments\_to\_course\_datesâ is set to true. |
| course[license] |  | string | The name of the licensing. Should be one of the following abbreviations (a descriptive name is included in parenthesis for reference):   * âprivateâ (Private Copyrighted) * âcc\_by\_nc\_ndâ (CC Attribution Non-Commercial No Derivatives) * âcc\_by\_nc\_saâ (CC Attribution Non-Commercial Share Alike) * âcc\_by\_ncâ (CC Attribution Non-Commercial) * âcc\_by\_ndâ (CC Attribution No Derivatives) * âcc\_by\_saâ (CC Attribution Share Alike) * âcc\_byâ (CC Attribution) * âpublic\_domainâ (Public Domain). |
| course[is\_public] |  | boolean | Set to true if course is public to both authenticated and unauthenticated users. |
| course[is\_public\_to\_auth\_users] |  | boolean | Set to true if course is public only to authenticated users. |
| course[public\_syllabus] |  | boolean | Set to true to make the course syllabus public. |
| course[public\_syllabus\_to\_auth] |  | boolean | Set to true to make the course syllabus to public for authenticated users. |
| course[public\_description] |  | string | A publicly visible description of the course. |
| course[allow\_student\_wiki\_edits] |  | boolean | If true, students will be able to modify the course wiki. |
| course[allow\_wiki\_comments] |  | boolean | If true, course members will be able to comment on wiki pages. |
| course[allow\_student\_forum\_attachments] |  | boolean | If true, students can attach files to forum posts. |
| course[open\_enrollment] |  | boolean | Set to true if the course is open enrollment. |
| course[self\_enrollment] |  | boolean | Set to true if the course is self enrollment. |
| course[restrict\_enrollments\_to\_course\_dates] |  | boolean | Set to true to restrict user enrollments to the start and end dates of the course. Setting this value to false will remove the course end date (if it exists), as well as the course start date (if the course is unpublished). |
| course[term\_id] |  | integer | The unique ID of the term to create to course in. |
| course[sis\_course\_id] |  | string | The unique SIS identifier. |
| course[integration\_id] |  | string | The unique Integration identifier. |
| course[hide\_final\_grades] |  | boolean | If this option is set to true, the totals in student grades summary will be hidden. |
| course[time\_zone] |  | string | The time zone for the course. Allowed time zones are [IANA time zones](http://www.iana.org/time-zones "IANA time zones") or friendlier [Ruby on Rails time zones](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html "Ruby on Rails time zones"). |
| course[apply\_assignment\_group\_weights] |  | boolean | Set to true to weight final grade based on assignment groups percentages. |
| course[storage\_quota\_mb] |  | integer | Set the storage quota for the course, in megabytes. The caller must have the âManage storage quotasâ account permission. |
| offer |  | boolean | If this option is set to true, the course will be available to students immediately. |
| course[event] |  | string | The action to take on each course.   * âclaimâ makes a course no longer visible to students. This action is also called âunpublishâ on the web site. A course cannot be unpublished if students have received graded submissions. * âofferâ makes a course visible to students. This action is also called âpublishâ on the web site. * âconcludeâ prevents future enrollments and makes a course read-only for all participants. The course still appears in prior-enrollment lists. * âdeleteâ completely removes the course from the web site (including course menus and prior-enrollment lists). All enrollments are deleted. Course content may be physically deleted at a future date. * âundeleteâ attempts to recover a course that has been deleted. This action requires account administrative rights. (Recovery is not guaranteed; please conclude rather than delete a course if there is any possibility the course will be used again.) The recovered course will be unpublished. Deleted enrollments will not be recovered.   Allowed values: `claim`, `offer`, `conclude`, `delete`, `undelete` |
| course[default\_view] |  | string | The type of page that users will see when they first visit the course   * âfeedâ Recent Activity Dashboard * âwikiâ Wiki Front Page * âmodulesâ Course Modules/Sections Page * âassignmentsâ Course Assignments List * âsyllabusâ Course Syllabus Page   other types may be added in the future  Allowed values: `feed`, `wiki`, `modules`, `syllabus`, `assignments` |
| course[syllabus\_body] |  | string | The syllabus body for the course |
| course[syllabus\_course\_summary] |  | boolean | Optional. Indicates whether the Course Summary (consisting of the courseâs assignments and calendar events) is displayed on the syllabus page. Defaults to `true`. |
| course[grading\_standard\_id] |  | integer | The grading standard id to set for the course. If no value is provided for this argument the current grading\_standard will be un-set from this course. |
| course[grade\_passback\_setting] |  | string | Optional. The grade\_passback\_setting for the course. Only ânightly\_syncâ and â are allowed |
| course[course\_format] |  | string | Optional. Specifies the format of the course. (Should be either âon\_campusâ or âonlineâ) |
| course[image\_id] |  | integer | This is a file ID corresponding to an image file in the course that will be used as the course image. This will clear the courseâs image\_url setting if set. If you attempt to provide image\_url and image\_id in a request it will fail. |
| course[image\_url] |  | string | This is a URL to an image to be used as the course image. This will clear the courseâs image\_id setting if set. If you attempt to provide image\_url and image\_id in a request it will fail. |
| course[remove\_image] |  | boolean | If this option is set to true, the course image url and course image ID are both set to nil |
| course[remove\_banner\_image] |  | boolean | If this option is set to true, the course banner image url and course banner image ID are both set to nil |
| course[blueprint] |  | boolean | Sets the course as a blueprint course. |
| course[blueprint\_restrictions] |  | BlueprintRestriction | Sets a default set to apply to blueprint course objects when restricted, unless *use\_blueprint\_restrictions\_by\_object\_type* is enabled. See the [Blueprint Restriction](blueprint_courses.html#BlueprintRestriction "Blueprint Restriction") documentation |
| course[use\_blueprint\_restrictions\_by\_object\_type] |  | boolean | When enabled, the *blueprint\_restrictions* parameter will be ignored in favor of the *blueprint\_restrictions\_by\_object\_type* parameter |
| course[blueprint\_restrictions\_by\_object\_type] |  | multiple BlueprintRestrictions | Allows setting multiple [Blueprint Restriction](blueprint_courses.html#BlueprintRestriction "Blueprint Restriction") to apply to blueprint course objects of the matching type when restricted. The possible object types are âassignmentâ, âattachmentâ, âdiscussion\_topicâ, âquizâ and âwiki\_pageâ. Example usage:   ``` course[blueprint_restrictions_by_object_type][assignment][content]=1  ``` |
| course[homeroom\_course] |  | boolean | Sets the course as a homeroom course. The setting takes effect only when the course is associated with a Canvas for Elementary-enabled account. |
| course[sync\_enrollments\_from\_homeroom] |  | string | Syncs enrollments from the homeroom that is set in homeroom\_course\_id. The setting only takes effect when the course is associated with a Canvas for Elementary-enabled account and sync\_enrollments\_from\_homeroom is enabled. |
| course[homeroom\_course\_id] |  | string | Sets the Homeroom Course id to be used with sync\_enrollments\_from\_homeroom. The setting only takes effect when the course is associated with a Canvas for Elementary-enabled account and sync\_enrollments\_from\_homeroom is enabled. |
| course[template] |  | boolean | Enable or disable the course as a template that can be selected by an account |
| course[course\_color] |  | string | Sets a color in hex code format to be associated with the course. The setting takes effect only when the course is associated with a Canvas for Elementary-enabled account. |
| course[friendly\_name] |  | string | Set a friendly name for the course. If this is provided and the course is associated with a Canvas for Elementary account, it will be shown instead of the course name. This setting takes priority over course nicknames defined by individual users. |
| course[enable\_course\_paces] |  | boolean | Enable or disable Course Pacing for the course. This setting only has an effect when the Course Pacing feature flag is enabled for the sub-account. Otherwise, Course Pacing are always disabled. |
| course[conditional\_release] |  | boolean | Enable or disable individual learning paths for students based on assessment |
| course[post\_manually] |  | boolean | When true, all grades in the course will be posted manually. When false, all grades in the course will be automatically posted. Use with caution as this setting will override any assignment level post policy. |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id> \
  -X PUT \
  -H 'Authorization: Bearer <token>' \
  -d 'course[name]=New course name' \
  -d 'course[start_at]=2012-05-05T00:00:00Z'
```

#### Example Response:

#### 

```
{
  "name": "New course name",
  "course_code": "COURSE-001",
  "start_at": "2012-05-05T00:00:00Z",
  "end_at": "2012-08-05T23:59:59Z",
  "sis_course_id": "12345"
}
```

## [Update courses](#method.courses.batch_update) [CoursesController#batch\_update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### PUT /api/v1/accounts/:account\_id/courses

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/courses`

Update multiple courses in an account. Operates asynchronously; use the [progress endpoint](progress.html#method.progress.show "progress endpoint") to query the status of an operation.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_ids[] | Required | string | List of ids of courses to update. At most 500 courses may be updated in one call. |
| event | Required | string | The action to take on each course. Must be one of âofferâ, âconcludeâ, âdeleteâ, or âundeleteâ.   * âofferâ makes a course visible to students. This action is also called âpublishâ on the web site. * âconcludeâ prevents future enrollments and makes a course read-only for all participants. The course still appears in prior-enrollment lists. * âdeleteâ completely removes the course from the web site (including course menus and prior-enrollment lists). All enrollments are deleted. Course content may be physically deleted at a future date. * âundeleteâ attempts to recover a course that has been deleted. (Recovery is not guaranteed; please conclude rather than delete a course if there is any possibility the course will be used again.) The recovered course will be unpublished. Deleted enrollments will not be recovered.   Allowed values: `offer`, `conclude`, `delete`, `undelete` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/<account_id>/courses \
  -X PUT \
  -H 'Authorization: Bearer <token>' \
  -d 'event=offer' \
  -d 'course_ids[]=1' \
  -d 'course_ids[]=2'
```

Returns a
[Progress](progress.html#Progress)
object

## [Reset a course](#method.courses.reset_content) [CoursesController#reset\_content](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### POST /api/v1/courses/:course\_id/reset\_content

**Scope:** 
`url:POST|/api/v1/courses/:course_id/reset_content`

Deletes the current course, and creates a new equivalent course with no content, but all sections and users moved over.

Returns a
[Course](courses.html#Course)
object

## [Get effective due dates](#method.courses.effective_due_dates) [CoursesController#effective\_due\_dates](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/effective\_due\_dates

**Scope:** 
`url:GET|/api/v1/courses/:course_id/effective_due_dates`

For each assignment in the course, returns each assigned studentâs ID and their corresponding due date along with some grading period data. Returns a collection with keys representing assignment IDs and values as a collection containing keys representing student IDs and values representing the studentâs effective due\_at, the grading\_period\_id of which the due\_at falls in, and whether or not the grading period is closed (in\_closed\_grading\_period)

The list of assignment IDs for which effective student due dates are requested. If not provided, all assignments in the course will be used.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| assignment\_ids[] |  | string | no description |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/effective_due_dates
  -X GET \
  -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{
  "1": {
     "14": { "due_at": "2015-09-05", "grading_period_id": null, "in_closed_grading_period": false },
     "15": { due_at: null, "grading_period_id": 3, "in_closed_grading_period": true }
  },
  "2": {
     "14": { "due_at": "2015-08-05", "grading_period_id": 3, "in_closed_grading_period": true }
  }
}
```

## [Permissions](#method.courses.permissions) [CoursesController#permissions](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/permissions

**Scope:** 
`url:GET|/api/v1/courses/:course_id/permissions`

Returns permission information for the calling user in the given course. See also the [Account](accounts.html#method.accounts.permissions "Account") and [Group](groups.html#method.groups.permissions "Group") counterparts.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| permissions[] |  | string | List of permissions to check against the authenticated user. Permission names are documented in the [Create a role](roles.html#method.role_overrides.add_role "Create a role") endpoint. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/permissions \
  -H 'Authorization: Bearer <token>' \
  -d 'permissions[]=manage_grades'
  -d 'permissions[]=send_messages'
```

#### Example Response:

#### 

```
{'manage_grades': 'false', 'send_messages': 'true'}
```

## [Get bulk user progress](#method.courses.bulk_user_progress) [CoursesController#bulk\_user\_progress](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### GET /api/v1/courses/:course\_id/bulk\_user\_progress

**Scope:** 
`url:GET|/api/v1/courses/:course_id/bulk_user_progress`

Returns progress information for all users enrolled in the given course.

You must be a user who has permission to view all grades in the course (such as a teacher or administrator).

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/bulk_user_progress \
  -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
[
  {
    "id": 1,
    "display_name": "Test Student 1",
    "avatar_image_url": "https://<canvas>/images/messages/avatar-50.png",
    "html_url": "https://<canvas>/courses/1/users/1",
    "pronouns": null,
    "progress": {
      "requirement_count": 2,
      "requirement_completed_count": 1,
      "next_requirement_url": "https://<canvas>/courses/<course_id>/modules/items/<item_id>",
      "completed_at": null
    }
  },
  {
    "id": 2,
    "display_name": "Test Student 2",
    "avatar_image_url": "https://<canvas>/images/messages/avatar-50.png",
    "html_url": "https://<canvas>/courses/1/users/2",
    "pronouns": null,
    "progress": {
      "requirement_count": 2,
      "requirement_completed_count": 2,
      "next_requirement_url": null,
      "completed_at": "2021-08-10T16:26:08Z"
    }
  }
]
```

## [Remove quiz migration alert](#method.courses.dismiss_migration_limitation_msg) [CoursesController#dismiss\_migration\_limitation\_msg](https://github.com/instructure/canvas-lms/blob/master/app/controllers/courses_controller.rb)

### POST /api/v1/courses/:id/dismiss\_migration\_limitation\_message

**Scope:** 
`url:POST|/api/v1/courses/:id/dismiss_migration_limitation_message`

Remove alert about the limitations of quiz migrations that is displayed to a user in a course

you must be logged in to use this endpoint

#### Example Response:

#### 

```
{ "success": "true" }
```

## [Get course copy status](#method.content_imports.copy_course_status) [ContentImportsController#copy\_course\_status](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_imports_controller.rb)

### GET /api/v1/courses/:course\_id/course\_copy/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/course_copy/:id`

DEPRECATED: Please use the [Content Migrations API](content_migrations.html#method.content_migrations.create "Content Migrations API")

Retrieve the status of a course copy

#### API response field:

* id

  The unique identifier for the course copy.
* created\_at

  The time that the copy was initiated.
* progress

  The progress of the copy as an integer. It is null before the copying starts, and 100 when finished.
* workflow\_state

  The current status of the course copy. Possible values: âcreatedâ, âstartedâ, âcompletedâ, âfailedâ
* status\_url

  The url for the course copy status API endpoint.

#### Example Response:

#### 

```
{'progress':100, 'workflow_state':'completed', 'id':257, 'created_at':'2011-11-17T16:50:06Z', 'status_url':'/api/v1/courses/9457/course_copy/257'}
```

## [Copy course content](#method.content_imports.copy_course_content) [ContentImportsController#copy\_course\_content](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_imports_controller.rb)

### POST /api/v1/courses/:course\_id/course\_copy

**Scope:** 
`url:POST|/api/v1/courses/:course_id/course_copy`

DEPRECATED: Please use the [Content Migrations API](content_migrations.html#method.content_migrations.create "Content Migrations API")

Copies content from one course into another. The default is to copy all course content. You can control specific types to copy by using either the âexceptâ option or the âonlyâ option.

The response is the same as the course copy status endpoint

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| source\_course |  | string | ID or SIS-ID of the course to copy the content from |
| except[] |  | string | A list of the course content types to exclude, all areas not listed will be copied.  Allowed values: `course_settings`, `assignments`, `external_tools`, `files`, `topics`, `calendar_events`, `quizzes`, `wiki_pages`, `modules`, `outcomes` |
| only[] |  | string | A list of the course content types to copy, all areas not listed will not be copied.  Allowed values: `course_settings`, `assignments`, `external_tools`, `files`, `topics`, `calendar_events`, `quizzes`, `wiki_pages`, `modules`, `outcomes` |