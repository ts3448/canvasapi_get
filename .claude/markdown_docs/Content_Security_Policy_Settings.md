# Content Security Policy Settings

# Content Security Policy Settings API

### BETA: This API resource is not finalized, and there could be breaking changes before its final release.



API for enabling/disabling the use of Content Security Policy headers and
configuring allowed domains

## [Get current settings for account or course](#method.csp_settings.get_csp_settings) [CspSettingsController#get\_csp\_settings](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### GET /api/v1/courses/:course\_id/csp\_settings

**Scope:** 
`url:GET|/api/v1/courses/:course_id/csp_settings`

### GET /api/v1/accounts/:account\_id/csp\_settings

**Scope:** 
`url:GET|/api/v1/accounts/:account_id/csp_settings`

Update multiple modules in an account.

#### API response field:

* enabled

  Whether CSP is enabled.
* inherited

  Whether the current CSP settings are inherited from a parent account.
* settings\_locked

  Whether current CSP settings can be overridden by sub-accounts and courses.
* effective\_whitelist

  If enabled, lists the currently allowed domains (includes domains automatically allowed through external tools).
* tools\_whitelist

  (Account-only) Lists the automatically allowed domains with their respective external tools
* current\_account\_whitelist

  (Account-only) Lists the current list of domains explicitly allowed by this account. (Note: this list will not take effect unless CSP is explicitly enabled on this account)

## [Enable, disable, or clear explicit CSP setting](#method.csp_settings.set_csp_setting) [CspSettingsController#set\_csp\_setting](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### PUT /api/v1/courses/:course\_id/csp\_settings

**Scope:** 
`url:PUT|/api/v1/courses/:course_id/csp_settings`

### PUT /api/v1/accounts/:account\_id/csp\_settings

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/csp_settings`

Either explicitly sets CSP to be on or off for courses and sub-accounts, or clear the explicit settings to default to those set by a parent account

Note: If âinheritedâ and âsettings\_lockedâ are both true for this account or course, then the CSP setting cannot be modified.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| status | Required | string | If set to âenabledâ for an account, CSP will be enabled for all its courses and sub-accounts (that have not explicitly enabled or disabled it), using the allowed domains set on this account. If set to âdisabledâ, CSP will be disabled for this account or course and for all sub-accounts that have not explicitly re-enabled it. If set to âinheritedâ, this account or course will reset to the default state where CSP settings are inherited from the first parent account to have them explicitly set.  Allowed values: `enabled`, `disabled`, `inherited` |

## [Lock or unlock current CSP settings for sub-accounts and courses](#method.csp_settings.set_csp_lock) [CspSettingsController#set\_csp\_lock](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### PUT /api/v1/accounts/:account\_id/csp\_settings/lock

**Scope:** 
`url:PUT|/api/v1/accounts/:account_id/csp_settings/lock`

Can only be set if CSP is explicitly enabled or disabled on this account (i.e. âinheritedâ is false).

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| settings\_locked | Required | boolean | Whether sub-accounts and courses will be prevented from overriding settings inherited from this account. |

## [Add an allowed domain to account](#method.csp_settings.add_domain) [CspSettingsController#add\_domain](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### POST /api/v1/accounts/:account\_id/csp\_settings/domains

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/csp_settings/domains`

Adds an allowed domain for the current account. Note: this will not take effect unless CSP is explicitly enabled on this account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| domain | Required | string | no description |

## [Add multiple allowed domains to an account](#method.csp_settings.add_multiple_domains) [CspSettingsController#add\_multiple\_domains](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### POST /api/v1/accounts/:account\_id/csp\_settings/domains/batch\_create

**Scope:** 
`url:POST|/api/v1/accounts/:account_id/csp_settings/domains/batch_create`

Adds multiple allowed domains for the current account. Note: this will not take effect unless CSP is explicitly enabled on this account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| domains | Required | Array | no description |

## [Remove a domain from account](#method.csp_settings.remove_domain) [CspSettingsController#remove\_domain](https://github.com/instructure/canvas-lms/blob/master/app/controllers/csp_settings_controller.rb)

### BETA: This API endpoint is not finalized, and there could be breaking changes before its final release.

### DELETE /api/v1/accounts/:account\_id/csp\_settings/domains

**Scope:** 
`url:DELETE|/api/v1/accounts/:account_id/csp_settings/domains`

Removes an allowed domain from the current account.

#### Request Parameters:

| Parameter |  | Type | Description |
| --- | --- | --- | --- |
| domain | Required | string | no description |