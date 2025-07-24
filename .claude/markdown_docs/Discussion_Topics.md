# Discussion Topics

# Discussion Topics API



API for accessing and participating in discussion topics in groups and courses.

### A FileAttachment object looks like:

```
// A file attachment
{
  "content-type": "unknown/unknown",
  "url": "http://www.example.com/courses/1/files/1/download",
  "filename": "content.txt",
  "display_name": "content.txt"
}
```

### A DiscussionTopic object looks like:

```
// A discussion topic
{
  // The ID of this topic.
  "id": 1,
  // The topic title.
  "title": "Topic 1",
  // The HTML content of the message body.
  "message": "<p>content here</p>",
  // The URL to the discussion topic in canvas.
  "html_url": "https://<canvas>/courses/1/discussion_topics/2",
  // The datetime the topic was posted. If it is null it hasn't been posted yet.
  // (see delayed_post_at)
  "posted_at": "2037-07-21T13:29:31Z",
  // The datetime for when the last reply was in the topic.
  "last_reply_at": "2037-07-28T19:38:31Z",
  // If true then a user may not respond to other replies until that user has made
  // an initial reply. Defaults to false.
  "require_initial_post": false,
  // Whether or not posts in this topic are visible to the user.
  "user_can_see_posts": true,
  // The count of entries in the topic.
  "discussion_subentry_count": 0,
  // The read_state of the topic for the current user, 'read' or 'unread'.
  "read_state": "read",
  // The count of unread entries of this topic for the current user.
  "unread_count": 0,
  // Whether or not the current user is subscribed to this topic.
  "subscribed": true,
  // (Optional) Why the user cannot subscribe to this topic. Only one reason will
  // be returned even if multiple apply. Can be one of: 'initial_post_required':
  // The user must post a reply first; 'not_in_group_set': The user is not in the
  // group set for this graded group discussion; 'not_in_group': The user is not
  // in this topic's group; 'topic_is_announcement': This topic is an announcement
  "subscription_hold": "not_in_group_set",
  // The unique identifier of the assignment if the topic is for grading,
  // otherwise null.
  "assignment_id": null,
  // The datetime to publish the topic (if not right away).
  "delayed_post_at": null,
  // Whether this discussion topic is published (true) or draft state (false)
  "published": true,
  // The datetime to lock the topic (if ever).
  "lock_at": null,
  // Whether or not the discussion is 'closed for comments'.
  "locked": false,
  // Whether or not the discussion has been 'pinned' by an instructor
  "pinned": false,
  // Whether or not this is locked for the user.
  "locked_for_user": true,
  // (Optional) Information for the user about the lock. Present when
  // locked_for_user is true.
  "lock_info": null,
  // (Optional) An explanation of why this is locked for the user. Present when
  // locked_for_user is true.
  "lock_explanation": "This discussion is locked until September 1 at 12:00am",
  // The username of the topic creator.
  "user_name": "User Name",
  // DEPRECATED An array of topic_ids for the group discussions the user is a part
  // of.
  "topic_children": [5, 7, 10],
  // An array of group discussions the user is a part of. Fields include: id,
  // group_id
  "group_topic_children": [{"id":5,"group_id":1}, {"id":7,"group_id":5}, {"id":10,"group_id":4}],
  // If the topic is for grading and a group assignment this will point to the
  // original topic in the course.
  "root_topic_id": null,
  // If the topic is a podcast topic this is the feed url for the current user.
  "podcast_url": "/feeds/topics/1/enrollment_1XAcepje4u228rt4mi7Z1oFbRpn3RAkTzuXIGOPe.rss",
  // The type of discussion. Values are 'side_comment' or 'not_threaded', for
  // discussions that only allow one level of nested comments, and 'threaded' for
  // fully threaded discussions.
  "discussion_type": "side_comment",
  // The unique identifier of the group category if the topic is a group
  // discussion, otherwise null.
  "group_category_id": null,
  // Array of file attachments.
  "attachments": null,
  // The current user's permissions on this topic.
  "permissions": {"attach":true},
  // Whether or not users can rate entries in this topic.
  "allow_rating": true,
  // Whether or not grade permissions are required to rate entries.
  "only_graders_can_rate": true,
  // DEPRECATED, Whether or not entries should be sorted by rating.
  "sort_by_rating": true,
  // How entries should be sorted by default.
  "sort_order": "asc",
  // Can users decide their preferred sort order.
  "sort_order_locked": true,
  // Threaded replies should be expanded by default.
  "expand": true,
  // Can users decide their preferred thread expand setting.
  "expand_locked": true
}
```

