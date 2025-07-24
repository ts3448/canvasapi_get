# LTI Registrations

# LTI Registrations API

### BETA: This API resource is not finalized, and there could be breaking changes before its final release.



API for accessing and configuring LTI registrations in a root account.
LTI Registrations can be any of:

* 1.3 Dynamic Registration
* 1.3 manual installation (via JSON, URL, or UI)
* 1.1 manual installation (via XML, URL, or UI)

The Dynamic Registration process uses a different API endpoint to finalize
the process and create the registration. The
[Registration guide](/doc/api/registration.html) has more details on that process.

### A Lti::Registration object looks like:

```
// A registration of an LTI tool in Canvas
{
  // the Canvas ID of the Lti::Registration object
  "id": 2,
  // Tool-provided registration name
  "name": "My LTI Tool",
  // Admin-configured friendly display name
  "admin_nickname": "My LTI Tool (Campus A)",
  // Tool-provided URL to the tool's icon
  "icon_url": "https://mytool.com/icon.png",
  // Tool-provided name of the tool vendor
  "vendor": "My Tool LLC",
  // The Canvas id of the account that owns this registration
  "account_id": 1,
  // Flag indicating if registration is internally-owned
  "internal_service": false,
  // Flag indicating if registration is owned by this account, or inherited from
  // Site Admin
  "inherited": false,
  // LTI version of the registration, either 1.1 or 1.3
  "lti_version": "1.3",
  // Flag indicating if registration was created using LTI Dynamic Registration.
  // Only present if lti_version is 1.3
  "dynamic_registration": false,
  // The state of the registration
  "workflow_state": "active",
  // Timestamp of the registration's creation
  "created_at": "2024-01-01T00:00:00Z",
  // Timestamp of the registration's last update
  "updated_at": "2024-01-01T00:00:00Z",
  // The user that created this registration. Not always present. If a string,
  // this registration was created by Instructure.
  "created_by": {"type":"User"},
  // The user that last updated this registration. Not always present. If a
  // string, this registration was last updated by Instructure.
  "updated_by": {"type":"User"},
  // The Canvas id of the root account
  "root_account_id": 1,
  // The binding for this registration and this account
  "account_binding": {"type":"Lti::RegistrationAccountBinding"},
  // The Canvas-style tool configuration for this registration
  "configuration": {"type":"Lti::ToolConfiguration"}
}
```

### A Lti::LegacyConfiguration object looks like:

```
// A legacy configuration format for LTI 1.3 tools.
{
  // The display name of the tool
  "title": "My Tool",
  // The description of the tool
  "description": "My Tool is built by me, for me.",
  // A key-value listing of all custom fields the tool has requested
  "custom_fields": {"context_title":"$Context.title","special_tool_thing":"foo1234"},
  // The default launch URL for the tool. Overridable by placements.
  "target_link_uri": "https://mytool.com/launch",
  // 1.3 specific. URL used for initial login request
  "oidc_initiation_url": "https://mytool.com/1_3/login",
  // 1.3 specific. Region-specific login URLs for data protection compliance
  "oidc_initiation_urls": {"eu-west-1":"https:\/\/dub.mytool.com\/1_3\/login"},
  // 1.3 specific. The tool's public JWK in JSON format. Discouraged in favor of a
  // url hosting a JWK set.
  "public_jwk": {"e":"AQAB","etc":"etc"},
  // 1.3 specific. The tool-hosted URL containing its public JWK keyset. Canvas
  // may cache JWKs up to 5 minutes.
  "public_jwk_url": "https://mytool.com/1_3/jwks",
  // 1.3 specific. List of LTI scopes requested by the tool
  "scopes": ["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"],
  // Array of extensions for the tool
  "extensions": null
}
```

### A Lti::ToolConfiguration object looks like:

