# Admins

# Admins API



Manage account role assignments

### An Admin object looks like:

```
{
  // The unique identifier for the account role/user assignment.
  "id": 1023,
  // The account role assigned. This can be 'AccountAdmin' or a user-defined role
  // created by the Roles API.
  "role": "AccountAdmin",
  // The user the role is assigned to. See the Users API for details.
  "user": null,
  // The status of the account role/user assignment.
  "workflow_state": "deleted"
}
```

## [List account admins](#method.admins.index) [AdminsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/admins_controller.rb)

### GET /api/v1/accounts/:account\_id/admins

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/admins`

A paginated list of the admins in the account

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id[] |  | [Integer] | Scope the results to those with user IDs equal to any of the IDs specified here. |
| search\_term |  | string | The partial name or full ID of the admins to match and return in the results list. Must be at least 2 characters. |
| include\_deleted |  | boolean | When set to true, returns admins who have been deleted |

Returns a list of
[Admin](admins.html#Admin)
objects

## [Make an account admin](#method.admins.create) [AdminsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/admins_controller.rb)

### POST /api/v1/accounts/:account\_id/admins

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/admins`

Flag an existing user as an admin within the account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id | Required | integer | The id of the user to promote. |
| role |  | string | DEPRECATED  The userâs admin relationship with the account will be  created with the given role. Defaults to âAccountAdminâ. |
| role\_id |  | integer | The userâs admin relationship with the account will be created with the given role. Defaults to the built-in role for âAccountAdminâ. |
| send\_confirmation |  | boolean | Send a notification email to the new admin if true. Default is true. |

Returns an
[Admin](admins.html#Admin)
object

## [Remove account admin](#method.admins.destroy) [AdminsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/admins_controller.rb)

### DELETE /api/v1/accounts/:account\_id/admins/:user\_id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/admins/:user_id`

Remove the rights associated with an account admin role from a user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| role |  | string | DEPRECATED  Account role to remove from the user. |
| role\_id | Required | integer | The id of the role representing the userâs admin relationship with the account. |

Returns an
[Admin](admins.html#Admin)
object

## [List my admin roles](#method.admins.self_roles) [AdminsController#self\_roles](https://github.com/instructure/canvas-lms/blob/master/app/controllers/admins_controller.rb)

### GET /api/v1/accounts/:account\_id/admins/self

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/admins/self`

A paginated list of the current userâs roles in the account. The results are the same as those returned by the [List account admins](admins.html#method.admins.index "List account admins") endpoint with `user_id` set to `self`, except the âAdmins - Add / Removeâ permission is not required.

Returns a list of
[Admin](admins.html#Admin)
objects