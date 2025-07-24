# Rubrics

# Rubrics API



API for accessing rubric information.

### A Rubric object looks like:

```
{
  // the ID of the rubric
  "id": 1,
  // title of the rubric
  "title": "some title",
  // the context owning the rubric
  "context_id": 1,
  "context_type": "Course",
  "points_possible": 10.0,
  "reusable": false,
  "read_only": true,
  // whether or not free-form comments are used
  "free_form_criterion_comments": true,
  "hide_score_total": true,
  // An array with all of this Rubric's grading Criteria
  "data": null,
  // If an assessment type is included in the 'include' parameter, includes an
  // array of rubric assessment objects for a given rubric, based on the
  // assessment type requested. If the user does not request an assessment type
  // this key will be absent.
  "assessments": null,
  // If an association type is included in the 'include' parameter, includes an
  // array of rubric association objects for a given rubric, based on the
  // association type requested. If the user does not request an association type
  // this key will be absent.
  "associations": null
}
```

### A RubricCriterion object looks like:

```
{
  // the ID of the criterion
  "id": "_10",
  "description": null,
  "long_description": null,
  "points": 5,
  "criterion_use_range": false,
  // the possible ratings for this Criterion
  "ratings": null
}
```

### A RubricRating object looks like:

```
{
  "id": "name_2",
  "criterion_id": "_10",
  "description": null,
  "long_description": null,
  "points": 5
}
```

### A RubricAssessment object looks like:

```
{
  // the ID of the rubric
  "id": 1,
  // the rubric the assessment belongs to
  "rubric_id": 1,
  "rubric_association_id": 2,
  "score": 5.0,
  // the object of the assessment
  "artifact_type": "Submission",
  // the id of the object of the assessment
  "artifact_id": 3,
  // the current number of attempts made on the object of the assessment
  "artifact_attempt": 2,
  // the type of assessment. values will be either 'grading', 'peer_review', or
  // 'provisional_grade'
  "assessment_type": "grading",
  // user id of the person who made the assessment
  "assessor_id": 6,
  // (Optional) If 'full' is included in the 'style' parameter, returned
  // assessments will have their full details contained in their data hash. If the
  // user does not request a style, this key will be absent.
  "data": null,
  // (Optional) If 'comments_only' is included in the 'style' parameter, returned
  // assessments will include only the comments portion of their data hash. If the
  // user does not request a style, this key will be absent.
  "comments": null
}
```

### A RubricAssociation object looks like:

```
{
  // the ID of the association
  "id": 1,
  // the ID of the rubric
  "rubric_id": 1,
  // the ID of the object this association links to
  "association_id": 1,
  // the type of object this association links to
  "association_type": "Course",
  // Whether or not the associated rubric is used for grade calculation
  "use_for_grading": true,
  "summary_data": "",
  // Whether or not the association is for grading (and thus linked to an
  // assignment) or if it's to indicate the rubric should appear in its context.
  // Values will be grading or bookmark.
  "purpose": "grading",
  // Whether or not the score total is displayed within the rubric. This option is
  // only available if the rubric is not used for grading.
  "hide_score_total": true,
  "hide_points": true,
  "hide_outcome_results": true
}
```

## [Create a single rubric](#method.rubrics.create) [RubricsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_controller.rb)

### POST /api/v1/courses/:course\_id/rubrics

**Scope:** 
`url:POST|/api/v1/courses/:course_id/rubrics`

Returns the rubric with the given id.

Unfortuantely this endpoint does not return a standard Rubric object, instead it returns a hash that looks like

```
{ 'rubric': Rubric, 'rubric_association': RubricAssociation }

```

This may eventually be deprecated in favor of a more standardized return value, but that is not currently planned.

TODO: document once feature is public: [rubric](criteria_via_llm) [Boolean]

