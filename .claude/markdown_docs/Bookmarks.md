# Bookmarks

# Bookmarks API



### A Bookmark object looks like:

```
{
  "id": 1,
  "name": "Biology 101",
  "url": "/courses/1",
  "position": 1,
  "data": {"active_tab":1}
}
```

## [List bookmarks](#method.bookmarks/bookmarks.index) [Bookmarks::BookmarksController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/bookmarks/bookmarks_controller.rb)

### GET /api/v1/users/self/bookmarks

**Scope:** 
`url:GET|/api/v1/users/self/bookmarks`

Returns the paginated list of bookmarks.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/bookmarks' \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[Bookmark](bookmarks.html#Bookmark)
objects

## [Create bookmark](#method.bookmarks/bookmarks.create) [Bookmarks::BookmarksController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/bookmarks/bookmarks_controller.rb)

### POST /api/v1/users/self/bookmarks

**Scope:** 
`url:POST|/api/v1/users/self/bookmarks`

Creates a bookmark.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The name of the bookmark |
| url |  | string | The url of the bookmark |
| position |  | integer | The position of the bookmark. Defaults to the bottom. |
| data |  | string | The data associated with the bookmark |

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/bookmarks' \
     -F 'name=Biology 101' \
     -F 'url=/courses/1' \
     -H 'Authorization: Bearer <token>'
```

Returns a
[Bookmark](bookmarks.html#Bookmark)
object

## [Get bookmark](#method.bookmarks/bookmarks.show) [Bookmarks::BookmarksController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/bookmarks/bookmarks_controller.rb)

### GET /api/v1/users/self/bookmarks/:id

**Scope:** 
`url:GET|/api/v1/users/self/bookmarks/:id`

Returns the details for a bookmark.

#### Example Request:

#### 

```
curl 'https://<canvas>/api/v1/users/self/bookmarks/1' \
     -H 'Authorization: Bearer <token>'
```

Returns a
[Bookmark](bookmarks.html#Bookmark)
object

## [Update bookmark](#method.bookmarks/bookmarks.update) [Bookmarks::BookmarksController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/bookmarks/bookmarks_controller.rb)

### PUT /api/v1/users/self/bookmarks/:id

**Scope:** 
`url:PUT|/api/v1/users/self/bookmarks/:id`

Updates a bookmark

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The name of the bookmark |
| url |  | string | The url of the bookmark |
| position |  | integer | The position of the bookmark. Defaults to the bottom. |
| data |  | string | The data associated with the bookmark |

#### Example Request:

#### 

```
curl -X PUT 'https://<canvas>/api/v1/users/self/bookmarks/1' \
     -F 'name=Biology 101' \
     -F 'url=/courses/1' \
     -H 'Authorization: Bearer <token>'
```

Returns a
[Folder](files.html#Folder)
object

## [Delete bookmark](#method.bookmarks/bookmarks.destroy) [Bookmarks::BookmarksController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/bookmarks/bookmarks_controller.rb)

### DELETE /api/v1/users/self/bookmarks/:id

**Scope:** 
`url:DELETE|/api/v1/users/self/bookmarks/:id`

Deletes a bookmark

#### Example Request:

#### 

```
curl -X DELETE 'https://<canvas>/api/v1/users/self/bookmarks/1' \
     -H 'Authorization: Bearer <token>'
```