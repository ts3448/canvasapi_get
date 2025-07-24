# Notice Handlers

# Notice Handlers API



API for the LTI Platform Notification Service.

Requires LTI Advantage (JWT OAuth2) tokens with the
`https://purl.imsglobal.org/spec/lti/scope/noticehandlers` scope.

See the Canvas
[Platform Notification Service](/doc/api/file.pns.html)
intro guide for an overview of these endpoints and information on specific
notice types.

### A NoticeCatalog object looks like:

```
// Set of notice handlers (one per notice type) for an LTI tool deployment.
{
  // The LTI tool's client ID (global developer key ID)
  "client_id": "10000000000001",
  // String that identifies the Platform-Tool integration governing the notices
  "deployment_id": "123:8865aa05b4b79b64a91a86042e43af5ea8ae79eb",
  // List of notice handlers for the tool
  "notice_handlers": [{"handler":"","notice_type":"LtiHelloWorldNotice"}]
}
```

### A NoticeHandler object looks like:

```
// A notice handler for a particular tool deployment and notice type.
{
  // URL to receive the notice
  "handler": "https://example.com/notice_handler",
  // The type of notice
  "notice_type": "LtiHelloWorldNotice",
  // The maximum number of notices to include in a single batch, or 'null' if not
  // set.
  "max_batch_size": 100
}
```

## [Show notice handlers](#method.lti/ims/notice_handlers.index) [Lti::Ims::NoticeHandlersController#index](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/ims/notice_handlers_controller.rb)

### GET /api/lti/notice-handlers/:context\_external\_tool\_id

**Scope:** 
`url:GET|/api/lti/notice-handlers/:context_external_tool_id`

List all notice handlers for the tool

#### Example Response:

#### 

```
{
  "client_id": 10000000000267,
  "deployment_id": "123:8865aa05b4b79b64a91a86042e43af5ea8ae79eb",
  "notice_handlers": [
    {
      "handler": "",
      "notice_type": "LtiHelloWorldNotice"
    }
  ]
}
```

Returns a
[NoticeCatalog](notice_handlers.html#NoticeCatalog)
object

## [Set notice handler](#method.lti/ims/notice_handlers.update) [Lti::Ims::NoticeHandlersController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/ims/notice_handlers_controller.rb)

### PUT /api/lti/notice-handlers/:context\_external\_tool\_id

**Scope:** 
`url:PUT|/api/lti/notice-handlers/:context_external_tool_id`

Subscribe (set) or unsubscribe (remove) a notice handler for the tool

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| notice\_type | Required | string | The type of notice |
| handler | Required | string | URL to receive the notice, or an empty string to unsubscribe |
| max\_batch\_size |  | integer | The maximum number of notices to include in a single batch |

#### Example Response:

#### 

```
{
    "handler": "",
    "notice_type": "LtiHelloWorldNotice"
}
```

Returns a
[NoticeHandler](notice_handlers.html#NoticeHandler)
object