```
When true, rubric[criteria] will be ignored (does not need to be included
at all). Instead, rubric criteria will be automatically generated from a
large language model (llm).

```

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id |  | integer | The id of the rubric |
| rubric\_association\_id |  | integer | The id of the rubric association object (not the course/assignment itself, but the join table record id). It can be used in place of [rubric\_association](association_id) and [rubric\_association](association_type) if desired. |
| rubric[title] |  | string | The title of the rubric |
| rubric[free\_form\_criterion\_comments] |  | boolean | Whether or not you can write custom comments in the ratings field for a rubric |
| rubric\_association[association\_id] |  | integer | The id of the object with which this rubric is associated |
| rubric\_association[association\_type] |  | string | The type of object this rubric is associated with  Allowed values: `Assignment`, `Course`, `Account` |
| rubric\_association[use\_for\_grading] |  | boolean | Whether or not the associated rubric is used for grade calculation |
| rubric\_association[hide\_score\_total] |  | boolean | Whether or not the score total is displayed within the rubric. This option is only available if the rubric is not used for grading. |
| rubric\_association[purpose] |  | string | Whether or not the association is for grading (and thus linked to an assignment) or if itâs to indicate the rubric should appear in its context |
| rubric[criteria] |  | Hash | An indexed Hash of RubricCriteria objects where the keys are integer ids and the values are the RubricCriteria objects |

## [Update a single rubric](#method.rubrics.update) [RubricsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_controller.rb)

### PUT /api/v1/courses/:course\_id/rubrics/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/rubrics/:id`

Returns the rubric with the given id.

Unfortuantely this endpoint does not return a standard Rubric object, instead it returns a hash that looks like

```
{ 'rubric': Rubric, 'rubric_association': RubricAssociation }

```

This may eventually be deprecated in favor of a more standardized return value, but that is not currently planned.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id |  | integer | The id of the rubric |
| rubric\_association\_id |  | integer | The id of the rubric association object (not the course/assignment itself, but the join table record id). It can be used in place of [rubric\_association](association_id) and [rubric\_association](association_type) if desired. |
| rubric[title] |  | string | The title of the rubric |
| rubric[free\_form\_criterion\_comments] |  | boolean | Whether or not you can write custom comments in the ratings field for a rubric |
| rubric[skip\_updating\_points\_possible] |  | boolean | Whether or not to update the points possible |
| rubric\_association[association\_id] |  | integer | The id of the object with which this rubric is associated |
| rubric\_association[association\_type] |  | string | The type of object this rubric is associated with  Allowed values: `Assignment`, `Course`, `Account` |
| rubric\_association[use\_for\_grading] |  | boolean | Whether or not the associated rubric is used for grade calculation |
| rubric\_association[hide\_score\_total] |  | boolean | Whether or not the score total is displayed within the rubric. This option is only available if the rubric is not used for grading. |
| rubric\_association[purpose] |  | string | Whether or not the association is for grading (and thus linked to an assignment) or if itâs to indicate the rubric should appear in its context  Allowed values: `grading`, `bookmark` |
| rubric[criteria] |  | Hash | An indexed Hash of RubricCriteria objects where the keys are integer ids and the values are the RubricCriteria objects |

## [Delete a single](#method.rubrics.destroy) [RubricsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_controller.rb)

### DELETE /api/v1/courses/:course\_id/rubrics/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/rubrics/:id`

Deletes a Rubric and removes all RubricAssociations.

