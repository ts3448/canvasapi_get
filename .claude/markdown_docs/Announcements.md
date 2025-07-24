# Announcements

# Announcements API



API for retrieving announcements. This API is Announcement-specific.
See also the Discussion Topics API, which operates on Announcements also.

## [List announcements](#method.announcements_api.index) [AnnouncementsApiController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/announcements_api_controller.rb)

### GET /api/v1/announcements

**Scope:** 
`url:GET|/api/v1/announcements`

Returns the paginated list of announcements for the given courses and date range. Note that a `context_code` field is added to the responses so you can tell which course each announcement belongs to.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| context\_codes[] | Required | string | List of context\_codes to retrieve announcements for (for example, `course_123`). Only courses are presently supported. The call will fail unless the caller has View Announcements permission in all listed courses. |
| start\_date |  | Date | Only return announcements posted since the start\_date (inclusive). Defaults to 14 days ago. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. |
| end\_date |  | Date | Only return announcements posted before the end\_date (inclusive). Defaults to 28 days from start\_date. The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. Announcements scheduled for future posting will only be returned to course administrators. |
| available\_after |  | Date | Only return announcements having locked\_at nil or after available\_after (exclusive). The value should be formatted as: yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ. Effective only for students (who donât have moderate forum right). |
| active\_only |  | boolean | Only return active announcements that have been published. Applies only to requesting users that have permission to view unpublished items. Defaults to false for users with access to view unpublished items, otherwise true and unmodifiable. |
| latest\_only |  | boolean | Only return the latest announcement for each associated context. The response will include at most one announcement for each specified context in the context\_codes[] parameter. Defaults to false. |
| include |  | array | Optional list of resources to include with the response. May include a string of the name of the resource. Possible values are: âsectionsâ, âsections\_user\_countâ if âsectionsâ is passed, includes the course sections that are associated with the topic, if the topic is specific to certain sections of the course. If âsections\_user\_countâ is passed, then:   ``` (a) If sections were asked for *and* the topic is specific to certain     course sections sections, includes the number of users in each     section. (as part of the section json asked for above) (b) Else, includes at the root level the total number of users in the     topic's context (group or course) that the topic applies to.  ``` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/announcements?context_codes[]=course_1&context_codes[]=course_2 \
     -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
[{
  "id": 1,
  "title": "Hear ye",
  "message": "Henceforth, all assignments must be...",
  "posted_at": "2017-01-31T22:00:00Z",
  "delayed_post_at": null,
  "context_code": "course_2",
  ...
}]
```

Returns a list of
[DiscussionTopic](discussion_topics.html#DiscussionTopic)
objects