# Accounts

# Accounts API



API for accessing account data.

### An Account object looks like:

```
{
  // the ID of the Account object
  "id": 2,
  // The display name of the account
  "name": "Canvas Account",
  // The UUID of the account
  "uuid": "WvAHhY5FINzq5IyRIJybGeiXyFkG3SqHUPb7jZY5",
  // The account's parent ID, or null if this is the root account
  "parent_account_id": 1,
  // The ID of the root account, or null if this is the root account
  "root_account_id": 1,
  // The storage quota for the account in megabytes, if not otherwise specified
  "default_storage_quota_mb": 500,
  // The storage quota for a user in the account in megabytes, if not otherwise
  // specified
  "default_user_storage_quota_mb": 50,
  // The storage quota for a group in the account in megabytes, if not otherwise
  // specified
  "default_group_storage_quota_mb": 50,
  // The default time zone of the account. Allowed time zones are
  // {http://www.iana.org/time-zones IANA time zones} or friendlier
  // {http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html Ruby on Rails
  // time zones}.
  "default_time_zone": "America/Denver",
  // The account's identifier in the Student Information System. Only included if
  // the user has permission to view SIS information.
  "sis_account_id": "123xyz",
  // The account's identifier in the Student Information System. Only included if
  // the user has permission to view SIS information.
  "integration_id": "123xyz",
  // The id of the SIS import if created through SIS. Only included if the user
  // has permission to manage SIS information.
  "sis_import_id": 12,
  // The number of courses directly under the account (available via include)
  "course_count": 10,
  // The number of sub-accounts directly under the account (available via include)
  "sub_account_count": 10,
  // The account's identifier that is sent as context_id in LTI launches.
  "lti_guid": "123xyz",
  // The state of the account. Can be 'active' or 'deleted'.
  "workflow_state": "active"
}
```

### A TermsOfService object looks like:

```
{
  // Terms Of Service id
  "id": 1,
  // The given type for the Terms of Service
  "terms_type": "default",
  // Boolean dictating if the user must accept Terms of Service
  "passive": false,
  // The id of the root account that owns the Terms of Service
  "account_id": 1,
  // Content of the Terms of Service
  "content": "To be or not to be that is the question",
  // The type of self registration allowed
  "self_registration_type": "["none", "observer", "all"]"
}
```

### A HelpLink object looks like:

```
{
  // The ID of the help link
  "id": "instructor_question",
  // The name of the help link
  "text": "Ask Your Instructor a Question",
  // The description of the help link
  "subtext": "Questions are submitted to your instructor",
  // The URL of the help link
  "url": "#teacher_feedback",
  // The type of the help link
  "type": "default",
  // The roles that have access to this help link
  "available_to": ["user", "student", "teacher", "admin", "observer", "unenrolled"]
}
```

### A HelpLinks object looks like:

```
{
  // Help link button title
  "help_link_name": "Help And Policies",
  // Help link button icon
  "help_link_icon": "help",
  // Help links defined by the account. Could include default help links.
  "custom_help_links": [{"id":"link1","text":"Custom Link!","subtext":"Something something.","url":"https:\/\/google.com","type":"custom","available_to":["user","student","teacher","admin","observer","unenrolled"],"is_featured":true,"is_new":false,"feature_headline":"Check this out!"}],
  // Default help links provided when account has not set help links of their own.
  "default_help_links": [{"available_to":["student"],"text":"Ask Your Instructor a Question","subtext":"Questions are submitted to your instructor","url":"#teacher_feedback","type":"default","id":"instructor_question","is_featured":false,"is_new":true,"feature_headline":""}, {"available_to":["user","student","teacher","admin","observer","unenrolled"],"text":"Search the Canvas Guides","subtext":"Find answers to common questions","url":"https:\/\/community.canvaslms.com\/t5\/Guides\/ct-p\/guides","type":"default","id":"search_the_canvas_guides","is_featured":false,"is_new":false,"feature_headline":""}, {"available_to":["user","student","teacher","admin","observer","unenrolled"],"text":"Report a Problem","subtext":"If Canvas misbehaves, tell us about it","url":"#create_ticket","type":"default","id":"report_a_problem","is_featured":false,"is_new":false,"feature_headline":""}]
}
```

## [List accounts](#method.accounts.index) [AccountsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts

**Scope:** 
`url:GET|/api/v1/accounts`

