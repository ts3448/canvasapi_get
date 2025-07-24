# Logins

# Logins API



API for creating and viewing user logins under an account

## [List user logins](#method.pseudonyms.index) [PseudonymsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/pseudonyms_controller.rb)

### GET /api/v1/accounts/:account\_id/logins

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/logins`

### GET /api/v1/users/:user\_id/logins

**Scope:** 
`url:GET|/api/v1/users/:user_id/logins`

Given a user ID, return a paginated list of that userâs logins for the given account.

#### API response field:

* account\_id

  The ID of the loginâs account.
* id

  The unique, numeric ID for the login.
* sis\_user\_id

  The loginâs unique SIS ID.
* integration\_id

  The loginâs unique integration ID.
* unique\_id

  The unique ID for the login.
* user\_id

  The unique ID of the loginâs user.
* authentication\_provider\_id

  The ID of the authentication provider that this login is associated with
* authentication\_provider\_type

  The type of the authentication provider that this login is associated with
* workflow\_state

  The current status of the login
* declared\_user\_type

  The declared intention for this userâs role

#### Example Response:

#### 

```
[
  {
    "account_id": 1,
    "id" 2,
    "sis_user_id": null,
    "unique_id": "belieber@example.com",
    "user_id": 2,
    "authentication_provider_id": 1,
    "authentication_provider_type": "facebook",
    "workflow_state": "active",
    "declared_user_type": null,
  }
]
```

## [Kickoff password recovery flow](#method.pseudonyms.forgot_password) [PseudonymsController#forgot\_password](https://github.com/instructure/canvas-lms/blob/master/app/controllers/pseudonyms_controller.rb)

### POST /api/v1/users/reset\_password

**Scope:** 
`url:POST|/api/v1/users/reset_password`

Given a user email, generate a nonce and email it to the user

#### API response field:

* requested

  The recovery request status

#### Example Response:

#### 

```
{
  "requested": true
}
```

## [Create a user login](#method.pseudonyms.create) [PseudonymsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/pseudonyms_controller.rb)

### POST /api/v1/accounts/:account\_id/logins

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/logins`

