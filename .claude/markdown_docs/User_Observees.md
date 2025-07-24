# User Observees

# User Observees API



API for accessing information about the users a user is observing.

### A PairingCode object looks like:

```
// A code used for linking a user to a student to observe them.
{
  // The ID of the user.
  "user_id": 2,
  // The actual code to be sent to other APIs
  "code": "abc123",
  // When the code expires
  "expires_at": "2012-05-30T17:45:25Z",
  // The current status of the code
  "workflow_state": "active"
}
```

## [List observees](#method.user_observees.index) [UserObserveesController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### GET /api/v1/users/:user\_id/observees

**Scope:** 
`url:GET|/api/v1/users/:user_id/observees`

A paginated list of the users that the given user is observing.

**Note:** all users are allowed to list their own observees. Administrators can list other usersâ observees.

The returned observees will include an attribute âobservation\_link\_root\_account\_idsâ, a list of ids for the root accounts the observer and observee are linked on. The observer will only be able to observe in courses associated with these root accounts.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âavatar\_urlâ: Optionally include avatar\_url.   Allowed values: `avatar_url` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observees \
     -X GET \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[User](users.html#User)
objects

## [List observers](#method.user_observees.observers) [UserObserveesController#observers](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### GET /api/v1/users/:user\_id/observers

**Scope:** 
`url:GET|/api/v1/users/:user_id/observers`

A paginated list of the observers of a given user.

**Note:** all users are allowed to list their own observers. Administrators can list other usersâ observers.

The returned observers will include an attribute âobservation\_link\_root\_account\_idsâ, a list of ids for the root accounts the observer and observee are linked on. The observer will only be able to observe in courses associated with these root accounts.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | * âavatar\_urlâ: Optionally include avatar\_url.   Allowed values: `avatar_url` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observers \
     -X GET \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[User](users.html#User)
objects

## [Add an observee with credentials](#method.user_observees.create) [UserObserveesController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### POST /api/v1/users/:user\_id/observees

**Scope:** 
`url:POST|/api/v1/users/:user_id/observees`

Register the given user to observe another user, given the observeeâs credentials.

**Note:** all users are allowed to add their own observees, given the observeeâs credentials or access token are provided. Administrators can add observees given credentials, access token or the [observeeâs id](user_observees.html#method.user_observees.update "observeeâs id").

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| observee[unique\_id] |  | string | The login id for the user to observe. Required if access\_token is omitted. |
| observee[password] |  | string | The password for the user to observe. Required if access\_token is omitted. |
| access\_token |  | string | The access token for the user to observe. Required if `observee[unique_id]` or `observee[password]` are omitted. |
| pairing\_code |  | string | A generated pairing code for the user to observe. Required if the Observer pairing code feature flag is enabled |
| root\_account\_id |  | integer | The ID for the root account to associate with the observation link. Defaults to the current domain account. If âallâ is specified, a link will be created for each root account associated to both the observer and observee. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observees \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -F 'observee[unique_id]=UNIQUE_ID' \
     -F 'observee[password]=PASSWORD'
```

Returns an
[User](users.html#User)
object

## [Show an observee](#method.user_observees.show) [UserObserveesController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### GET /api/v1/users/:user\_id/observees/:observee\_id

**Scope:** 
`url:GET|/api/v1/users/:user_id/observees/:observee_id`

Gets information about an observed user.

**Note:** all users are allowed to view their own observees.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observees/<observee_id> \
     -X GET \
     -H 'Authorization: Bearer <token>'
```

Returns an
[User](users.html#User)
object

## [Show an observer](#method.user_observees.show_observer) [UserObserveesController#show\_observer](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### GET /api/v1/users/:user\_id/observers/:observer\_id

**Scope:** 
`url:GET|/api/v1/users/:user_id/observers/:observer_id`

Gets information about an observer.

**Note:** all users are allowed to view their own observers.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observers/<observer_id> \
     -X GET \
     -H 'Authorization: Bearer <token>'
```

Returns an
[User](users.html#User)
object

## [Add an observee](#method.user_observees.update) [UserObserveesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### PUT /api/v1/users/:user\_id/observees/:observee\_id

**Scope:** 
`url:PUT|/api/v1/users/:user_id/observees/:observee_id`

Registers a user as being observed by the given user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| root\_account\_id |  | integer | The ID for the root account to associate with the observation link. If not specified, a link will be created for each root account associated to both the observer and observee. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observees/<observee_id> \
     -X PUT \
     -H 'Authorization: Bearer <token>'
```

Returns an
[User](users.html#User)
object

## [Remove an observee](#method.user_observees.destroy) [UserObserveesController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/user_observees_controller.rb)

### DELETE /api/v1/users/:user\_id/observees/:observee\_id

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/observees/:observee_id`

Unregisters a user as being observed by the given user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| root\_account\_id |  | integer | If specified, only removes the link for the given root account |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/<user_id>/observees/<observee_id> \
     -X DELETE \
     -H 'Authorization: Bearer <token>'
```

Returns an
[User](users.html#User)
object

## [Create observer pairing code](#method.observer_pairing_codes_api.create) [ObserverPairingCodesApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/observer_pairing_codes_api_controller.rb)

### POST /api/v1/users/:user\_id/observer\_pairing\_codes

**Scope:** 
`url:POST|/api/v1/users/:user_id/observer_pairing_codes`

If the user is a student, will generate a code to be used with self registration or observees APIs to link another user to this student.

Returns a
[PairingCode](user_observees.html#PairingCode)
object