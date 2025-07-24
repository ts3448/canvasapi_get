# Feature Flags

# Feature Flags API



Manage optional features in Canvas.

*Deprecated*[2016-01-15] FeatureFlags previously had a locking\_account\_id field;
it was never used, and has been removed. It is still included in API responses
for backwards compatibility reasons. Its value is always null.

### A Feature object looks like:

```
{
  // The symbolic name of the feature, used in FeatureFlags
  "feature": "fancy_wickets",
  // The user-visible name of the feature
  "display_name": "Fancy Wickets",
  // The type of object the feature applies to (RootAccount, Account, Course, or
  // User):
  // * RootAccount features may only be controlled by flags on root accounts.
  // * Account features may be controlled by flags on accounts and their parent
  // accounts.
  // * Course features may be controlled by flags on courses and their parent
  // accounts.
  // * User features may be controlled by flags on users and site admin only.
  "applies_to": "Course",
  // The FeatureFlag that applies to the caller
  "feature_flag": {"feature":"fancy_wickets","state":"allowed"},
  // If true, a feature that is 'allowed' globally will be 'off' by default in
  // root accounts. Otherwise, root accounts inherit the global 'allowed' setting,
  // which allows sub-accounts and courses to turn features on with no root
  // account action.
  "root_opt_in": true,
  // Whether the feature is a feature preview. If true, opting in includes ongoing
  // updates outside the regular release schedule.
  "beta": true,
  // Whether the details of the feature are autoexpanded on page load vs. the user
  // clicking to expand.
  "autoexpand": true,
  // A URL to the release notes describing the feature
  "release_notes_url": "http://canvas.example.com/release_notes#fancy_wickets"
}
```

### A FeatureFlag object looks like:

```
{
  // The type of object to which this flag applies (Account, Course, or User).
  // (This field is not present if this FeatureFlag represents the global Canvas
  // default)
  "context_type": "Account",
  // The id of the object to which this flag applies (This field is not present if
  // this FeatureFlag represents the global Canvas default)
  "context_id": 1038,
  // The feature this flag controls
  "feature": "fancy_wickets",
  // The policy for the feature at this context.  can be 'off', 'allowed',
  // 'allowed_on', or 'on'.
  "state": "allowed",
  // If set, this feature flag cannot be changed in the caller's context because
  // the flag is set 'off' or 'on' in a higher context
  "locked": false
}
```

## [List features](#method.feature_flags.index) [FeatureFlagsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### GET /api/v1/courses/:course\_id/features

**Scope:** 
`url:GET|/api/v1/courses/:course_id/features`

### GET /api/v1/accounts/:account\_id/features

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/features`

### GET /api/v1/users/:user\_id/features

**Scope:** 
`url:GET|/api/v1/users/:user_id/features`

A paginated list of all features that apply to a given Account, Course, or User.

#### Example Request:

#### 

```
curl 'http://<canvas>/api/v1/courses/1/features' \
  -H "Authorization: Bearer <token>"
```

Returns a list of
[Feature](feature_flags.html#Feature)
objects

## [List enabled features](#method.feature_flags.enabled_features) [FeatureFlagsController#enabled\_features](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### GET /api/v1/courses/:course\_id/features/enabled

**Scope:** 
`url:GET|/api/v1/courses/:course_id/features/enabled`

### GET /api/v1/accounts/:account\_id/features/enabled

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/features/enabled`

### GET /api/v1/users/:user\_id/features/enabled

**Scope:** 
`url:GET|/api/v1/users/:user_id/features/enabled`

A paginated list of all features that are enabled on a given Account, Course, or User. Only the feature names are returned.

#### Example Request:

#### 

```
curl 'http://<canvas>/api/v1/courses/1/features/enabled' \
  -H "Authorization: Bearer <token>"
```

#### Example Response:

#### 

```
["fancy_wickets", "automatic_essay_grading", "telepathic_navigation"]
```