Create a new login for an existing user in the given account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user[id] | Required | string | The ID of the user to create the login for. |
| login[unique\_id] | Required | string | The unique ID for the new login. |
| login[password] |  | string | The new loginâs password. |
| login[sis\_user\_id] |  | string | SIS ID for the login. To set this parameter, the caller must be able to manage SIS permissions on the account. |
| login[integration\_id] |  | string | Integration ID for the login. To set this parameter, the caller must be able to manage SIS permissions on the account. The Integration ID is a secondary identifier useful for more complex SIS integrations. |
| login[authentication\_provider\_id] |  | string | The authentication provider this login is associated with. Logins associated with a specific provider can only be used with that provider. Legacy providers (LDAP, CAS, SAML) will search for logins associated with them, or unassociated logins. New providers will only search for logins explicitly associated with them. This can be the integer ID of the provider, or the type of the provider (in which case, it will find the first matching provider). |
| login[declared\_user\_type] |  | string | The declared intention of the user type. This can be set, but does not change any Canvas functionality with respect to their access. A user can still be a teacher, admin, student, etc. in any particular context without regard to this setting. This can be used for administrative purposes for integrations to be able to more easily identify why the user was created. Valid values are:   ``` * administrative * observer * staff * student * student_other * teacher  ``` |
| user[existing\_user\_id] |  | string | A Canvas User ID to identify a user in a trusted account (alternative to âid`, `existing\_sis\_user\_id`, or `existing\_integration\_id`). This parameter is not available in OSS Canvas. |
| user[existing\_integration\_id] |  | string | An Integration ID to identify a user in a trusted account (alternative to âid`, `existing\_user\_id`, or `existing\_sis\_user\_id`). This parameter is not available in OSS Canvas. |
| user[existing\_sis\_user\_id] |  | string | An SIS User ID to identify a user in a trusted account (alternative to âid`, `existing\_integration\_id`, or `existing\_user\_id`). This parameter is not available in OSS Canvas. |
| user[trusted\_account] |  | string | The domain of the account to search for the user. This field is required when identifying a user in a trusted account. This parameter is not available in OSS Canvas. |

#### Example Request:

#### 

```
#create a facebook login for user with ID 123
curl 'https://<canvas>/api/v1/accounts/<account_id>/logins' \
     -F 'user[id]=123' \
     -F 'login[unique_id]=112233445566' \
     -F 'login[authentication_provider_id]=facebook' \
     -H 'Authorization: Bearer <token>'
```

#### 

```
#create a login for user in another trusted account:
curl 'https://<canvas>/api/v1/accounts/<account_id>/logins' \
     -F 'user[existing_user_sis_id]=SIS42' \
     -F 'user[trusted_account]=canvas.example.edu' \
     -F 'login[unique_id]=112233445566' \
     -H 'Authorization: Bearer <token>'
```

## [Edit a user login](#method.pseudonyms.update) [PseudonymsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/pseudonyms_controller.rb)

### PUT /api/v1/accounts/:account\_id/logins/:id

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/logins/:id`

Update an existing login for a user in the given account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| login[unique\_id] |  | string | The new unique ID for the login. |
| login[password] |  | string | The new password for the login. Admins can only set a password for another user if the âPassword setting by adminsâ account setting is enabled. |
| login[old\_password] |  | string | The prior password for the login. Required if the caller is changing their own password. |
| login[sis\_user\_id] |  | string | SIS ID for the login. To set this parameter, the caller must be able to manage SIS permissions on the account. |
| login[integration\_id] |  | string | Integration ID for the login. To set this parameter, the caller must be able to manage SIS permissions on the account. The Integration ID is a secondary identifier useful for more complex SIS integrations. |
| login[authentication\_provider\_id] |  | string | The authentication provider this login is associated with. Logins associated with a specific provider can only be used with that provider. Legacy providers (LDAP, CAS, SAML) will search for logins associated with them, or unassociated logins. New providers will only search for logins explicitly associated with them. This can be the integer ID of the provider, or the type of the provider (in which case, it will find the first matching provider). To unassociate from a known provider, specify null or an empty string. |
| login[workflow\_state] |  | string | Used to suspend or re-activate a login.  Allowed values: `active`, `suspended` |
| login[declared\_user\_type] |  | string | The declared intention of the user type. This can be set, but does not change any Canvas functionality with respect to their access. A user can still be a teacher, admin, student, etc. in any particular context without regard to this setting. This can be used for administrative purposes for integrations to be able to more easily identify why the user was created. Valid values are:   ``` * administrative * observer * staff * student * student_other * teacher  ``` |
| override\_sis\_stickiness |  | boolean | Default is true. If false, any fields containing âstickyâ changes will not be updated. See SIS CSV Format documentation for information on which fields can have SIS stickiness |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/accounts/:account_id/logins/:login_id \
  -H "Authorization: Bearer <ACCESS-TOKEN>" \
  -X PUT
```

#### Example Response:

#### 

```
{
  "id": 1,
  "user_id": 2,
  "account_id": 3,
  "unique_id": "bieber@example.com",
  "created_at": "2020-01-29T19:33:35Z",
  "sis_user_id": null,
  "integration_id": null,
  "authentication_provider_id": null,
  "workflow_state": "active",
  "declared_user_type": "teacher"
}
```

## [Delete a user login](#method.pseudonyms.destroy) [PseudonymsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/pseudonyms_controller.rb)

### DELETE /api/v1/users/:user\_id/logins/:id

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/logins/:id`

Delete an existing login.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/:user_id/logins/:login_id \
  -H "Authorization: Bearer <ACCESS-TOKEN>" \
  -X DELETE
```

#### Example Response:

#### 

```
{
  "unique_id": "bieber@example.com",
  "sis_user_id": null,
  "account_id": 1,
  "id": 12345,
  "user_id": 2
}
```