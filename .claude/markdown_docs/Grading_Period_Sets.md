# Grading Period Sets

# Grading Period Sets API



Manage grading period sets

### A GradingPeriodSets object looks like:

```
{
  // The title of the grading period set.
  "title": "Hello World",
  // If true, the grading periods in the set are weighted.
  "weighted": true,
  // If true, the totals for all grading periods in the set are displayed.
  "display_totals_for_all_grading_periods": true
}
```

## [List grading period sets](#method.grading_period_sets.index) [GradingPeriodSetsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/grading_period_sets_controller.rb)

### GET /api/v1/accounts/:account\_id/grading\_period\_sets

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/grading_period_sets`

Returns the paginated list of grading period sets

#### Example Response:

#### 

```
{
  "grading_period_set": [GradingPeriodGroup]
}
```

## [Create a grading period set](#method.grading_period_sets.create) [GradingPeriodSetsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/grading_period_sets_controller.rb)

### POST /api/v1/accounts/:account\_id/grading\_period\_sets

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/grading_period_sets`

Create and return a new grading period set

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| enrollment\_term\_ids[] |  | Array | A list of associated term ids for the grading period set |
| grading\_period\_set[title] | Required | string | The title of the grading period set |
| grading\_period\_set[weighted] |  | boolean | A boolean to determine whether the grading periods in the set are weighted |
| grading\_period\_set[display\_totals\_for\_all\_grading\_periods] |  | boolean | A boolean to determine whether the totals for all grading periods in the set are displayed |

#### Example Response:

#### 

```
{
  "grading_period_set": [GradingPeriodGroup]
}
```

## [Update a grading period set](#method.grading_period_sets.update) [GradingPeriodSetsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/grading_period_sets_controller.rb)

### PATCH /api/v1/accounts/:account\_id/grading\_period\_sets/:id

**Scope:** 
`url:PATCH|/api/v1/accounts/:account_id/grading_period_sets/:id`

Update an existing grading period set

**204 No Content** response code is returned if the update was successful.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| enrollment\_term\_ids[] |  | Array | A list of associated term ids for the grading period set |
| grading\_period\_set[][title] | Required | string | The title of the grading period set |
| grading\_period\_set[][weighted] |  | boolean | A boolean to determine whether the grading periods in the set are weighted |
| grading\_period\_set[][display\_totals\_for\_all\_grading\_periods] |  | boolean | A boolean to determine whether the totals for all grading periods in the set are displayed |

## [Delete a grading period set](#method.grading_period_sets.destroy) [GradingPeriodSetsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/grading_period_sets_controller.rb)

### DELETE /api/v1/accounts/:account\_id/grading\_period\_sets/:id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/grading_period_sets/:id`

**204 No Content** response code is returned if the deletion was successful.