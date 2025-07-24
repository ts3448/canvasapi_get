# Quiz IP Filters

# Quiz IP Filters API



API for accessing quiz IP filters

### A QuizIPFilter object looks like:

```
{
  // A unique name for the filter.
  "name": "Current Filter",
  // Name of the Account (or Quiz) the IP filter is defined in.
  "account": "Some Quiz",
  // An IP address (or range mask) this filter embodies.
  "filter": "192.168.1.1/24"
}
```

## [Get available quiz IP filters.](#method.quizzes/quiz_ip_filters.index) [Quizzes::QuizIpFiltersController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/quizzes/quiz_ip_filters_controller.rb)

### GET /api/v1/courses/:course\_id/quizzes/:quiz\_id/ip\_filters

**Scope:** 
`url:GET|/api/v1/courses/:course_id/quizzes/:quiz_id/ip_filters`

Get a list of available IP filters for this Quiz.

**200 OK** response code is returned if the request was successful.

#### Example Response:

#### 

```
{
  "quiz_ip_filters": [QuizIPFilter]
}
```