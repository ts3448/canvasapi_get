# Favorites

# Favorites API



### A Favorite object looks like:

```
{
  // The ID of the object the Favorite refers to
  "context_id": 1170,
  // The type of the object the Favorite refers to (currently, only 'Course' is
  // supported)
  "context_type": "Course"
}
```

## [List favorite courses](#method.favorites.list_favorite_courses) [FavoritesController#list\_favorite\_courses](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### GET /api/v1/users/self/favorites/courses

**Scope:** 
`url:GET|/api/v1/users/self/favorites/courses`

Retrieve the paginated list of favorite courses for the current user. If the user has not chosen any favorites, then a selection of currently enrolled courses will be returned.

See the [List courses API](courses.html#method.courses.index "List courses API") for details on accepted include[] parameters.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| exclude\_blueprint\_courses |  | boolean | When set, only return courses that are not configured as blueprint courses. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/courses \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

Returns a list of
[Course](courses.html#Course)
objects

## [List favorite groups](#method.favorites.list_favorite_groups) [FavoritesController#list\_favorite\_groups](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### GET /api/v1/users/self/favorites/groups

**Scope:** 
`url:GET|/api/v1/users/self/favorites/groups`

Retrieve the paginated list of favorite groups for the current user. If the user has not chosen any favorites, then a selection of groups that the user is a member of will be returned.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/groups \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

Returns a list of
[Group](groups.html#Group)
objects

## [Add course to favorites](#method.favorites.add_favorite_course) [FavoritesController#add\_favorite\_course](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### POST /api/v1/users/self/favorites/courses/:id

**Scope:** 
`url:POST|/api/v1/users/self/favorites/courses/:id`

Add a course to the current userâs favorites. If the course is already in the userâs favorites, nothing happens. Canvas for Elementary subject and homeroom courses can be added to favorites, but this has no effect in the UI.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id | Required | string | The ID or SIS ID of the course to add. The current user must be registered in the course. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/courses/1170 \
  -X POST \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Length: 0'
```

Returns a
[Favorite](favorites.html#Favorite)
object

## [Add group to favorites](#method.favorites.add_favorite_groups) [FavoritesController#add\_favorite\_groups](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### POST /api/v1/users/self/favorites/groups/:id

**Scope:** 
`url:POST|/api/v1/users/self/favorites/groups/:id`

Add a group to the current userâs favorites. If the group is already in the userâs favorites, nothing happens.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id | Required | string | The ID or SIS ID of the group to add. The current user must be a member of the group. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/group/1170 \
  -X POST \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Length: 0'
```

Returns a
[Favorite](favorites.html#Favorite)
object

## [Remove course from favorites](#method.favorites.remove_favorite_course) [FavoritesController#remove\_favorite\_course](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### DELETE /api/v1/users/self/favorites/courses/:id

**Scope:** 
`url:DELETE|/api/v1/users/self/favorites/courses/:id`

Remove a course from the current userâs favorites.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id | Required | string | the ID or SIS ID of the course to remove |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/courses/1170 \
  -X DELETE \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

Returns a
[Favorite](favorites.html#Favorite)
object

## [Remove group from favorites](#method.favorites.remove_favorite_groups) [FavoritesController#remove\_favorite\_groups](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### DELETE /api/v1/users/self/favorites/groups/:id

**Scope:** 
`url:DELETE|/api/v1/users/self/favorites/groups/:id`

Remove a group from the current userâs favorites.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| id | Required | string | the ID or SIS ID of the group to remove |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/groups/1170 \
  -X DELETE \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

Returns a
[Favorite](favorites.html#Favorite)
object

## [Reset course favorites](#method.favorites.reset_course_favorites) [FavoritesController#reset\_course\_favorites](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### DELETE /api/v1/users/self/favorites/courses

**Scope:** 
`url:DELETE|/api/v1/users/self/favorites/courses`

Reset the current userâs course favorites to the default automatically generated list of enrolled courses

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/courses \
  -X DELETE \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

## [Reset group favorites](#method.favorites.reset_groups_favorites) [FavoritesController#reset\_groups\_favorites](https://github.com/instructure/canvas-lms/blob/master/app/controllers/favorites_controller.rb)

### DELETE /api/v1/users/self/favorites/groups

**Scope:** 
`url:DELETE|/api/v1/users/self/favorites/groups`

Reset the current userâs group favorites to the default automatically generated list of enrolled group

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/favorites/group \
  -X DELETE \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```