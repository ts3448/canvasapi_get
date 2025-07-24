# Announcement External Feeds

# Announcement External Feeds API



External feeds represent RSS feeds that can be attached to a Course or Group,
in order to automatically create announcements for each new item in
the feed.

### An ExternalFeed object looks like:

```
{
  // The ID of the feed
  "id": 5,
  // The title of the feed, pulled from the feed itself. If the feed hasn't yet
  // been pulled, a temporary name will be synthesized based on the URL
  "display_name": "My Blog",
  // The HTTP/HTTPS URL to the feed
  "url": "http://example.com/myblog.rss",
  // If not null, only feed entries whose title contains this string will trigger
  // new posts in Canvas
  "header_match": "pattern",
  // When this external feed was added to Canvas
  "created_at": "2012-06-01T00:00:00-06:00",
  // The verbosity setting determines how much of the feed's content is imported
  // into Canvas as part of the posting. 'link_only' means that only the title and
  // a link to the item. 'truncate' means that a summary of the first portion of
  // the item body will be used. 'full' means that the full item body will be
  // used.
  "verbosity": "truncate"
}
```

## [List external feeds](#method.external_feeds.index) [ExternalFeedsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/external_feeds_controller.rb)

### GET /api/v1/courses/:course\_id/external\_feeds

**Scope:** 
`url:GET|/api/v1/courses/:course_id/external_feeds`

### GET /api/v1/groups/:group\_id/external\_feeds

**Scope:** 
`url:GET|/api/v1/groups/:group_id/external_feeds`

Returns the paginated list of External Feeds this course or group.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/external_feeds \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[ExternalFeed](announcement_external_feeds.html#ExternalFeed)
objects

## [Create an external feed](#method.external_feeds.create) [ExternalFeedsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/external_feeds_controller.rb)

### POST /api/v1/courses/:course\_id/external\_feeds

**Scope:** 
`url:POST|/api/v1/courses/:course_id/external_feeds`

### POST /api/v1/groups/:group\_id/external\_feeds

**Scope:** 
`url:POST|/api/v1/groups/:group_id/external_feeds`

Create a new external feed for the course or group.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| url | Required | string | The url to the external rss or atom feed |
| header\_match |  | boolean | If given, only feed entries that contain this string in their title will be imported |
| verbosity |  | string | Defaults to âfullâ  Allowed values: `full`, `truncate`, `link_only` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/external_feeds \
    -F url='http://example.com/rss.xml' \
    -F header_match='news flash!' \
    -F verbosity='full' \
    -H 'Authorization: Bearer <token>'
```

Returns an
[ExternalFeed](announcement_external_feeds.html#ExternalFeed)
object

## [Delete an external feed](#method.external_feeds.destroy) [ExternalFeedsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/external_feeds_controller.rb)

### DELETE /api/v1/courses/:course\_id/external\_feeds/:external\_feed\_id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/external_feeds/:external_feed_id`

### DELETE /api/v1/groups/:group\_id/external\_feeds/:external\_feed\_id

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/external_feeds/:external_feed_id`

Deletes the external feed.

#### Example Request:

#### 

```
curl -X DELETE https://<canvas>/api/v1/courses/<course_id>/external_feeds/<feed_id> \
     -H 'Authorization: Bearer <token>'
```

Returns an
[ExternalFeed](announcement_external_feeds.html#ExternalFeed)
object