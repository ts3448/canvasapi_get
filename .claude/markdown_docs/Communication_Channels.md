# Communication Channels

# Communication Channels API



API for accessing users' email and SMS communication channels.

In this API, the `:user_id` parameter can always be replaced with `self` if
the requesting user is asking for his/her own information.

### A CommunicationChannel object looks like:

```
{
  // The ID of the communication channel.
  "id": 16,
  // The address, or path, of the communication channel.
  "address": "sheldon@caltech.example.com",
  // The type of communcation channel being described. Possible values are:
  // 'email', 'push', 'sms'. This field determines the type of value seen in
  // 'address'.
  "type": "email",
  // The position of this communication channel relative to the user's other
  // channels when they are ordered.
  "position": 1,
  // The ID of the user that owns this communication channel.
  "user_id": 1,
  // The number of bounces the channel has experienced. This is reset if the
  // channel sends successfully.
  "bounce_count": 0,
  // The time the last bounce occurred.
  "last_bounce_at": "2012-05-30T17:00:00Z",
  // The current state of the communication channel. Possible values are:
  // 'unconfirmed' or 'active'.
  "workflow_state": "active"
}
```

## [List user communication channels](#method.communication_channels.index) [CommunicationChannelsController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/communication_channels_controller.rb)

### GET /api/v1/users/:user\_id/communication\_channels

**Scope:** 
`url:GET|/api/v1/users/:user_id/communication_channels`

Returns a paginated list of communication channels for the specified user, sorted by position.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/12345/communication_channels \
     -H 'Authorization: Bearer <token>'
```

Returns a list of
[CommunicationChannel](communication_channels.html#CommunicationChannel)
objects

## [Create a communication channel](#method.communication_channels.create) [CommunicationChannelsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/communication_channels_controller.rb)

### POST /api/v1/users/:user\_id/communication\_channels

**Scope:** 
`url:POST|/api/v1/users/:user_id/communication_channels`

Creates a new communication channel for the specified user.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| communication\_channel[address] | Required | string | An email address or SMS number. Not required for âpushâ type channels. |
| communication\_channel[type] | Required | string | The type of communication channel.  In order to enable push notification support, the server must be properly configured (via âsns\_creds` in Vault) to communicate with Amazon Simple Notification Services, and the developer key used to create the access token from this request must have an SNS ARN configured on it.  Allowed values: `email`, `sms`, `push` |
| communication\_channel[token] |  | string | A registration id, device token, or equivalent token given to an app when registering with a push notification provider. Only valid for âpushâ type channels. |
| skip\_confirmation |  | boolean | Only valid for site admins and account admins making requests; If true, the channel is automatically validated and no confirmation email or SMS is sent. Otherwise, the user must respond to a confirmation message to confirm the channel. |

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/1/communication_channels \
     -H 'Authorization: Bearer <token>' \
     -d 'communication_channel[address]=new@example.com' \
     -d 'communication_channel[type]=email' \
```

Returns a
[CommunicationChannel](communication_channels.html#CommunicationChannel)
object

## [Delete a communication channel](#method.communication_channels.destroy) [CommunicationChannelsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/communication_channels_controller.rb)

### DELETE /api/v1/users/:user\_id/communication\_channels/:id

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/communication_channels/:id`

### DELETE /api/v1/users/:user\_id/communication\_channels/:type/:address

**Scope:** 
`url:DELETE|/api/v1/users/:user_id/communication_channels/:type/:address`

Delete an existing communication channel.

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/5/communication_channels/3
     -H 'Authorization: Bearer <token>
     -X DELETE
```

Returns a
[CommunicationChannel](communication_channels.html#CommunicationChannel)
object

## [Delete a push notification endpoint](#method.communication_channels.delete_push_token) [CommunicationChannelsController#delete\_push\_token](https://github.com/instructure/canvas-lms/blob/master/app/controllers/communication_channels_controller.rb)

### DELETE /api/v1/users/self/communication\_channels/push

**Scope:** 
`url:DELETE|/api/v1/users/self/communication_channels/push`

#### Example Request:

#### 

```
curl https://<canvas>/api/v1/users/self/communication_channels/push
     -H 'Authorization: Bearer <token>
     -X DELETE
     -d 'push_token=<push_token>'
```