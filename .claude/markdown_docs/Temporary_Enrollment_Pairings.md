# Temporary Enrollment Pairings

# Temporary Enrollment Pairings API



### A TemporaryEnrollmentPairing object looks like:

```
// A pairing unique to that enrollment period given to a recipient of that
// temporary enrollment.
{
  // the ID of the temporary enrollment pairing
  "id": 1,
  // The current status of the temporary enrollment pairing
  "workflow_state": "active"
}
```

## [List temporary enrollment pairings](#method.temporary_enrollment_pairings_api.index) [TemporaryEnrollmentPairingsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/temporary_enrollment_pairings_api_controller.rb)

### GET /api/v1/accounts/:account\_id/temporary\_enrollment\_pairings

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/temporary_enrollment_pairings`

Returns the list of temporary enrollment pairings for a root account.

Returns a list of
[TemporaryEnrollmentPairing](temporary_enrollment_pairings.html#TemporaryEnrollmentPairing)
objects

## [Get a single temporary enrollment pairing](#method.temporary_enrollment_pairings_api.show) [TemporaryEnrollmentPairingsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/temporary_enrollment_pairings_api_controller.rb)

### GET /api/v1/accounts/:account\_id/temporary\_enrollment\_pairings/:id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/temporary_enrollment_pairings/:id`

Returns the temporary enrollment pairing with the given id.

Returns a
[TemporaryEnrollmentPairing](temporary_enrollment_pairings.html#TemporaryEnrollmentPairing)
object

## [New TemporaryEnrollmentPairing](#method.temporary_enrollment_pairings_api.new) [TemporaryEnrollmentPairingsApiController#new](https://github.com/instructure/canvas-lms/blob/master/app/controllers/temporary_enrollment_pairings_api_controller.rb)

### GET /api/v1/accounts/:account\_id/temporary\_enrollment\_pairings/new

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/temporary_enrollment_pairings/new`

Initialize an unsaved Temporary Enrollment Pairing.

Returns a
[TemporaryEnrollmentPairing](temporary_enrollment_pairings.html#TemporaryEnrollmentPairing)
object

## [Create Temporary Enrollment Pairing](#method.temporary_enrollment_pairings_api.create) [TemporaryEnrollmentPairingsApiController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/temporary_enrollment_pairings_api_controller.rb)

### POST /api/v1/accounts/:account\_id/temporary\_enrollment\_pairings

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/temporary_enrollment_pairings`

Create a Temporary Enrollment Pairing.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| workflow\_state |  | string | The workflow state of the temporary enrollment pairing. |
| ending\_enrollment\_state |  | string | The ending enrollment state to be given to each associated enrollment when the enrollment period has been reached. Defaults to âdeletedâ if no value is given. Accepted values are âdeletedâ, âcompletedâ, and âinactiveâ.  Allowed values: `deleted`, `completed`, `inactive` |

Returns a
[TemporaryEnrollmentPairing](temporary_enrollment_pairings.html#TemporaryEnrollmentPairing)
object

## [Delete Temporary Enrollment Pairing](#method.temporary_enrollment_pairings_api.destroy) [TemporaryEnrollmentPairingsApiController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/temporary_enrollment_pairings_api_controller.rb)

### DELETE /api/v1/accounts/:account\_id/temporary\_enrollment\_pairings/:id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/temporary_enrollment_pairings/:id`

Delete a temporary enrollment pairing

Returns a
[TemporaryEnrollmentPairing](temporary_enrollment_pairings.html#TemporaryEnrollmentPairing)
object