```
// A Registration's Canvas-specific tool configuration.
{
  // The display name of the tool
  "title": "My Tool",
  // The description of the tool
  "description": "My Tool is built by me, for me.",
  // A key-value listing of all custom fields the tool has requested
  "custom_fields": {"context_title":"$Context.title","special_tool_thing":"foo1234"},
  // The default launch URL for the tool. Overridable by placements.
  "target_link_uri": "https://mytool.com/launch",
  // The tool's main domain. Highly recommended for deep linking, used to match
  // links to the tool.
  "domain": "mytool.com",
  // Tool-provided identifier, can be anything
  "tool_id": "MyTool",
  // Canvas-defined privacy level for the tool
  "privacy_level": "public",
  // 1.3 specific. URL used for initial login request
  "oidc_initiation_url": "https://mytool.com/1_3/login",
  // 1.3 specific. Region-specific login URLs for data protection compliance
  "oidc_initiation_urls": {"eu-west-1":"https:\/\/dub.mytool.com\/1_3\/login"},
  // 1.3 specific. The tool's public JWK in JSON format. Discouraged in favor of a
  // url hosting a JWK set.
  "public_jwk": {"e":"AQAB","etc":"etc"},
  // 1.3 specific. The tool-hosted URL containing its public JWK keyset. Canvas
  // may cache JWKs up to 5 minutes.
  "public_jwk_url": "https://mytool.com/1_3/jwks",
  // 1.3 specific. List of LTI scopes requested by the tool
  "scopes": ["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"],
  // 1.3 specific. List of possible launch URLs for after the Canvas authorize
  // redirect step
  "redirect_uris": ["https://mytool.com/launch", "https://mytool.com/1_3/launch"],
  // Default launch settings for all placements
  "launch_settings": {"message_type":"LtiResourceLinkRequest"},
  // List of placements configured by the tool
  "placements": [{"type":"Lti::Placement"}]
}
```

### A Lti::LaunchSettings object looks like:

```
// Default launch settings for all placements
{
  // Default message type for all placements
  "message_type": "LtiResourceLinkRequest",
  // The text of the link to the tool (if applicable).
  "text": "Hello World",
  // Canvas-specific i18n for placement text. See the Navigation Placement docs.
  "labels": {"en":"Hello World","es":"Hola Mundo"},
  // Placement-specific custom fields to send in the launch. Merged with
  // tool-level custom fields.
  "custom_fields": {"special_placement_thing":"foo1234"},
  // Default iframe height. Not valid for all placements. Overrides tool-level
  // launch_height.
  "selection_height": 800,
  // Default iframe width. Not valid for all placements. Overrides tool-level
  // launch_width.
  "selection_width": 1000,
  // Default iframe height. Not valid for all placements. Overrides tool-level
  // launch_height.
  "launch_height": 800,
  // Default iframe width. Not valid for all placements. Overrides tool-level
  // launch_width.
  "launch_width": 1000,
  // Default icon URL. Not valid for all placements. Overrides tool-level
  // icon_url.
  "icon_url": "https://mytool.com/icon.png",
  // The HTML class name of an InstUI Icon. Used instead of an icon_url in select
  // placements.
  "canvas_icon_class": "icon-lti",
  // Comma-separated list of Canvas permission short names required for a user to
  // launch from this placement.
  "required_permissions": "manage_course_content_edit,manage_course_content_read",
  // When set to '_blank', opens placement in a new tab.
  "windowTarget": "_blank",
  // The Canvas layout to use when launching the tool. See the Navigation
  // Placement docs.
  "display_type": "full_width_in_context",
  // The 1.1 launch URL for this placement. Overrides tool-level url.
  "url": "https://mytool.com/launch?placement=course_navigation",
  // The 1.3 launch URL for this placement. Overrides tool-level target_link_uri.
  "target_link_uri": "https://mytool.com/launch?placement=course_navigation",
  // Specifies types of users that can see this placement. Only valid for some
  // placements like course_navigation.
  "visibility": "admins",
  // 1.1 specific. If true, the tool will send the SIS email in the
  // lis_person_contact_email_primary launch property
  "prefer_sis_email": false,
  // 1.1 specific. If true, query parameters from the launch URL will not be
  // copied to the POST body.
  "oauth_compliant": true,
  // An SVG to use instead of an icon_url. Only valid for global_navigation.
  "icon_svg_path_64": "M100,37L70.1,10.5v176H37...",
  // Default display state for course_navigation. If 'enabled', will show in
  // course sidebar. If 'disabled', will be hidden.
  "default": "disabled",
  // Comma-separated list of media types that the tool can accept. Only valid for
  // file_item.
  "accept_media_types": "image/*,video/*",
  // If true, the tool will be launched in the tray. Only used by the
  // editor_button placement.
  "use_tray": true
}
```

