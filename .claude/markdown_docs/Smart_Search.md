# Smart Search

# Smart Search API

### BETA: This API resource is not finalized, and there could be breaking changes before its final release.



API for AI-powered course content search. NOTE: This feature has limited availability at present.

### A SearchResult object looks like:

```
// Reference to an object that matches a smart search
{
  // The ID of the matching object.
  "content_id": 2,
  // The type of the matching object.
  "content_type": "WikiPage",
  // The title of the matching object.
  "title": "Nicolaus Copernicus",
  // The body of the matching object.
  "body": "Nicolaus Copernicus was a Renaissance-era mathematician and astronomer who...",
  // The Canvas URL of the matching object.
  "html_url": "https://canvas.example.com/courses/123/pages/nicolaus-copernicus",
  // The distance between the search query and the result. Smaller numbers
  // indicate closer matches.
  "distance": 0.212
}
```

## [Search course content](#method.smart_search.search) [SmartSearchController#search](https://github.com/instructure/canvas-lms/blob/master/app/controllers/smart_search_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/courses/:course\_id/smartsearch

**Scope:** 
`url:GET|/api/v1/courses/:course_id/smartsearch`

Find course content using a meaning-based search

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| q | Required | string | The search query |
| filter[] |  | string | Types of objects to search. By default, all supported types are searched. Supported types include `pages`, `assignments`, `announcements`, and `discussion_topics`. |
| include[] |  | string | Optional information to include with each search result:  modules  An array of module objects that the search result belongs to.  status  The published status for all results and the due\_date for all assignments.  Allowed values: `status`, `modules` |

Returns a list of
[SearchResult](smart_search.html#SearchResult)
objects