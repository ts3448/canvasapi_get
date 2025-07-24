# LiveAssessments

# LiveAssessments API



Manage live assessment results

Manage live assessments

### A Result object looks like:

```
// A pass/fail results for a student
{
  // A unique identifier for this result
  "id": "42",
  // Whether the user passed or not
  "passed": true,
  // When this result was recorded
  "assessed_at": "2014-05-13T00:01:57-06:00",
  // Unique identifiers of objects associated with this result
  "links": {"user":"42","assessor":"23","assessment":"5"}
}
```

### A ResultLinks object looks like:

```
// Unique identifiers of objects associated with a result
{
  // A unique identifier for the user to whom this result applies
  "user": "42",
  // A unique identifier for the user who created this result
  "assessor": "23",
  // A unique identifier for the assessment that this result is for
  "assessment": "5"
}
```

### An Assessment object looks like:

```
// A simple assessment that collects pass/fail results for a student
{
  // A unique identifier for this live assessment
  "id": "42",
  // A client specified unique identifier for the assessment
  "key": "2014-05-27,outcome_52",
  // A human readable title for the assessment
  "title": "May 27th Reading Assessment"
}
```

## [Create live assessment results](#method.live_assessments/results.create) [LiveAssessments::ResultsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/live_assessments/results_controller.rb)

### POST /api/v1/courses/:course\_id/live\_assessments/:assessment\_id/results

**Scope:** 
`url:POST|/api/v1/courses/:course_id/live_assessments/:assessment_id/results`

Creates live assessment results and adds them to a live assessment

#### Example Request:

#### 

```
{
  "results": [{
    "passed": false,
    "assessed_at": "2014-05-26T14:57:23-07:00",
    "links": {
      "user": "15"
    }
  },{
    "passed": true,
    "assessed_at": "2014-05-26T13:05:40-07:00",
    "links": {
      "user": "16"
    }
  }]
}
```

#### Example Response:

#### 

```
{
  "results": [Result]
}
```

## [List live assessment results](#method.live_assessments/results.index) [LiveAssessments::ResultsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/live_assessments/results_controller.rb)

### GET /api/v1/courses/:course\_id/live\_assessments/:assessment\_id/results

**Scope:** 
`url:GET|/api/v1/courses/:course_id/live_assessments/:assessment_id/results`

Returns a paginated list of live assessment results

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| user\_id |  | integer | If set, restrict results to those for this user |

#### Example Response:

#### 

```
{
  "results": [Result]
}
```

## [Create or find a live assessment](#method.live_assessments/assessments.create) [LiveAssessments::AssessmentsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/live_assessments/assessments_controller.rb)

### POST /api/v1/courses/:course\_id/live\_assessments

**Scope:** 
`url:POST|/api/v1/courses/:course_id/live_assessments`

Creates or finds an existing live assessment with the given key and aligns it with the linked outcome

#### Example Request:

#### 

```
{
  "assessments": [{
    "key": "2014-05-27-Outcome-52",
    "title": "Tuesday's LiveAssessment",
    "links": {
      "outcome": "1"
    }
  }]
}
```

#### Example Response:

#### 

```
{
  "links": {
    "assessments.results": "http://example.com/courses/1/live_assessments/5/results"
  },
  "assessments": [Assessment]
}
```

## [List live assessments](#method.live_assessments/assessments.index) [LiveAssessments::AssessmentsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/live_assessments/assessments_controller.rb)

### GET /api/v1/courses/:course\_id/live\_assessments

**Scope:** 
`url:GET|/api/v1/courses/:course_id/live_assessments`

Returns a paginated list of live assessments.

#### Example Response:

#### 

```
{
  "links": {
    "assessments.results": "http://example.com/courses/1/live_assessments/{assessments.id}/results"
  },
  "assessments": [Assessment]
}
```