Returns a
[Rubric](rubrics.html#Rubric)
object

## [List rubrics](#method.rubrics_api.index) [RubricsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### GET /api/v1/accounts/:account\_id/rubrics

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/rubrics`

### GET /api/v1/courses/:course\_id/rubrics

**Scope:** 
`url:GET|/api/v1/courses/:course_id/rubrics`

Returns the paginated list of active rubrics for the current context.

## [Get a single rubric](#method.rubrics_api.show) [RubricsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### GET /api/v1/accounts/:account\_id/rubrics/:id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/rubrics/:id`

### GET /api/v1/courses/:course\_id/rubrics/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/rubrics/:id`

Returns the rubric with the given id.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Related records to include in the response.  Allowed values: `assessments`, `graded_assessments`, `peer_assessments`, `associations`, `assignment_associations`, `course_associations`, `account_associations` |
| style |  | string | Applicable only if assessments are being returned. If included, returns either all criteria data associated with the assessment, or just the comments. If not included, both data and comments are omitted.  Allowed values: `full`, `comments_only` |

Returns a
[Rubric](rubrics.html#Rubric)
object

## [Get the courses and assignments for](#method.rubrics_api.used_locations) [RubricsApiController#used\_locations](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### GET /api/v1/courses/:course\_id/rubrics/:id/used\_locations

**Scope:** 
`url:GET|/api/v1/courses/:course_id/rubrics/:id/used_locations`

### GET /api/v1/accounts/:account\_id/rubrics/:id/used\_locations

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/rubrics/:id/used_locations`

Returns the rubric with the given id.

## [Creates a rubric using a CSV file](#method.rubrics_api.upload) [RubricsApiController#upload](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### POST /api/v1/courses/:course\_id/rubrics/upload

**Scope:** 
`url:POST|/api/v1/courses/:course_id/rubrics/upload`

### POST /api/v1/accounts/:account\_id/rubrics/upload

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/rubrics/upload`

Returns the rubric import object that was created

## [Templated file for importing a rubric](#method.rubrics_api.upload_template) [RubricsApiController#upload\_template](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### GET /api/v1/rubrics/upload\_template

**Scope:** 
`url:GET|/api/v1/rubrics/upload_template`

## [Get the status of a rubric import](#method.rubrics_api.upload_status) [RubricsApiController#upload\_status](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubrics_api_controller.rb)

### GET /api/v1/courses/:course\_id/rubrics/upload/:id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/rubrics/upload/:id`

### GET /api/v1/accounts/:account\_id/rubrics/upload/:id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/rubrics/upload/:id`

Can return the latest rubric import for an account or course, or a specific import by id

## [Create a single rubric assessment](#method.rubric_assessments.create) [RubricAssessmentsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_assessments_controller.rb)

### POST /api/v1/courses/:course\_id/rubric\_associations/:rubric\_association\_id/rubric\_assessments

**Scope:** 
`url:POST|/api/v1/courses/:course_id/rubric_associations/:rubric_association_id/rubric_assessments`

Returns the rubric assessment with the given id. The returned object also provides the information of

```
:ratings, :assessor_name, :related_group_submissions_and_assessments, :artifact

```

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| course\_id |  | integer | The id of the course |
| rubric\_association\_id |  | integer | The id of the object with which this rubric assessment is associated |
| provisional |  | string | (optional) Indicates whether this assessment is provisional, defaults to false. |
| final |  | string | (optional) Indicates a provisional grade will be marked as final. It only takes effect if the provisional param is passed as true. Defaults to false. |
| graded\_anonymously |  | boolean | (optional) Defaults to false |
| rubric\_assessment |  | Hash | A Hash of data to complement the rubric assessment: The user id that refers to the person being assessed   ``` rubric_assessment[user_id]  ```   Assessment type. There are only three valid types: âgradingâ, âpeer\_reviewâ, or âprovisional\_gradeâ   ``` rubric_assessment[assessment_type]  ```   The points awarded for this row.   ``` rubric_assessment[criterion_id][points]  ```   Comments to add for this row.   ``` rubric_assessment[criterion_id][comments]  ```   For each criterion\_id, change the id by the criterion number, ex: criterion\_123 If the criterion\_id is not specified it defaults to false, and nothing is updated. |

## [Update a single rubric assessment](#method.rubric_assessments.update) [RubricAssessmentsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_assessments_controller.rb)

### PUT /api/v1/courses/:course\_id/rubric\_associations/:rubric\_association\_id/rubric\_assessments/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/rubric_associations/:rubric_association_id/rubric_assessments/:id`

Returns the rubric assessment with the given id. The returned object also provides the information of

```
:ratings, :assessor_name, :related_group_submissions_and_assessments, :artifact

```

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id |  | integer | The id of the rubric assessment |
| course\_id |  | integer | The id of the course |
| rubric\_association\_id |  | integer | The id of the object with which this rubric assessment is associated |
| provisional |  | string | (optional) Indicates whether this assessment is provisional, defaults to false. |
| final |  | string | (optional) Indicates a provisional grade will be marked as final. It only takes effect if the provisional param is passed as true. Defaults to false. |
| graded\_anonymously |  | boolean | (optional) Defaults to false |
| rubric\_assessment |  | Hash | A Hash of data to complement the rubric assessment: The user id that refers to the person being assessed   ``` rubric_assessment[user_id]  ```   Assessment type. There are only three valid types: âgradingâ, âpeer\_reviewâ, or âprovisional\_gradeâ   ``` rubric_assessment[assessment_type]  ```   The points awarded for this row.   ``` rubric_assessment[criterion_id][points]  ```   Comments to add for this row.   ``` rubric_assessment[criterion_id][comments]  ```   For each criterion\_id, change the id by the criterion number, ex: criterion\_123 If the criterion\_id is not specified it defaults to false, and nothing is updated. |

## [Delete a single rubric assessment](#method.rubric_assessments.destroy) [RubricAssessmentsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_assessments_controller.rb)

### DELETE /api/v1/courses/:course\_id/rubric\_associations/:rubric\_association\_id/rubric\_assessments/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/rubric_associations/:rubric_association_id/rubric_assessments/:id`

Deletes a rubric assessment

Returns a
[RubricAssessment](rubrics.html#RubricAssessment)
object

## [Create a RubricAssociation](#method.rubric_associations.create) [RubricAssociationsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_associations_controller.rb)

### POST /api/v1/courses/:course\_id/rubric\_associations

**Scope:** 
`url:POST|/api/v1/courses/:course_id/rubric_associations`

Returns the rubric with the given id.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| rubric\_association[rubric\_id] |  | integer | The id of the Rubric |
| rubric\_association[association\_id] |  | integer | The id of the object with which this rubric is associated |
| rubric\_association[association\_type] |  | string | The type of object this rubric is associated with  Allowed values: `Assignment`, `Course`, `Account` |
| rubric\_association[title] |  | string | The name of the object this rubric is associated with |
| rubric\_association[use\_for\_grading] |  | boolean | Whether or not the associated rubric is used for grade calculation |
| rubric\_association[hide\_score\_total] |  | boolean | Whether or not the score total is displayed within the rubric. This option is only available if the rubric is not used for grading. |
| rubric\_association[purpose] |  | string | Whether or not the association is for grading (and thus linked to an assignment) or if itâs to indicate the rubric should appear in its context  Allowed values: `grading`, `bookmark` |
| rubric\_association[bookmarked] |  | boolean | Whether or not the associated rubric appears in its context |

Returns a
[RubricAssociation](rubrics.html#RubricAssociation)
object

## [Update a RubricAssociation](#method.rubric_associations.update) [RubricAssociationsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_associations_controller.rb)

### PUT /api/v1/courses/:course\_id/rubric\_associations/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/rubric_associations/:id`

Returns the rubric with the given id.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id |  | integer | The id of the RubricAssociation to update |
| rubric\_association[rubric\_id] |  | integer | The id of the Rubric |
| rubric\_association[association\_id] |  | integer | The id of the object with which this rubric is associated |
| rubric\_association[association\_type] |  | string | The type of object this rubric is associated with  Allowed values: `Assignment`, `Course`, `Account` |
| rubric\_association[title] |  | string | The name of the object this rubric is associated with |
| rubric\_association[use\_for\_grading] |  | boolean | Whether or not the associated rubric is used for grade calculation |
| rubric\_association[hide\_score\_total] |  | boolean | Whether or not the score total is displayed within the rubric. This option is only available if the rubric is not used for grading. |
| rubric\_association[purpose] |  | string | Whether or not the association is for grading (and thus linked to an assignment) or if itâs to indicate the rubric should appear in its context  Allowed values: `grading`, `bookmark` |
| rubric\_association[bookmarked] |  | boolean | Whether or not the associated rubric appears in its context |

Returns a
[RubricAssociation](rubrics.html#RubricAssociation)
object

## [Delete a RubricAssociation](#method.rubric_associations.destroy) [RubricAssociationsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/rubric_associations_controller.rb)

### DELETE /api/v1/courses/:course\_id/rubric\_associations/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/rubric_associations/:id`

Delete the RubricAssociation with the given ID

Returns a
[RubricAssociation](rubrics.html#RubricAssociation)
object