### A Lti::Placement object looks like:

```
// The tool's configuration for a specific placement
{
  // The name of the placement.
  "placement": "course_navigation",
  // If true, the tool will show in this placement. If false, it will not.
  "enabled": true,
  // Default message type for all placements
  "message_type": "LtiResourceLinkRequest",
  // The text of the link to the tool (if applicable).
  "text": "Hello World",
  // Canvas-specific i18n for placement text. See the Navigation Placement docs.
  "labels": {"en":"Hello World","es":"Hola Mundo"},
  // Placement-specific custom fields to send in the launch. Merged with
  // tool-level custom fields.
  "custom_fields": {"special_placement_thing":"foo1234"},
  // Default iframe height. Not valid for all placements. Overrides tool-level
  // launch_height.
  "selection_height": 800,
  // Default iframe width. Not valid for all placements. Overrides tool-level
  // launch_width.
  "selection_width": 1000,
  // Default iframe height. Not valid for all placements. Overrides tool-level
  // launch_height.
  "launch_height": 800,
  // Default iframe width. Not valid for all placements. Overrides tool-level
  // launch_width.
  "launch_width": 1000,
  // Default icon URL. Not valid for all placements. Overrides tool-level
  // icon_url.
  "icon_url": "https://mytool.com/icon.png",
  // The HTML class name of an InstUI Icon. Used instead of an icon_url in select
  // placements.
  "canvas_icon_class": "icon-lti",
  // Comma-separated list of Canvas permission short names required for a user to
  // launch from this placement.
  "required_permissions": "manage_course_content_edit,manage_course_content_read",
  // When set to '_blank', opens placement in a new tab.
  "windowTarget": "_blank",
  // The Canvas layout to use when launching the tool. See the Navigation
  // Placement docs.
  "display_type": "full_width_in_context",
  // The 1.1 launch URL for this placement. Overrides tool-level url.
  "url": "https://mytool.com/launch?placement=course_navigation",
  // The 1.3 launch URL for this placement. Overrides tool-level target_link_uri.
  "target_link_uri": "https://mytool.com/launch?placement=course_navigation",
  // Specifies types of users that can see this placement. Only valid for some
  // placements like course_navigation.
  "visibility": "admins",
  // 1.1 specific. If true, the tool will send the SIS email in the
  // lis_person_contact_email_primary launch property
  "prefer_sis_email": false,
  // (Only applies to 1.1) If true, Canvas will not copy launch URL query
  // parameters to the POST body.
  "oauth_compliant": true,
  // An SVG to use instead of an icon_url. Only valid for global_navigation.
  "icon_svg_path_64": "M100,37L70.1,10.5v176H37...",
  // Default display state for course_navigation. If 'enabled', will show in
  // course sidebar. If 'disabled', will be hidden.
  "default": "disabled",
  // Comma-separated list of media types that the tool can accept. Only valid for
  // file_item.
  "accept_media_types": "image/*,video/*",
  // If true, the tool will be launched in the tray. Only used by the
  // editor_button placement.
  "use_tray": true
}
```

### A Lti::Overlay object looks like:

```
// Changes made by a Canvas admin to a tool's configuration.
{
  // The display name of the tool
  "title": "My Tool",
  // The description of the tool
  "description": "My Tool is built by me, for me.",
  // A key-value listing of all custom fields the tool has requested
  "custom_fields": {"context_title":"$Context.title","special_tool_thing":"foo1234"},
  // The default launch URL for the tool. Overridable by placements.
  "target_link_uri": "https://mytool.com/launch",
  // The tool's main domain. Highly recommended for deep linking, used to match
  // links to the tool.
  "domain": "mytool.com",
  // Canvas-defined privacy level for the tool
  "privacy_level": "public",
  // 1.3 specific. URL used for initial login request
  "oidc_initiation_url": "https://mytool.com/1_3/login",
  // 1.3 specific. List of LTI scopes that the tool has requested but an admin has
  // disabled
  "disabled_scopes": ["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"],
  // List of placements that the tool has requested but an admin has disabled
  "disabled_placements": ["course_navigation"],
  // Placement-specific settings changed by an admin
  "placements": {"course_navigation":{"$ref":"Lti::Placement"}}
}
```