## [List environment features](#method.feature_flags.environment) [FeatureFlagsController#environment](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### GET /api/v1/features/environment

**Scope:** 
`url:GET|/api/v1/features/environment`

Return a hash of global feature options that pertain to the Canvas user interface. This is the same information supplied to the web interface as `ENV.FEATURES`.

#### Example Request:

#### 

```
curl 'http://<canvas>/api/v1/features/environment' \
  -H "Authorization: Bearer <token>"
```

#### Example Response:

#### 

```
{ "telepathic_navigation": true, "fancy_wickets": true, "automatic_essay_grading": false }
```

## [Get feature flag](#method.feature_flags.show) [FeatureFlagsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### GET /api/v1/courses/:course\_id/features/flags/:feature

**Scope:** 
`url:GET|/api/v1/courses/:course_id/features/flags/:feature`

### GET /api/v1/accounts/:account\_id/features/flags/:feature

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/features/flags/:feature`

### GET /api/v1/users/:user\_id/features/flags/:feature

**Scope:** 
`url:GET|/api/v1/users/:user_id/features/flags/:feature`

Get the feature flag that applies to a given Account, Course, or User. The flag may be defined on the object, or it may be inherited from a parent account. You can look at the context\_id and context\_type of the returned object to determine which is the case. If these fields are missing, then the object is the global Canvas default.

#### Example Request:

#### 

```
curl 'http://<canvas>/api/v1/courses/1/features/flags/fancy_wickets' \
  -H "Authorization: Bearer <token>"
```

Returns a
[FeatureFlag](feature_flags.html#FeatureFlag)
object

## [Set feature flag](#method.feature_flags.update) [FeatureFlagsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### PUT /api/v1/courses/:course\_id/features/flags/:feature

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/features/flags/:feature`

### PUT /api/v1/accounts/:account\_id/features/flags/:feature

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/features/flags/:feature`

### PUT /api/v1/users/:user\_id/features/flags/:feature

**Scope:** 
`url:PUT|/api/v1/users/:user_id/features/flags/:feature`

Set a feature flag for a given Account, Course, or User. This call will fail if a parent account sets a feature flag for the same feature in any state other than âallowedâ.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| state |  | string | âoffâ  The feature is not available for the course, user, or account and sub-accounts.  âallowedâ  (valid only on accounts) The feature is off in the account, but may be enabled in sub-accounts and courses by setting a feature flag on the sub-account or course.  âonâ  The feature is turned on unconditionally for the user, course, or account and sub-accounts.  Allowed values: `off`, `allowed`, `on` |

#### Example Request:

#### 

```
curl -X PUT 'http://<canvas>/api/v1/courses/1/features/flags/fancy_wickets' \
  -H "Authorization: Bearer " \
  -F "state=on"
```

Returns a
[FeatureFlag](feature_flags.html#FeatureFlag)
object

## [Remove feature flag](#method.feature_flags.delete) [FeatureFlagsController#delete](https://github.com/instructure/canvas-lms/blob/master/app/controllers/feature_flags_controller.rb)

### DELETE /api/v1/courses/:course\_id/features/flags/:feature

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/features/flags/:feature`

### DELETE /api/v1/accounts/:account\_id/features/flags/:feature

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/features/flags/:feature`

### DELETE /api/v1/users/:user\_id/features/flags/:feature

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/features/flags/:feature`

Remove feature flag for a given Account, Course, or User. (Note that the flag must be defined on the Account, Course, or User directly.) The object will then inherit the feature flags from a higher account, if any exist. If this flag was âonâ or âoffâ, then lower-level account flags that were masked by this one will apply again.

#### Example Request:

#### 

```
curl -X DELETE 'http://<canvas>/api/v1/courses/1/features/flags/fancy_wickets' \
  -H "Authorization: Bearer <token>"
```

Returns a
[FeatureFlag](feature_flags.html#FeatureFlag)
object