## [List discussion topics](#method.discussion_topics.index) [DiscussionTopicsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics`

### GET /api/v1/groups/:group\_id/discussion\_topics

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics`

Returns the paginated list of discussion topics for this course or group.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | If âall\_datesâ is passed, all dates associated with graded discussionsâ assignments will be included. if âsectionsâ is passed, includes the course sections that are associated with the topic, if the topic is specific to certain sections of the course. If âsections\_user\_countâ is passed, then:   ``` (a) If sections were asked for *and* the topic is specific to certain     course sections, includes the number of users in each     section. (as part of the section json asked for above) (b) Else, includes at the root level the total number of users in the     topic's context (group or course) that the topic applies to.  ```   If âoverridesâ is passed, the overrides for the assignment will be included  Allowed values: `all_dates`, `sections`, `sections_user_count`, `overrides` |
| order\_by |  | string | Determines the order of the discussion topic list. Defaults to âpositionâ.  Allowed values: `position`, `recent_activity`, `title` |
| scope |  | string | Only return discussion topics in the given state(s). Defaults to including all topics. Filtering is done after pagination, so pages may be smaller than requested if topics are filtered. Can pass multiple states as comma separated string.  Allowed values: `locked`, `unlocked`, `pinned`, `unpinned` |
| only\_announcements |  | boolean | Return announcements instead of discussion topics. Defaults to false |
| filter\_by |  | string | The state of the discussion topic to return. Currently only supports unread state.  Allowed values: `all`, `unread` |
| search\_term |  | string | The partial title of the discussion topics to match and return. |
| exclude\_context\_module\_locked\_topics |  | boolean | For students, exclude topics that are locked by module progression. Defaults to false. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[DiscussionTopic](discussion_topics.html#DiscussionTopic)
objects

## [Create a new discussion topic](#method.discussion_topics.create) [DiscussionTopicsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics`

### POST /api/v1/groups/:group\_id/discussion\_topics

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics`

Create an new discussion topic for the course or group.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| title |  | string | no description |
| message |  | string | no description |
| discussion\_type |  | string | The type of discussion. Defaults to side\_comment or not\_threaded if not value is given. Accepted values are âside\_commentâ, ânot\_threadedâ for discussions that only allow one level of nested comments, and âthreadedâ for fully threaded discussions.  Allowed values: `side_comment`, `threaded`, `not_threaded` |
| published |  | boolean | Whether this topic is published (true) or draft state (false). Only teachers and TAs have the ability to create draft state topics. |
| delayed\_post\_at |  | DateTime | If a timestamp is given, the topic will not be published until that time. |
| allow\_rating |  | boolean | Whether or not users can rate entries in this topic. |
| lock\_at |  | DateTime | If a timestamp is given, the topic will be scheduled to lock at the provided timestamp. If the timestamp is in the past, the topic will be locked. |
| podcast\_enabled |  | boolean | If true, the topic will have an associated podcast feed. |
| podcast\_has\_student\_posts |  | boolean | If true, the podcast will include posts from students as well. Implies podcast\_enabled. |
| require\_initial\_post |  | boolean | If true then a user may not respond to other replies until that user has made an initial reply. Defaults to false. |
| assignment |  | Assignment | To create an assignment discussion, pass the assignment parameters as a sub-object. See the [Create an Assignment API](assignments.html#method.assignments_api.create "Create an Assignment API") for the available parameters. The name parameter will be ignored, as itâs taken from the discussion title. If you want to make a discussion that was an assignment NOT an assignment, pass set\_assignment = false as part of the assignment object |
| is\_announcement |  | boolean | If true, this topic is an announcement. It will appear in the announcementâs section rather than the discussions section. This requires announcment-posting permissions. |
| pinned |  | boolean | If true, this topic will be listed in the âPinned Discussionâ section |
| position\_after |  | string | By default, discussions are sorted chronologically by creation date, you can pass the id of another topic to have this one show up after the other when they are listed. |
| group\_category\_id |  | integer | If present, the topic will become a group discussion assigned to the group. |
| only\_graders\_can\_rate |  | boolean | If true, only graders will be allowed to rate entries. |
| sort\_order |  | string | Default sort order of the discussion. Accepted values are âascâ, âdescâ.  Allowed values: `asc`, `desc` |
| sort\_order\_locked |  | boolean | If true, users cannot choose their prefered sort order |
| expanded |  | boolean | If true, thread will be expanded by default |
| expanded\_locked |  | boolean | If true, users cannot choose their prefered thread expansion setting |
| sort\_by\_rating |  | boolean | (DEPRECATED) If true, entries will be sorted by rating. |
| attachment |  | File | A multipart/form-data form-field-style attachment. Attachments larger than 1 kilobyte are subject to quota restrictions. |
| specific\_sections |  | string | A comma-separated list of sections ids to which the discussion topic should be made specific to. If it is not desired to make the discussion topic specific to sections, then this parameter may be omitted or set to âallâ. Can only be present only on announcements and only those that are for a course (as opposed to a group). |
| lock\_comment |  | boolean | If is\_announcement and lock\_comment are true, âAllow Participants to Commentâ setting is disabled. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics \
    -F title='my topic' \
    -F message='initial message' \
    -F podcast_enabled=1 \
    -H 'Authorization: Bearer <token>'
    -F 'attachment=@<filename>' \
```

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics \
    -F title='my assignment topic' \
    -F message='initial message' \
    -F assignment[points_possible]=15 \
    -H 'Authorization: Bearer <token>'
```

## [Update a topic](#method.discussion_topics.update) [DiscussionTopicsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id`

Update an existing discussion topic for the course or group.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| title |  | string | no description |
| message |  | string | no description |
| discussion\_type |  | string | The type of discussion. Defaults to side\_comment or not\_threaded if not value is given. Accepted values are âside\_commentâ, ânot\_threadedâ for discussions that only allow one level of nested comments, and âthreadedâ for fully threaded discussions.  Allowed values: `side_comment`, `threaded`, `not_threaded` |
| published |  | boolean | Whether this topic is published (true) or draft state (false). Only teachers and TAs have the ability to create draft state topics. |
| delayed\_post\_at |  | DateTime | If a timestamp is given, the topic will not be published until that time. |
| lock\_at |  | DateTime | If a timestamp is given, the topic will be scheduled to lock at the provided timestamp. If the timestamp is in the past, the topic will be locked. |
| podcast\_enabled |  | boolean | If true, the topic will have an associated podcast feed. |
| podcast\_has\_student\_posts |  | boolean | If true, the podcast will include posts from students as well. Implies podcast\_enabled. |
| require\_initial\_post |  | boolean | If true then a user may not respond to other replies until that user has made an initial reply. Defaults to false. |
| assignment |  | Assignment | To create an assignment discussion, pass the assignment parameters as a sub-object. See the [Create an Assignment API](assignments.html#method.assignments_api.create "Create an Assignment API") for the available parameters. The name parameter will be ignored, as itâs taken from the discussion title. If you want to make a discussion that was an assignment NOT an assignment, pass set\_assignment = false as part of the assignment object |
| is\_announcement |  | boolean | If true, this topic is an announcement. It will appear in the announcementâs section rather than the discussions section. This requires announcment-posting permissions. |
| pinned |  | boolean | If true, this topic will be listed in the âPinned Discussionâ section |
| position\_after |  | string | By default, discussions are sorted chronologically by creation date, you can pass the id of another topic to have this one show up after the other when they are listed. |
| group\_category\_id |  | integer | If present, the topic will become a group discussion assigned to the group. |
| allow\_rating |  | boolean | If true, users will be allowed to rate entries. |
| only\_graders\_can\_rate |  | boolean | If true, only graders will be allowed to rate entries. |
| sort\_order |  | string | Default sort order of the discussion. Accepted values are âascâ, âdescâ.  Allowed values: `asc`, `desc` |
| sort\_order\_locked |  | boolean | If true, users cannot choose their prefered sort order |
| expanded |  | boolean | If true, thread will be expanded by default |
| expanded\_locked |  | boolean | If true, users cannot choose their prefered thread expansion setting |
| sort\_by\_rating |  | boolean | (DEPRECATED) If true, entries will be sorted by rating. |
| specific\_sections |  | string | A comma-separated list of sections ids to which the discussion topic should be made specific too. If it is not desired to make the discussion topic specific to sections, then this parameter may be omitted or set to âallâ. Can only be present only on announcements and only those that are for a course (as opposed to a group). |
| lock\_comment |  | boolean | If is\_announcement and lock\_comment are true, âAllow Participants to Commentâ setting is disabled. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id> \
    -F title='This will be positioned after Topic #1234' \
    -F position_after=1234 \
    -H 'Authorization: Bearer <token>'
```

## [Delete a topic](#method.discussion_topics.destroy) [DiscussionTopicsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id`

Deletes the discussion topic. This will also delete the assignment, if itâs an assignment discussion.

#### Example Request:

#### 

```
curl -X DELETE https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id> \
     -H 'Authorization: Bearer <token>'
```

## [Reorder pinned topics](#method.discussion_topics.reorder) [DiscussionTopicsController#reorder](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/reorder

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/reorder`

### POST /api/v1/groups/:group\_id/discussion\_topics/reorder

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/reorder`

Puts the pinned discussion topics in the specified order. All pinned topics should be included.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| order[] | Required | integer | The ids of the pinned discussion topics in the desired order. (For example, âorder=104,102,103â.) |

## [Update an entry](#method.discussion_entries.update) [DiscussionEntriesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_entries_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:id

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:id

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id`

Update an existing discussion entry.

The entry must have been created by the current user, or the current user must have admin rights to the discussion. If the edit is not allowed, a 401 will be returned.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| message |  | string | The updated body of the entry. |

#### Example Request:

#### 

```
curl -X PUT 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>' \
     -F 'message=<message>' \
     -H "Authorization: Bearer <token>"
```

## [Delete an entry](#method.discussion_entries.destroy) [DiscussionEntriesController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_entries_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:id

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:id

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id`

Delete a discussion entry.

The entry must have been created by the current user, or the current user must have admin rights to the discussion. If the delete is not allowed, a 401 will be returned.

The discussion will be marked deleted, and the user\_id and message will be cleared out.

#### Example Request:

#### 

```
curl -X DELETE 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>' \
     -H "Authorization: Bearer <token>"
```

## [Get a single topic](#method.discussion_topics_api.show) [DiscussionTopicsApiController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id`

Returns data on an individual discussion topic. See the List action for the response formatting.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | If âall\_datesâ is passed, all dates associated with graded discussionsâ assignments will be included. if âsectionsâ is passed, includes the course sections that are associated with the topic, if the topic is specific to certain sections of the course. If âsections\_user\_countâ is passed, then:   ``` (a) If sections were asked for *and* the topic is specific to certain     course sections, includes the number of users in each     section. (as part of the section json asked for above) (b) Else, includes at the root level the total number of users in the     topic's context (group or course) that the topic applies to.  ```   If âoverridesâ is passed, the overrides for the assignment will be included  Allowed values: `all_dates`, `sections`, `sections_user_count`, `overrides` |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id> \
    -H 'Authorization: Bearer <token>'
```

## [Find Last Summary](#method.discussion_topics_api.find_summary) [DiscussionTopicsApiController#find\_summary](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/summaries

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id/summaries`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/summaries

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id/summaries`

Returns: (1) last userInput (what current user had keyed in to produce the last discussion summary), (2) last discussion summary generated by the current user for current discussion topic, based on userInput, (3) and some usage information.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/summaries \
    -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{
  "id": 1,
  "userInput": "Give me a brief summary of the discussion.",
  "text": "This is a summary of the discussion topic.",
  "usage": { "currentCount": 1, "limit": 5 }
}
```

## [Find or Create Summary](#method.discussion_topics_api.find_or_create_summary) [DiscussionTopicsApiController#find\_or\_create\_summary](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/summaries

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/summaries`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/summaries

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/summaries`

Generates a summary for a discussion topic. Returns the summary text and usage information.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| userInput |  | string | Areas or topics for the summary to focus on. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/summaries \
    -X POST \
    -H 'Authorization: Bearer <token>'
```

#### Example Response:

#### 

```
{
  "id": 1,
  "text": "This is a summary of the discussion topic.",
  "usage": { "currentCount": 1, "limit": 5 }
}
```

## [Disable summary](#method.discussion_topics_api.disable_summary) [DiscussionTopicsApiController#disable\_summary](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/summaries/disable

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/summaries/disable`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/summaries/disable

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/summaries/disable`

Deprecated, to remove after VICE-5047 gets merged Disables the summary for a discussion topic.

#### Example Request:

#### 

```
curl -X PUT https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/disable_summary \
```

#### Example Response:

#### 

```
{
  "success": true
}
```

## [Summary Feedback](#method.discussion_topics_api.summary_feedback) [DiscussionTopicsApiController#summary\_feedback](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/summaries/:summary\_id/feedback

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/summaries/:summary_id/feedback`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/summaries/:summary\_id/feedback

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/summaries/:summary_id/feedback`

Persists feedback on a discussion topic summary.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| \_action |  | string | Required The action to take on the summary. Possible values are:   * âseenâ: Marks the summary as seen. This action saves the feedback if itâs not already persisted. * âlikeâ: Marks the summary as liked. * âdislikeâ: Marks the summary as disliked. * âreset\_likeâ: Resets the like status of the summary. * âregenerateâ: Regenerates the summary feedback. * âdisable\_summaryâ: Disables the summary feedback.   Any other value will result in an error response. |

#### Example Request:

#### 

```
curl -X POST https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/summaries/<summary_id>/feedback \
     -F '_action=like' \
     -H "Authorization: Bearer
```

#### Example Response:

#### 

```
{
  "liked": true,
  "disliked": false
}
```

## [Get the full topic](#method.discussion_topics_api.view) [DiscussionTopicsApiController#view](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/view

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id/view`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/view

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id/view`

Return a cached structure of the discussion topic, containing all entries, their authors, and their message bodies.

May require (depending on the topic) that the user has posted in the topic. If it is required, and the user has not posted, will respond with a 403 Forbidden status and the body ârequire\_initial\_postâ.

In some rare situations, this cached structure may not be available yet. In that case, the server will respond with a 503 error, and the caller should try again soon.

The response is an object containing the following keys:

* âparticipantsâ: A list of summary information on users who have posted to the discussion. Each value is an object containing their id, display\_name, and avatar\_url.
* âunread\_entriesâ: A list of entry ids that are unread by the current user. this implies that any entry not in this list is read.
* âentry\_ratingsâ: A map of entry ids to ratings by the current user. Entries not in this list have no rating. Only populated if rating is enabled.
* âforced\_entriesâ: A list of entry ids that have forced\_read\_state set to true. This flag is meant to indicate the entryâs read\_state has been manually set to âunreadâ by the user, so the entry should not be automatically marked as read.
* âviewâ: A threaded view of all the entries in the discussion, containing the id, user\_id, and message.
* ânew\_entriesâ: Because this view is eventually consistent, itâs possible that newly created or updated entries wonât yet be reflected in the view. If the application wants to also get a flat list of all entries not yet reflected in the view, pass include\_new\_entries=1 to the request and this array of entries will be returned. These entries are returned in a flat array, in ascending created\_at order.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/view' \
     -H "Authorization: Bearer <token>"
```

#### Example Response:

#### 

```
{
  "unread_entries": [1,3,4],
  "entry_ratings": {3: 1},
  "forced_entries": [1],
  "participants": [
    { "id": 10, "display_name": "user 1", "avatar_image_url": "https://...", "html_url": "https://..." },
    { "id": 11, "display_name": "user 2", "avatar_image_url": "https://...", "html_url": "https://..." }
  ],
  "view": [
    { "id": 1, "user_id": 10, "parent_id": null, "message": "...html text...", "replies": [
      { "id": 3, "user_id": 11, "parent_id": 1, "message": "...html....", "replies": [...] }
    ]},
    { "id": 2, "user_id": 11, "parent_id": null, "message": "...html..." },
    { "id": 4, "user_id": 10, "parent_id": null, "message": "...html..." }
  ]
}
```

## [Post an entry](#method.discussion_topics_api.add_entry) [DiscussionTopicsApiController#add\_entry](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries`

Create a new entry in a discussion topic. Returns a json representation of the created entry (see documentation for âentriesâ method) on success.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| message |  | string | The body of the entry. |
| attachment |  | string | a multipart/form-data form-field-style attachment. Attachments larger than 1 kilobyte are subject to quota restrictions. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries.json' \
     -F 'message=<message>' \
     -F 'attachment=@<filename>' \
     -H "Authorization: Bearer <token>"
```

## [Duplicate discussion topic](#method.discussion_topics_api.duplicate) [DiscussionTopicsApiController#duplicate](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/duplicate

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/duplicate`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/duplicate

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/duplicate`

Duplicate a discussion topic according to context (Course/Group)

#### Example Request:

#### 

```
curl -X POST -H 'Authorization: Bearer <token>' \
https://<canvas>/api/v1/courses/123/discussion_topics/123/duplicate

curl -X POST -H 'Authorization: Bearer <token>' \
https://<canvas>/api/v1/group/456/discussion_topics/456/duplicate
```

Returns a
[DiscussionTopic](discussion_topics.html#DiscussionTopic)
object

## [List topic entries](#method.discussion_topics_api.entries) [DiscussionTopicsApiController#entries](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries`

Retrieve the (paginated) top-level entries in a discussion topic.

May require (depending on the topic) that the user has posted in the topic. If it is required, and the user has not posted, will respond with a 403 Forbidden status and the body ârequire\_initial\_postâ.

Will include the 10 most recent replies, if any, for each entry returned.

If the topic is a root topic with children corresponding to groups of a group assignment, entries from those subtopics for which the user belongs to the corresponding group will be returned.

Ordering of returned entries is newest-first by posting timestamp (reply activity is ignored).

#### API response field:

* id

  The unique identifier for the entry.
* user\_id

  The unique identifier for the author of the entry.
* editor\_id

  The unique user id of the person to last edit the entry, if different than user\_id.
* user\_name

  The name of the author of the entry.
* message

  The content of the entry.
* read\_state

  The read state of the entry, âreadâ or âunreadâ.
* forced\_read\_state

  Whether the read\_state was forced (was set manually)
* created\_at

  The creation time of the entry, in ISO8601 format.
* updated\_at

  The updated time of the entry, in ISO8601 format.
* attachment

  JSON representation of the attachment for the entry, if any. Present only if there is an attachment.
* attachments

  **Deprecated**. Same as attachment, but returned as a one-element array. Present only if there is an attachment.
* recent\_replies

  The 10 most recent replies for the entry, newest first. Present only if there is at least one reply.
* has\_more\_replies

  True if there are more than 10 replies for the entry (i.e., not all were included in this response). Present only if there is at least one reply.

#### Example Response:

#### 

```
[ {
    "id": 1019,
    "user_id": 7086,
    "user_name": "nobody@example.com",
    "message": "Newer entry",
    "read_state": "read",
    "forced_read_state": false,
    "created_at": "2011-11-03T21:33:29Z",
    "attachment": {
      "content-type": "unknown/unknown",
      "url": "http://www.example.com/files/681/download?verifier=JDG10Ruitv8o6LjGXWlxgOb5Sl3ElzVYm9cBKUT3",
      "filename": "content.txt",
      "display_name": "content.txt" } },
  {
    "id": 1016,
    "user_id": 7086,
    "user_name": "nobody@example.com",
    "message": "first top-level entry",
    "read_state": "unread",
    "forced_read_state": false,
    "created_at": "2011-11-03T21:32:29Z",
    "recent_replies": [
      {
        "id": 1017,
        "user_id": 7086,
        "user_name": "nobody@example.com",
        "message": "Reply message",
        "created_at": "2011-11-03T21:32:29Z"
      } ],
    "has_more_replies": false } ]
```

## [Post a reply](#method.discussion_topics_api.add_reply) [DiscussionTopicsApiController#add\_reply](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:entry\_id/replies

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:entry\_id/replies

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies`

Add a reply to an entry in a discussion topic. Returns a json representation of the created reply (see documentation for ârepliesâ method) on success.

May require (depending on the topic) that the user has posted in the topic. If it is required, and the user has not posted, will respond with a 403 Forbidden status and the body ârequire\_initial\_postâ.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| message |  | string | The body of the entry. |
| attachment |  | string | a multipart/form-data form-field-style attachment. Attachments larger than 1 kilobyte are subject to quota restrictions. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>/replies.json' \
     -F 'message=<message>' \
     -F 'attachment=@<filename>' \
     -H "Authorization: Bearer <token>"
```

## [List entry replies](#method.discussion_topics_api.replies) [DiscussionTopicsApiController#replies](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:entry\_id/replies

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:entry\_id/replies

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies`

Retrieve the (paginated) replies to a top-level entry in a discussion topic.

May require (depending on the topic) that the user has posted in the topic. If it is required, and the user has not posted, will respond with a 403 Forbidden status and the body ârequire\_initial\_postâ.

Ordering of returned entries is newest-first by creation timestamp.

#### API response field:

* id

  The unique identifier for the reply.
* user\_id

  The unique identifier for the author of the reply.
* editor\_id

  The unique user id of the person to last edit the entry, if different than user\_id.
* user\_name

  The name of the author of the reply.
* message

  The content of the reply.
* read\_state

  The read state of the entry, âreadâ or âunreadâ.
* forced\_read\_state

  Whether the read\_state was forced (was set manually)
* created\_at

  The creation time of the reply, in ISO8601 format.

#### Example Response:

#### 

```
[ {
    "id": 1015,
    "user_id": 7084,
    "user_name": "nobody@example.com",
    "message": "Newer message",
    "read_state": "read",
    "forced_read_state": false,
    "created_at": "2011-11-03T21:27:44Z" },
  {
    "id": 1014,
    "user_id": 7084,
    "user_name": "nobody@example.com",
    "message": "Older message",
    "read_state": "unread",
    "forced_read_state": false,
    "created_at": "2011-11-03T21:26:44Z" } ]
```

## [List entries](#method.discussion_topics_api.entry_list) [DiscussionTopicsApiController#entry\_list](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### GET /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entry\_list

**Scope:** 
`url:GET|/api/v1/courses/:course_id/discussion_topics/:topic_id/entry_list`

### GET /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entry\_list

**Scope:** 
`url:GET|/api/v1/groups/:group_id/discussion_topics/:topic_id/entry_list`

Retrieve a paginated list of discussion entries, given a list of ids.

May require (depending on the topic) that the user has posted in the topic. If it is required, and the user has not posted, will respond with a 403 Forbidden status and the body ârequire\_initial\_postâ.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| ids[] |  | string | A list of entry ids to retrieve. Entries will be returned in id order, smallest id first. |

#### API response field:

* id

  The unique identifier for the reply.
* user\_id

  The unique identifier for the author of the reply.
* user\_name

  The name of the author of the reply.
* message

  The content of the reply.
* read\_state

  The read state of the entry, âreadâ or âunreadâ.
* forced\_read\_state

  Whether the read\_state was forced (was set manually)
* created\_at

  The creation time of the reply, in ISO8601 format.
* deleted

  If the entry has been deleted, returns true. The user\_id, user\_name, and message will not be returned for deleted entries.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entry_list?ids[]=1&ids[]=2&ids[]=3' \
     -H "Authorization: Bearer <token>"
```

#### Example Response:

#### 

```
[
  { ... entry 1 ... },
  { ... entry 2 ... },
  { ... entry 3 ... },
]
```

## [Mark topic as read](#method.discussion_topics_api.mark_topic_read) [DiscussionTopicsApiController#mark\_topic\_read](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/read

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/read`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/read

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/read`

Mark the initial text of the discussion topic as read.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/read.json' \
     -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Length: 0"
```

## [Mark all topic as read](#method.discussion_topics_api.mark_all_topic_read) [DiscussionTopicsApiController#mark\_all\_topic\_read](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/read\_all

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/read_all`

### PUT /api/v1/groups/:group\_id/discussion\_topics/read\_all

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/read_all`

Mark the initial text of all the discussion topics as read in the context.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/read_all' \
     -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Length: 0"
```

## [Mark topic as unread](#method.discussion_topics_api.mark_topic_unread) [DiscussionTopicsApiController#mark\_topic\_unread](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/read

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id/read`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/read

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id/read`

Mark the initial text of the discussion topic as unread.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/read.json' \
     -X DELETE \
     -H "Authorization: Bearer <token>"
```

## [Mark all entries as read](#method.discussion_topics_api.mark_all_read) [DiscussionTopicsApiController#mark\_all\_read](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/read\_all

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/read_all`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/read\_all

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/read_all`

Mark the discussion topic and all its entries as read.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| forced\_read\_state |  | boolean | A boolean value to set all of the entriesâ forced\_read\_state. No change is made if this argument is not specified. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/read_all.json' \
     -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Length: 0"
```

## [Mark all entries as unread](#method.discussion_topics_api.mark_all_unread) [DiscussionTopicsApiController#mark\_all\_unread](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/read\_all

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id/read_all`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/read\_all

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id/read_all`

Mark the discussion topic and all its entries as unread.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| forced\_read\_state |  | boolean | A boolean value to set all of the entriesâ forced\_read\_state. No change is made if this argument is not specified. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/read_all.json' \
     -X DELETE \
     -H "Authorization: Bearer <token>"
```

## [Mark entry as read](#method.discussion_topics_api.mark_entry_read) [DiscussionTopicsApiController#mark\_entry\_read](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:entry\_id/read

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:entry\_id/read

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/read`

Mark a discussion entry as read.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| forced\_read\_state |  | boolean | A boolean value to set the entryâs forced\_read\_state. No change is made if this argument is not specified. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>/read.json' \
     -X PUT \
     -H "Authorization: Bearer <token>"\
     -H "Content-Length: 0"
```

## [Mark entry as unread](#method.discussion_topics_api.mark_entry_unread) [DiscussionTopicsApiController#mark\_entry\_unread](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:entry\_id/read

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:entry\_id/read

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/read`

Mark a discussion entry as unread.

No request fields are necessary.

On success, the response will be 204 No Content with an empty body.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| forced\_read\_state |  | boolean | A boolean value to set the entryâs forced\_read\_state. No change is made if this argument is not specified. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>/read.json' \
     -X DELETE \
     -H "Authorization: Bearer <token>"
```

## [Rate entry](#method.discussion_topics_api.rate_entry) [DiscussionTopicsApiController#rate\_entry](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### POST /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/entries/:entry\_id/rating

**Scope:** 
`url:POST|/api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/rating`

### POST /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/entries/:entry\_id/rating

**Scope:** 
`url:POST|/api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/rating`

Rate a discussion entry.

On success, the response will be 204 No Content with an empty body.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| rating |  | integer | A rating to set on this entry. Only 0 and 1 are accepted. |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/entries/<entry_id>/rating.json' \
     -X POST \
     -H "Authorization: Bearer <token>"
```

## [Subscribe to a topic](#method.discussion_topics_api.subscribe_topic) [DiscussionTopicsApiController#subscribe\_topic](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### PUT /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/subscribed

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed`

### PUT /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/subscribed

**Scope:** 
`url:PUT|/api/v1/groups/:group_id/discussion_topics/:topic_id/subscribed`

Subscribe to a topic to receive notifications about new entries

On success, the response will be 204 No Content with an empty body

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/subscribed.json' \
     -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Length: 0"
```

## [Unsubscribe from a topic](#method.discussion_topics_api.unsubscribe_topic) [DiscussionTopicsApiController#unsubscribe\_topic](https://github.com/instructure/canvas-lms/blob/master/app/controllers/discussion_topics_api_controller.rb)

### DELETE /api/v1/courses/:course\_id/discussion\_topics/:topic\_id/subscribed

**Scope:** 
`url:DELETE|/api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed`

### DELETE /api/v1/groups/:group\_id/discussion\_topics/:topic\_id/subscribed

**Scope:** 
`url:DELETE|/api/v1/groups/:group_id/discussion_topics/:topic_id/subscribed`

Unsubscribe from a topic to stop receiving notifications about new entries

On success, the response will be 204 No Content with an empty body

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/courses/<course_id>/discussion_topics/<topic_id>/subscribed.json' \
     -X DELETE \
     -H "Authorization: Bearer <token>"
```