A paginated list of accounts that the current user can view or manage. Typically, students and even teachers will get an empty list in response, only account admins can view the accounts that they are in.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Array of additional information to include.  âlti\_guidâ  the âtool\_consumer\_instance\_guidâ that will be sent for this account on LTI launches  âregistration\_settingsâ  returns info about the privacy policy and terms of use  âservicesâ  returns services and whether they are enabled (requires account management permissions)  âcourse\_countâ  returns the number of courses directly under each account  âsub\_account\_countâ  returns the number of sub-accounts directly under each account  Allowed values: `lti_guid`, `registration_settings`, `services`, `course_count`, `sub_account_count` |

Returns a list of
[Account](accounts_(lti).html#Account)
objects

## [Get accounts that admins can manage](#method.accounts.manageable_accounts) [AccountsController#manageable\_accounts](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/manageable\_accounts

**Scope:** 
`url:GET|/api/v1/manageable_accounts`

A paginated list of accounts where the current user has permission to create or manage courses. List will be empty for students and teachers as only admins can view which accounts they are in.

Returns a list of
[Account](accounts_(lti).html#Account)
objects

## [Get accounts that users can create courses in](#method.accounts.course_creation_accounts) [AccountsController#course\_creation\_accounts](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/course\_creation\_accounts

**Scope:** 
`url:GET|/api/v1/course_creation_accounts`

A paginated list of accounts where the current user has permission to create courses.

Returns a list of
[Account](accounts_(lti).html#Account)
objects

## [List accounts for course admins](#method.accounts.course_accounts) [AccountsController#course\_accounts](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/course\_accounts

**Scope:** 
`url:GET|/api/v1/course_accounts`

A paginated list of accounts that the current user can view through their admin course enrollments. (Teacher, TA, or designer enrollments). Only returns âidâ, ânameâ, âworkflow\_stateâ, âroot\_account\_idâ and âparent\_account\_idâ

Returns a list of
[Account](accounts_(lti).html#Account)
objects

## [Get a single account](#method.accounts.show) [AccountsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:id

**Scope:** 
`url:GET|/api/v1/accounts/:id`

Retrieve information on an individual account, given by id or sis sis\_account\_id.

Returns an
[Account](accounts_(lti).html#Account)
object

## [Settings](#method.accounts.show_settings) [AccountsController#show\_settings](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/settings

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/settings`

Returns a JSON object containing a subset of settings for the specified account. Itâs possible an empty set will be returned if no settings are applicable. The caller must be an Account admin with the manage\_account\_settings permission.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/<account_id>/settings \
  -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{"microsoft_sync_enabled": true, "microsoft_sync_login_attribute_suffix": false}
```

## [List environment settings](#method.accounts.environment) [AccountsController#environment](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/settings/environment

**Scope:** 
`url:GET|/api/v1/settings/environment`

Return a hash of global settings for the root account This is the same information supplied to the web interface as `ENV.SETTINGS`.

#### Example Request:

#### 

```
curl 'http://<canvas>/api/v1/settings/environment' \
  -H "Authorization: Bearer <token>"
```

#### Example Response:

#### 

```
{ "calendar_contexts_limit": 10, "open_registration": false, ...}
```

## [Permissions](#method.accounts.permissions) [AccountsController#permissions](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/permissions

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/permissions`

Returns permission information for the calling user and the given account. You may use âself` as the account id to check permissions against the domain root account. The caller must have an account role or admin (teacher/TA/designer) enrollment in a course in the account.

See also the [Course](courses.html#method.courses.permissions "Course") and [Group](groups.html#method.groups.permissions "Group") counterparts.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| permissions[] |  | string | List of permissions to check against the authenticated user. Permission names are documented in the [Create a role](roles.html#method.role_overrides.add_role "Create a role") endpoint. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/self/permissions \
  -H 'Authorization: Bearer <token>' \
  -d 'permissions[]=manage_account_memberships' \
  -d 'permissions[]=become_user'
```

#### Example Response:

#### 

```
{'manage_account_memberships': 'false', 'become_user': 'true'}
```

## [Get the sub-accounts of an account](#method.accounts.sub_accounts) [AccountsController#sub\_accounts](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/sub\_accounts

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/sub_accounts`

List accounts that are sub-accounts of the given account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| recursive |  | boolean | If true, the entire account tree underneath this account will be returned (though still paginated). If false, only direct sub-accounts of this account will be returned. Defaults to false. |
| order |  | string | Sorts the accounts by id or name. Only applies when recursive is false. Defaults to id.  Allowed values: `id`, `name` |
| include[] |  | string | Array of additional information to include.  âcourse\_countâ  returns the number of courses directly under each account  âsub\_account\_countâ  returns the number of sub-accounts directly under each account  Allowed values: `course_count`, `sub_account_count` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/<account_id>/sub_accounts \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[Account](accounts_(lti).html#Account)
objects

## [Get the Terms of Service](#method.accounts.terms_of_service) [AccountsController#terms\_of\_service](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/terms\_of\_service

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/terms_of_service`

Returns the terms of service for that account

Returns a
[TermsOfService](accounts.html#TermsOfService)
object

## [Get help links](#method.accounts.help_links) [AccountsController#help\_links](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/help\_links

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/help_links`

Returns the help links for that account

Returns a
[HelpLinks](accounts.html#HelpLinks)
object

## [Get the manually-created courses sub-account for the domain root account](#method.accounts.manually_created_courses_account) [AccountsController#manually\_created\_courses\_account](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/manually\_created\_courses\_account

**Scope:** 
`url:GET|/api/v1/manually_created_courses_account`

## [List active courses in an account](#method.accounts.courses_api) [AccountsController#courses\_api](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### GET /api/v1/accounts/:account\_id/courses

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/courses`

Retrieve a paginated list of courses in this account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| with\_enrollments |  | boolean | If true, include only courses with at least one enrollment. If false, include only courses with no enrollments. If not present, do not filter on course enrollment status. |
| enrollment\_type[] |  | string | If set, only return courses that have at least one user enrolled in in the course with one of the specified enrollment types.  Allowed values: `teacher`, `student`, `ta`, `observer`, `designer` |
| published |  | boolean | If true, include only published courses. If false, exclude published courses. If not present, do not filter on published status. |
| completed |  | boolean | If true, include only completed courses (these may be in state âcompletedâ, or their enrollment term may have ended). If false, exclude completed courses. If not present, do not filter on completed status. |
| blueprint |  | boolean | If true, include only blueprint courses. If false, exclude them. If not present, do not filter on this basis. |
| blueprint\_associated |  | boolean | If true, include only courses that inherit content from a blueprint course. If false, exclude them. If not present, do not filter on this basis. |
| public |  | boolean | If true, include only public courses. If false, exclude them. If not present, do not filter on this basis. |
| by\_teachers[] |  | integer | List of User IDs of teachers; if supplied, include only courses taught by one of the referenced users. |
| by\_subaccounts[] |  | integer | List of Account IDs; if supplied, include only courses associated with one of the referenced subaccounts. |
| hide\_enrollmentless\_courses |  | boolean | If present, only return courses that have at least one enrollment. Equivalent to âwith\_enrollments=trueâ; retained for compatibility. |
| state[] |  | string | If set, only return courses that are in the given state(s). By default, all states but âdeletedâ are returned.  Allowed values: `created`, `claimed`, `available`, `completed`, `deleted`, `all` |
| enrollment\_term\_id |  | integer | If set, only includes courses from the specified term. |
| search\_term |  | string | The partial course name, code, or full ID to match and return in the results list. Must be at least 3 characters. |
| include[] |  | string | * All explanations can be seen in the [Course API index documentation](courses.html#method.courses.index "Course API index documentation") * âsectionsâ, âneeds\_grading\_countâ and âtotal\_scoresâ are not valid options at the account level   Allowed values: `syllabus_body`, `term`, `course_progress`, `storage_quota_used_mb`, `total_students`, `teachers`, `account_name`, `concluded`, `post_manually` |
| sort |  | string | The column to sort results by.  Allowed values: `course_status`, `course_name`, `sis_course_id`, `teacher`, `account_name` |
| order |  | string | The order to sort the given column by.  Allowed values: `asc`, `desc` |
| search\_by |  | string | The filter to search by. âcourseâ searches for course names, course codes, and SIS IDs. âteacherâ searches for teacher names  Allowed values: `course`, `teacher` |
| starts\_before |  | Date | If set, only return courses that start before the value (inclusive) or their enrollment term starts before the value (inclusive) or both the courseâs start\_at and the enrollment termâs start\_at are set to null. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. |
| ends\_after |  | Date | If set, only return courses that end after the value (inclusive) or their enrollment term ends after the value (inclusive) or both the courseâs end\_at and the enrollment termâs end\_at are set to null. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. |
| homeroom |  | boolean | If set, only return homeroom courses. |

Returns a list of
[Course](courses.html#Course)
objects

## [Update an account](#method.accounts.update) [AccountsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### PUT /api/v1/accounts/:id

**Scope:** 
`url:PUT|/api/v1/accounts/:id`

Update an existing account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| account[name] |  | string | Updates the account name |
| account[sis\_account\_id] |  | string | Updates the account sis\_account\_id Must have manage\_sis permission and must not be a root\_account. |
| account[default\_time\_zone] |  | string | The default time zone of the account. Allowed time zones are [IANA time zones](http://www.iana.org/time-zones "IANA time zones") or friendlier [Ruby on Rails time zones](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html "Ruby on Rails time zones"). |
| account[default\_storage\_quota\_mb] |  | integer | The default course storage quota to be used, if not otherwise specified. |
| account[default\_user\_storage\_quota\_mb] |  | integer | The default user storage quota to be used, if not otherwise specified. |
| account[default\_group\_storage\_quota\_mb] |  | integer | The default group storage quota to be used, if not otherwise specified. |
| account[course\_template\_id] |  | integer | The ID of a course to be used as a template for all newly created courses. Empty means to inherit the setting from parent account, 0 means to not use a template even if a parent account has one set. The course must be marked as a template. |
| account[parent\_account\_id] |  | integer | The ID of a parent account to move the account to. The new parent account must be in the same root account as the original. The hierarchy of sub-accounts will be preserved in the new parent account. The caller must be an administrator in both the original parent account and the new parent account. |
| account[settings][restrict\_student\_past\_view][value] |  | boolean | Restrict students from viewing courses after end date |
| account[settings][restrict\_student\_past\_view][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][restrict\_student\_future\_view][value] |  | boolean | Restrict students from viewing courses before start date |
| account[settings][microsoft\_sync\_enabled] |  | boolean | Determines whether this account has Microsoft Teams Sync enabled or not.  Note that if you are altering Microsoft Teams sync settings you must enable the Microsoft Group enrollment syncing feature flag. In addition, if you are enabling Microsoft Teams sync, you must also specify a tenant, login attribute, and a remote attribute. Specifying a suffix to use is optional. |
| account[settings][microsoft\_sync\_tenant] |  | string | The tenant this account should use when using Microsoft Teams Sync. This should be an Azure Active Directory domain name. |
| account[settings][microsoft\_sync\_login\_attribute] |  | string | The attribute this account should use to lookup users when using Microsoft Teams Sync. Must be one of âsubâ, âemailâ, âoidâ, âpreferred\_usernameâ, or âintegration\_idâ. |
| account[settings][microsoft\_sync\_login\_attribute\_suffix] |  | string | A suffix that will be appended to the result of the login attribute when associating Canvas users with Microsoft users. Must be under 255 characters and contain no whitespace. This field is optional. |
| account[settings][microsoft\_sync\_remote\_attribute] |  | string | The Active Directory attribute to use when associating Canvas users with Microsoft users. Must be one of âmailâ, âmailNicknameâ, or âuserPrincipalNameâ. |
| account[settings][restrict\_student\_future\_view][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][lock\_all\_announcements][value] |  | boolean | Disable comments on announcements |
| account[settings][lock\_all\_announcements][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][usage\_rights\_required][value] |  | boolean | Copyright and license information must be provided for files before they are published. |
| account[settings][usage\_rights\_required][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][restrict\_student\_future\_listing][value] |  | boolean | Restrict students from viewing future enrollments in course list |
| account[settings][restrict\_student\_future\_listing][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][conditional\_release][value] |  | boolean | Enable or disable individual learning paths for students based on assessment |
| account[settings][conditional\_release][locked] |  | boolean | Lock this setting for sub-accounts and courses |
| account[settings][password\_policy] |  | Hash | Hash of optional password policy configuration parameters for a root account  `allow_login_suspension` boolean  Allow suspension of user logins upon reaching maximum\_login\_attempts  `require_number_characters` boolean  Require the use of number characters when setting up a new password  `require_symbol_characters` boolean  Require the use of symbol characters when setting up a new password  `minimum_character_length` integer  Minimum number of characters required for a new password  `maximum_login_attempts` integer  Maximum number of login attempts before a user is locked out  *Required* feature option:   ``` Enhance password options  ``` |
| account[settings][enable\_as\_k5\_account][value] |  | boolean | Enable or disable Canvas for Elementary for this account |
| account[settings][use\_classic\_font\_in\_k5][value] |  | boolean | Whether or not the classic font is used on the dashboard. Only applies if enable\_as\_k5\_account is true. |
| account[settings][horizon\_account][value] |  | boolean | Enable or disable Canvas Career for this account |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |
| account[settings][lock\_outcome\_proficiency][value] |  | boolean | DEPRECATED  Restrict instructors from changing mastery scale |
| account[lock\_outcome\_proficiency][locked] |  | boolean | DEPRECATED  Lock this setting for sub-accounts and courses |
| account[settings][lock\_proficiency\_calculation][value] |  | boolean | DEPRECATED  Restrict instructors from changing proficiency calculation method |
| account[lock\_proficiency\_calculation][locked] |  | boolean | DEPRECATED  Lock this setting for sub-accounts and courses |
| account[services] |  | Hash | Give this a set of keys and boolean values to enable or disable services matching the keys |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/<account_id> \
  -X PUT \
  -H 'Authorization: Bearer <token>' \
  -d 'account[name]=New account name' \
  -d 'account[default_time_zone]=Mountain Time (US & Canada)' \
  -d 'account[default_storage_quota_mb]=450'
```

Returns an
[Account](accounts_(lti).html#Account)
object

## [Delete a user from the root account](#method.accounts.remove_user) [AccountsController#remove\_user](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### DELETE /api/v1/accounts/:account\_id/users/:user\_id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/users/:user_id`

Delete a user record from a Canvas root account. If a user is associated with multiple root accounts (in a multi-tenant instance of Canvas), this action will NOT remove them from the other accounts.

WARNING: This API will allow a user to remove themselves from the account. If they do this, they wonât be able to make API calls or log into Canvas at that account.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/3/users/5 \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -X DELETE
```

Returns an
[User](users.html#User)
object

## [Delete multiple users from the root account](#method.accounts.remove_users) [AccountsController#remove\_users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### DELETE /api/v1/accounts/:account\_id/users

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/users`

Delete multiple users from a Canvas root account. If a user is associated with multiple root accounts (in a multi-tenant instance of Canvas), this action will NOT remove them from the other accounts.

WARNING: This API will allow a user to remove themselves from the account. If they do this, they wonât be able to make API calls or log into Canvas at that account.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/3/users \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -X DELETE
  -d 'user_ids[]=1' \
  -d 'user_ids[]=2'
```

Returns a
[Progress](progress.html#Progress)
object

## [Update multiple users](#method.accounts.update_users) [AccountsController#update\_users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### PUT /api/v1/accounts/:account\_id/users/bulk\_update

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/users/bulk_update`

Updates multiple users in bulk.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_ids |  | string | Array<Integer>  The IDs of the users to update. |
| user |  | Hash | The attributes to update for each user. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/3/users/bulk_update \
  -X PUT \
  -H 'Authorization: Bearer <token>' \
  -d 'user_ids[]=1' \
  -d 'user_ids[]=2' \
  -d 'user[event]=suspend'
```

Returns a
[Progress](progress.html#Progress)
object

## [Restore a deleted user from a root account](#method.accounts.restore_user) [AccountsController#restore\_user](https://github.com/instructure/canvas-lms/blob/master/app/controllers/accounts_controller.rb)

### PUT /api/v1/accounts/:account\_id/users/:user\_id/restore

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/users/:user_id/restore`

Restore a user record along with the most recently deleted pseudonym from a Canvas root account.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/3/users/5/restore \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -X PUT
```

Returns an
[User](users.html#User)
object

## [Create a new sub-account](#method.sub_accounts.create) [SubAccountsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sub_accounts_controller.rb)

### POST /api/v1/accounts/:account\_id/sub\_accounts

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/sub_accounts`

Add a new sub-account to a given account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| account[name] | Required | string | The name of the new sub-account. |
| account[sis\_account\_id] |  | string | The accountâs identifier in the Student Information System. |
| account[default\_storage\_quota\_mb] |  | integer | The default course storage quota to be used, if not otherwise specified. |
| account[default\_user\_storage\_quota\_mb] |  | integer | The default user storage quota to be used, if not otherwise specified. |
| account[default\_group\_storage\_quota\_mb] |  | integer | The default group storage quota to be used, if not otherwise specified. |

Returns an
[Account](accounts_(lti).html#Account)
object

## [Delete a sub-account](#method.sub_accounts.destroy) [SubAccountsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/sub_accounts_controller.rb)

### DELETE /api/v1/accounts/:account\_id/sub\_accounts/:id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/sub_accounts/:id`

Cannot delete an account with active courses or active sub\_accounts. Cannot delete a root\_account

Returns an
[Account](accounts_(lti).html#Account)
object