# Result

# Result API



Result API for
1EdTech (IMS) [Assignment and Grade Services](/doc/api/file.assignment_tools.html).

### A Result object looks like:

```
{
  // The fully qualified URL for showing the Result
  "id": "http://institution.canvas.com/api/lti/courses/5/line_items/2/results/1",
  // The lti_user_id or the Canvas user_id
  "userId": "50 | 'abcasdf'",
  // The score of the result as defined by Canvas, scaled to the resultMaximum
  "resultScore": 50,
  // Maximum possible score for this result; 1 is the default value and will be
  // assumed if not specified otherwise. Minimum value of 0 required.
  "resultMaximum": 50,
  // Comment visible to the student about the result.
  "comment": null,
  // URL of the line item this belongs to
  "scoreOf": "http://institution.canvas.com/api/lti/courses/5/line_items/2"
}
```

## [Show a collection of Results](#method.lti/ims/results.index) [Lti::Ims::ResultsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/ims/results_controller.rb)

### GET /api/lti/courses/:course\_id/line\_items/:line\_item\_id/results

**Scope:** 
`url:GET|/api/lti/courses/:course_id/line_items/:line_item_id/results`

Show existing Results of a line item. Can be used to retrieve a specific studentâs result by adding the user\_id (defined as the lti\_user\_id or the Canvas user\_id) as a query parameter (i.e. user\_id=1000). If user\_id is included, it will return only one Result in the collection if the result exists, otherwise it will be empty. May also limit number of results by adding the limit query param (i.e. limit=100)

Returns a
[Result](result.html#Result)
object

## [Show a Result](#method.lti/ims/results.show) [Lti::Ims::ResultsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/ims/results_controller.rb)

### GET /api/lti/courses/:course\_id/line\_items/:line\_item\_id/results/:id

**Scope:** 
`url:GET|/api/lti/courses/:course_id/line_items/:line_item_id/results/:id`

Show existing Result of a line item.

Returns a
[Result](result.html#Result)
object