### A Lti::PlacementOverlay object looks like:

```
// Changes made by a Canvas admin to a tool's configuration for a specific
// placement.
{
  // The text of the link to the tool (if applicable).
  "text": "Hello World",
  // The default launch URL for the tool. Overridable by placements.
  "target_link_uri": "https://mytool.com/launch",
  // Default message type for all placements
  "message_type": "LtiResourceLinkRequest",
  // Default iframe height. Not valid for all placements. Overrides tool-level
  // launch_height.
  "launch_height": 800,
  // Default iframe width. Not valid for all placements. Overrides tool-level
  // launch_width.
  "launch_width": 1000,
  // Default icon URL. Not valid for all placements. Overrides tool-level
  // icon_url.
  "icon_url": "https://mytool.com/icon.png",
  // Default display state for course_navigation. If 'enabled', will show in
  // course sidebar. If 'disabled', will be hidden.
  "default": "disabled"
}
```

### A ListLtiRegistrationsResponse object looks like:

```
// The response for the List LTI Registrations API endpoint
{
  // The total number of LTI registrations across all pages
  "total": 1,
  // The paginated list of LTI::Registrations
  "data": [{"$ref":"Lti::Registration"}]
}
```

### A ContextSearchResponse object looks like:

```
// The response for the Search Accounts and Courses API endpoint
{
  // Accounts that match the search query. Limited to 100.
  "accounts": [{"$ref":"Account"}],
  // Courses that match the search query. Limited to 100.
  "courses": [{"$ref":"Course"}]
}
```

### A SearchableAccount object looks like:

```
// A minimal representation of an Account for Canvas Apps search purposes
{
  // The Canvas DB ID
  "id": "1",
  // The account name
  "name": "An Account",
  // The SIS ID of the account, if any. Only present if user can read or manage
  // SIS.
  "sis_id": "sis-account-1",
  // Names of the accounts in this account's hierarchy, excluding the root and
  // this account.
  "display_path": ["Sub Account"]
}
```

### A SearchableCourse object looks like:

```
// A minimal representation of a Course for Canvas Apps search purposes
{
  // The Canvas DB ID
  "id": "1",
  // The course name
  "name": "A Course",
  // The SIS ID of the course, if any. Only present if user can read or manage
  // SIS.
  "sis_id": "sis-course-1",
  // Names of the accounts in this course's account hierarchy, excluding the root.
  "display_path": ["Sub Account"],
  // The course code
  "course_code": "COURSE-101"
}
```

## [List LTI Registrations in an account](#method.lti/registrations.list) [Lti::RegistrationsController#list](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/accounts/:account\_id/lti\_registrations

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/lti_registrations`

Returns all LTI registrations in the specified account. Includes registrations created in this account, those set to âallowâ from a parent root account (like Site Admin) and âonâ for this account, and those enabled âonâ at the parent root account level.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| per\_page |  | integer | The number of registrations to return per page. Defaults to 15. |
| page |  | integer | The page number to return. Defaults to 1. |
| sort |  | string | The field to sort by. Choices are: name, nickname, lti\_version, installed, installed\_by, updated\_by, updated, and on. Defaults to installed. |
| dir |  | string | The order to sort the given column by. Defaults to desc.  Allowed values: `asc`, `desc` |
| include[] |  | string | Array of additional data to include. Always includes [account\_binding].  âaccount\_bindingâ  the registrationâs binding to the given account  âconfigurationâ  the registrationâs Canvas-style tool configuration, without any overlays applied.  âoverlaid\_configurationâ  the registrationâs Canvas-style tool configuration, with all overlays applied.  âoverlayâ  the registrationâs admin-defined configuration overlay |

#### Example Request:

#### 

```
This would return the specified LTI registration
curl -X GET 'https://<canvas>/api/v1/accounts/<account_id>/registrations' \
     -H "Authorization: Bearer <token>"
```

Returns a
[ListLtiRegistrationsResponse](lti_registrations.html#ListLtiRegistrationsResponse)
object

## [Show an LTI Registration](#method.lti/registrations.show) [Lti::RegistrationsController#show](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/accounts/:account\_id/lti\_registrations/:id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/lti_registrations/:id`

