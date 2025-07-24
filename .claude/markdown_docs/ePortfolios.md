# ePortfolios

# ePortfolios API



### An ePortfolio object looks like:

```
{
  // The database ID of the ePortfolio
  "id": 1,
  // The user ID to which the ePortfolio belongs
  "user_id": 1,
  // The name of the ePortfolio
  "name": "My Academic Journey",
  // Whether or not the ePortfolio is visible without authentication
  "public": true,
  // The creation timestamp for the ePortfolio
  "created_at": "2021-09-20T18:59:37Z",
  // The timestamp of the last time any of the ePortfolio attributes changed
  "updated_at": "2021-09-20T18:59:37Z",
  // The state of the ePortfolio. Either 'active' or 'deleted'
  "workflow_state": "active",
  // The timestamp when the ePortfolio was deleted, or else null
  "deleted_at": "2021-09-20T18:59:37Z",
  // A flag indicating whether the ePortfolio has been
  // flagged or moderated as spam. One of 'flagged_as_possible_spam',
  // 'marked_as_safe', 'marked_as_spam', or null
  "spam_status": null
}
```

### An ePortfolioPage object looks like:

```
{
  // The database ID of the ePortfolio
  "id": 1,
  // The ePortfolio ID to which the entry belongs
  "eportfolio_id": 1,
  // The positional order of the entry in the list
  "position": 1,
  // The name of the ePortfolio
  "name": "My Academic Journey",
  // The user entered content of the entry
  "content": "A long time ago...",
  // The creation timestamp for the ePortfolio
  "created_at": "2021-09-20T18:59:37Z",
  // The timestamp of the last time any of the ePortfolio attributes changed
  "updated_at": "2021-09-20T18:59:37Z"
}
```

## [Get all ePortfolios for a User](#method.eportfolios_api.index) [EportfoliosApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### GET /api/v1/users/:user\_id/eportfolios

**Scope:** 
`url:GET|/api/v1/users/:user_id/eportfolios`

Get a list of all ePortfolios for the specified user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | deleted  Include deleted ePortfolios. Only available to admins who can  moderate\_user\_content.  Allowed values: `deleted` |

Returns a list of
[ePortfolio](e_portfolios.html#ePortfolio)
objects

## [Get an ePortfolio](#method.eportfolios_api.show) [EportfoliosApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### GET /api/v1/eportfolios/:id

**Scope:** 
`url:GET|/api/v1/eportfolios/:id`

Get details for a single ePortfolio.

Returns an
[ePortfolio](e_portfolios.html#ePortfolio)
object

## [Delete an ePortfolio](#method.eportfolios_api.delete) [EportfoliosApiController#delete](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### DELETE /api/v1/eportfolios/:id

**Scope:** 
`url:DELETE|/api/v1/eportfolios/:id`

Mark an ePortfolio as deleted.

Returns an
[ePortfolio](e_portfolios.html#ePortfolio)
object

## [Get ePortfolio Pages](#method.eportfolios_api.pages) [EportfoliosApiController#pages](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### GET /api/v1/eportfolios/:eportfolio\_id/pages

**Scope:** 
`url:GET|/api/v1/eportfolios/:eportfolio_id/pages`

Get details for the pages of an ePortfolio

Returns a list of
[ePortfolioPage](e_portfolios.html#ePortfolioPage)
objects

## [Moderate an ePortfolio](#method.eportfolios_api.moderate) [EportfoliosApiController#moderate](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### PUT /api/v1/eportfolios/:eportfolio\_id/moderate

**Scope:** 
`url:PUT|/api/v1/eportfolios/:eportfolio_id/moderate`

Update the spam\_status of an eportfolio. Only available to admins who can moderate\_user\_content.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| spam\_status |  | string | The spam status for the ePortfolio  Allowed values: `marked_as_spam`, `marked_as_safe` |

Returns an
[ePortfolio](e_portfolios.html#ePortfolio)
object

## [Moderate all ePortfolios for a User](#method.eportfolios_api.moderate_all) [EportfoliosApiController#moderate\_all](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### PUT /api/v1/users/:user\_id/eportfolios

**Scope:** 
`url:PUT|/api/v1/users/:user_id/eportfolios`

Update the spam\_status for all active eportfolios of a user. Only available to admins who can moderate\_user\_content.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| spam\_status |  | string | The spam status for all the ePortfolios  Allowed values: `marked_as_spam`, `marked_as_safe` |

## [Restore a deleted ePortfolio](#method.eportfolios_api.restore) [EportfoliosApiController#restore](https://github.com/instructure/canvas-lms/blob/master/app/controllers/eportfolios_api_controller.rb)

### PUT /api/v1/eportfolios/:eportfolio\_id/restore

**Scope:** 
`url:PUT|/api/v1/eportfolios/:eportfolio_id/restore`

Restore an ePortfolio back to active that was previously deleted. Only available to admins who can moderate\_user\_content.

Returns an
[ePortfolio](e_portfolios.html#ePortfolio)
object