# Access Tokens

# Access Tokens API



## [Show an access token](#method.tokens.show) [TokensController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/tokens_controller.rb)

### GET /api/v1/users/:user\_id/tokens/:id

**Scope:** 
`url:GET|/api/v1/users/:user_id/tokens/:id`

The ID can be the actual database ID of the token, or the âtoken\_hintâ value.

## [Create an access token](#method.tokens.create) [TokensController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/tokens_controller.rb)

### POST /api/v1/users/:user\_id/tokens

**Scope:** 
`url:POST|/api/v1/users/:user_id/tokens`

Create a new access token for the specified user. If the user is not the current user, the token will be created as âpendingâ, and must be activated by the user before it can be used.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| token[purpose] | Required | string | The purpose of the token. |
| token[expires\_at] |  | DateTime | The time at which the token will expire. |
| token[scopes][] |  | Array | The scopes to associate with the token. Ignored if the default developer key does not have the âenable scopesâ option enabled. In such cases, the token will inherit the userâs permissions instead. |

## [Update an access token](#method.tokens.update) [TokensController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/tokens_controller.rb)

### PUT /api/v1/users/:user\_id/tokens/:id

**Scope:** 
`url:PUT|/api/v1/users/:user_id/tokens/:id`

Update an existing access token.

The ID can be the actual database ID of the token, or the âtoken\_hintâ value.

Regenerating an expired token requires a new expiration date.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| token[purpose] |  | string | The purpose of the token. |
| token[expires\_at] |  | DateTime | The time at which the token will expire. |
| token[scopes][] |  | Array | The scopes to associate with the token. |
| token[regenerate] |  | boolean | Regenerate the actual token. |

## [Delete an access token](#method.tokens.destroy) [TokensController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/tokens_controller.rb)

### DELETE /api/v1/users/:user\_id/tokens/:id

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/tokens/:id`

The ID can be the actual database ID of the token, or the âtoken\_hintâ value.