Return details about the specified LTI registration, including the configuration and account binding.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| include[] |  | string | Array of additional data to include. Always includes [account\_binding configuration].  âaccount\_bindingâ  the registrationâs binding to the given account  âconfigurationâ  the registrationâs Canvas-style tool configuration, without any overlays applied.  âoverlaid\_configurationâ  the registrationâs Canvas-style tool configuration, with all overlays applied.  âoverlaid\_legacy\_configurationâ  the registrationâs legacy-style configuration, with all overlays applied.  âoverlayâ  the registrationâs admin-defined configuration overlay  âoverlay\_versionsâ  the registrationâs overlayâs edit history |

#### Example Request:

#### 

```
This would return the specified LTI registration
curl -X GET 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/<registration_id>' \
     -H "Authorization: Bearer <token>"
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Create an LTI Registration](#method.lti/registrations.create) [Lti::RegistrationsController#create](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### POST /api/v1/accounts/:account\_id/lti\_registrations

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/lti_registrations`

Create a new LTI Registration, as well as an associated Tool Configuration, Developer Key, and Registration Account binding. To install/create using Dynamic Registration, please use the <a href=â/doc/api/registration.htmlâ>Dynamic Registration API.</a>

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The name of the tool. If one isnât provided, it will be inferred from the configurationâs title. |
| admin\_nickname |  | string | A friendly nickname set by admins to override the tool name |
| vendor |  | string | The vendor of the tool |
| description |  | string | A description of the tool. Cannot exceed 2048 bytes. |
| configuration |  | string | Required, Lti::ToolConfiguration | Lti::LegacyConfiguration  The LTI 1.3 configuration for the tool |
| overlay |  | string | Lti::Overlay  The overlay configuration for the tool. Overrides values in the base configuration. |
| unified\_tool\_id |  | string | The unique identifier for the tool, used for analytics. If not provided, one will be generated. |
| workflow\_state |  | string | The desired state for this registration/account binding. âallowâ is only valid for Site Admin registrations. Defaults to âoffâ.  Allowed values: `on`, `off`, `allow` |

#### Example Request:

#### 

```
This would create a new LTI Registration, as well as an associated Developer Key
and LTI Tool Configuration.

curl -X POST 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations' \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
          "vendor": "Example",
          "name": "An Example Tool",
          "admin_nickname": "A Great LTI Tool",
          "configuration": {
            "title": "Sample Tool",
            "description": "A sample LTI tool",
            "target_link_uri": "https://example.com/launch",
            "oidc_initiation_url": "https://example.com/oidc",
            "redirect_uris": ["https://example.com/redirect"],
            "scopes": ["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"],
            "placements": [
              {
                "placement": "course_navigation",
                "enabled": true
              }
            ],
            "launch_settings": {}
          }
        }'
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Show an LTI Registration (via the client\_id)](#method.lti/registrations.show_by_client_id) [Lti::RegistrationsController#show\_by\_client\_id](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/accounts/:account\_id/lti\_registration\_by\_client\_id/:client\_id

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/lti_registration_by_client_id/:client_id`

Returns details about the specified LTI registration, including the configuration and account binding.

#### Example Request:

#### 

```
This would return the specified LTI registration
curl -X GET 'https://<canvas>/api/v1/accounts/<account_id>/lti_registration_by_client_id/<client_id>' \
     -H "Authorization: Bearer <token>"
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Update an LTI Registration](#method.lti/registrations.update) [Lti::RegistrationsController#update](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### PUT /api/v1/accounts/:account\_id/lti\_registrations/:id

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/lti_registrations/:id`

Update the specified LTI registration with the provided parameters. Note that updating the base tool configuration of a registration that is associated with a Dynamic Registration will return a 422. All other fields can be updated freely.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| name |  | string | The name of the tool |
| admin\_nickname |  | string | The admin-configured friendly display name for the registration |
| description |  | string | A description of the tool. Cannot exceed 2048 bytes. |
| configuration |  | string | Lti::ToolConfiguration | Lti::LegacyConfiguration  The LTI 1.3 configuration for the tool. Note that updating the base tool configuration of a registration associated with a Dynamic Registration is not allowed. |
| overlay |  | string | Lti::Overlay  The overlay configuration for the tool. Overrides values in the base configuration. Note that updating the overlay of a registration associated with a Dynamic Registration IS allowed. |
| workflow\_state |  | string | The desired state for this registration/account binding. âallowâ is only valid for Site Admin registrations.  Allowed values: `on`, `off`, `allow` |

