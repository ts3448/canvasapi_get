# Services

# Services API



## [Get Kaltura config](#method.services_api.show_kaltura_config) [ServicesApiController#show\_kaltura\_config](https://github.com/instructure/canvas-lms/blob/master/app/controllers/services_api_controller.rb)

### GET /api/v1/services/kaltura

**Scope:** 
`url:GET|/api/v1/services/kaltura`

Return the config information for the Kaltura plugin in json format.

#### API response field:

* enabled

  Enabled state of the Kaltura plugin
* domain

  Main domain of the Kaltura instance (This is the URL where the Kaltura API resides)
* resources\_domain

  Kaltura URL for grabbing thumbnails and other resources
* rtmp\_domain

  Hostname to be used for RTMP recording
* partner\_id

  Partner ID used for communicating with the Kaltura instance

#### Example Response:

#### 

```
# For an enabled Kaltura plugin:
{
  'domain': 'kaltura.example.com',
  'enabled': true,
  'partner_id': '123456',
  'resource_domain': 'cdn.kaltura.example.com',
  'rtmp_domain': 'rtmp.example.com'
}

# For a disabled or unconfigured Kaltura plugin:
{
  'enabled': false
}
```

## [Start Kaltura session](#method.services_api.start_kaltura_session) [ServicesApiController#start\_kaltura\_session](https://github.com/instructure/canvas-lms/blob/master/app/controllers/services_api_controller.rb)

### POST /api/v1/services/kaltura\_session

**Scope:** 
`url:POST|/api/v1/services/kaltura_session`

Start a new Kaltura session, so that new media can be recorded and uploaded to this Canvas instanceâs Kaltura instance.

#### API response field:

* ks

  The kaltura session id, for use in the kaltura v3 API. This can be used in the uploadtoken service, for instance, to upload a new media file into kaltura.

#### Example Response:

#### 

```
{
  'ks': '1e39ad505f30c4fa1af5752b51bd69fe'
}
```