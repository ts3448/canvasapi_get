# API Token Scopes

# API Token Scopes API

### BETA: This API resource is not finalized, and there could be breaking changes before its final release.



API for retrieving API scopes

### A Scope object looks like:

```
{
  // The resource the scope is associated with
  "resource": "courses",
  // The localized resource name
  "resource_name": "Courses",
  // The controller the scope is associated to
  "controller": "courses",
  // The controller action the scope is associated to
  "action": "index",
  // The HTTP verb for the scope
  "verb": "GET",
  // The identifier for the scope
  "scope": "url:GET|/api/v1/courses"
}
```

## [List scopes](#method.scopes_api.index) [ScopesApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/scopes_api_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/accounts/:account\_id/scopes

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/scopes`

A list of scopes that can be applied to developer keys and access tokens.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| group\_by |  | string | The attribute to group the scopes by. By default no grouping is done.  Allowed values: `resource_name` |

Returns a list of
[Scope](api_token_scopes.html#Scope)
objects