#### Example Request:

#### 

```
This would update the specified LTI Registration, as well as its associated Developer Key
and LTI Tool Configuration.

curl -X PUT 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/<registration_id>' \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
          "vendor": "Example",
          "name": "An Example Tool",
          "admin_nickname": "A Great LTI Tool",
          "configuration": {
            "title": "Sample Tool",
            "description": "A sample LTI tool",
            "target_link_uri": "https://example.com/launch",
            "oidc_initiation_url": "https://example.com/oidc",
            "redirect_uris": ["https://example.com/redirect"],
            "scopes": ["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"],
            "placements": [
              {
                "placement": "course_navigation",
                "enabled": true
              }
            ],
            "launch_settings": {}
          }
        }'
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Reset an LTI Registration to Defaults](#method.lti/registrations.reset) [Lti::RegistrationsController#reset](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### PUT /api/v1/accounts/:account\_id/lti\_registrations/:id/reset

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/lti_registrations/:id/reset`

Reset the specified LTI registration to its default settings in this context. This removes all customizations that were present in the overlay associated with this context.

#### Example Request:

#### 

```
This would reset the specified LTI registration to its default settings
curl -X PUT 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/<registration_id>/reset' \
     -H "Authorization: Bearer <token>"
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Delete an LTI Registration](#method.lti/registrations.destroy) [Lti::RegistrationsController#destroy](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### DELETE /api/v1/accounts/:account\_id/lti\_registrations/:id

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/lti_registrations/:id`

Remove the specified LTI registration

#### Example Request:

#### 

```
This would delete the specified LTI registration
curl -X DELETE 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/<registration_id>' \
     -H "Authorization: Bearer <token>"
```

Returns a
[Lti::Registration](lti_registrations.html#Lti::Registration)
object

## [Bind an LTI Registration to an Account](#method.lti/registrations.bind) [Lti::RegistrationsController#bind](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### POST /api/v1/accounts/:account\_id/lti\_registrations/:id/bind

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/lti_registrations/:id/bind`

Enable or disable the specified LTI registration for the specified account. To enable an inherited registration (eg from Site Admin), pass the registrationâs global ID.

Only allowed for root accounts.

**Specifics for Site Admin:** âonâ enables and locks the registration on for all root accounts. âoffâ disables and hides the registration for all root accounts. âallowâ makes the registration visible to all root accounts, but accounts must bind it to use it.

**Specifics for centrally-managed/federated consortia:** Child root accounts may only bind registrations created in the same account. For parent root account, binding also applies to all child root accounts.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| workflow\_state | Required | string | The desired state for this registration/account binding. âallowâ is only valid for Site Admin registrations.  Allowed values: `on`, `off`, `allow` |

#### Example Request:

#### 

```
This would enable the specified LTI registration for the specified account
curl -X POST 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/<registration_id>/bind' \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"workflow_state": "on"}'
```

## [Search for Accounts and Courses](#method.lti/registrations.context_search) [Lti::RegistrationsController#context\_search](https://github.com/instructure/canvas-lms/blob/master/app/controllers/lti/registrations_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/accounts/:account\_id/lti\_registrations/context\_search

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/lti_registrations/context_search`

This is a utility endpoint used by the Canvas Apps UI and may not serve general use cases.

Search for accounts and courses that match the search term on name, SIS id, or course code. Returns bare-bones data about each account and course. Used to populate the search dropdowns when managing LTI registration availability.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| by\_account\_id |  | string | If provided, only searches within this account. |
| search\_term |  | string | String to search for in account names, SIS ids, or course codes. |

#### Example Request:

#### 

```
This would search for accounts and courses matching the search term "example"
curl -X GET 'https://<canvas>/api/v1/accounts/<account_id>/lti_registrations/context_search?search_term=example' \
     -H "Authorization: Bearer <token>"
```

Returns a
[ContextSearchResponse](lti_registrations.html#ContextSearchResponse)
object