# Content Shares

# Content Shares API



API for creating, accessing and updating Content Sharing. Content shares are used
to share content directly between users.

### A ContentShare object looks like:

```
// Content shared between users
{
  // The id of the content share for the current user
  "id": 1,
  // The name of the shared content
  "name": "War of 1812 homework",
  // The type of content that was shared. Can be assignment, discussion_topic,
  // page, quiz, module, or module_item.
  "content_type": "assignment",
  // The datetime the content was shared with this user.
  "created_at": "2017-05-09T10:12:00Z",
  // The datetime the content was updated.
  "updated_at": "2017-05-09T10:12:00Z",
  // The id of the user who sent or received the content share.
  "user_id": 1578941,
  // The user who shared the content. This field is provided only to receivers; it
  // is not populated in the sender's list of sent content shares.
  "sender": {"id":1,"display_name":"Matilda Vargas","avatar_image_url":"http:\/\/localhost:3000\/image_url","html_url":"http:\/\/localhost:3000\/users\/1"},
  // An Array of users the content is shared with.  This field is provided only to
  // senders; an empty array will be returned for the receiving users.
  "receivers": [{"id":1,"display_name":"Jon Snow","avatar_image_url":"http:\/\/localhost:3000\/image_url2","html_url":"http:\/\/localhost:3000\/users\/2"}],
  // The course the content was originally shared from.
  "source_course": {"id":787,"name":"History 105"},
  // Whether the recipient has viewed the content share.
  "read_state": "read",
  // The content export record associated with this content share
  "content_export": {"id":42}
}
```

## [Create a content share](#method.content_shares.create) [ContentSharesController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### POST /api/v1/users/:user\_id/content\_shares

**Scope:** 
`url:POST|/api/v1/users/:user_id/content_shares`

Share content directly between two or more users

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| receiver\_ids | Required | Array | IDs of users to share the content with. |
| content\_type | Required | string | Type of content you are sharing.  Allowed values: `assignment`, `discussion_topic`, `page`, `quiz`, `module`, `module_item` |
| content\_id | Required | integer | The id of the content that you are sharing |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/content_shares \
      -d 'content_type=assignment' \
      -d 'content_id=1' \
      -H 'Authorization: Bearer <token>' \
      -X POST
```

Returns a
[ContentShare](content_shares.html#ContentShare)
object

## [List content shares](#method.content_shares.index) [ContentSharesController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### GET /api/v1/users/:user\_id/content\_shares/sent

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_shares/sent`

### GET /api/v1/users/:user\_id/content\_shares/received

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_shares/received`

Return a paginated list of content shares a user has sent or received. Use `self` as the user\_id to retrieve your own content shares. Only linked observers and administrators may view other usersâ content shares.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/content_shares/received'
```

Returns a list of
[ContentShare](content_shares.html#ContentShare)
objects

## [Get unread shares count](#method.content_shares.unread_count) [ContentSharesController#unread\_count](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### GET /api/v1/users/:user\_id/content\_shares/unread\_count

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_shares/unread_count`

Return the number of content shares a user has received that have not yet been read. Use `self` as the user\_id to retrieve your own content shares. Only linked observers and administrators may view other usersâ content shares.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/content_shares/unread_count'
```

## [Get content share](#method.content_shares.show) [ContentSharesController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### GET /api/v1/users/:user\_id/content\_shares/:id

**Scope:** 
`url:GET|/api/v1/users/:user_id/content_shares/:id`

Return information about a single content share. You may use `self` as the user\_id to retrieve your own content share.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/content_shares/123'
```

Returns a
[ContentShare](content_shares.html#ContentShare)
object

## [Remove content share](#method.content_shares.destroy) [ContentSharesController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### DELETE /api/v1/users/:user\_id/content\_shares/:id

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/content_shares/:id`

Remove a content share from your list. Use `self` as the user\_id. Note that this endpoint does not delete other usersâ copies of the content share.

#### Example Request:

#### 

```
curl -X DELETE 'https://<canvas>/api/v1/users/self/content_shares/123'
```

## [Add users to content share](#method.content_shares.add_users) [ContentSharesController#add\_users](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### POST /api/v1/users/:user\_id/content\_shares/:id/add\_users

**Scope:** 
`url:POST|/api/v1/users/:user_id/content_shares/:id/add_users`

Send a previously created content share to additional users

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| receiver\_ids |  | Array | IDs of users to share the content with. |

#### Example Request:

#### 

```
curl -X POST 'https://<canvas>/api/v1/users/self/content_shares/123/add_users?receiver_ids[]=789'
```

Returns a
[ContentShare](content_shares.html#ContentShare)
object

## [Update a content share](#method.content_shares.update) [ContentSharesController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/content_shares_controller.rb)

### PUT /api/v1/users/:user\_id/content\_shares/:id

**Scope:** 
`url:PUT|/api/v1/users/:user_id/content_shares/:id`

Mark a content share read or unread

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| read\_state |  | string | Read state for the content share  Allowed values: `read`, `unread` |

#### Example Request:

#### 

```
curl -X PUT 'https://<canvas>/api/v1/users/self/content_shares/123?read_state=read'
```

Returns a
[ContentShare](content_shares.html#ContentShare)
object