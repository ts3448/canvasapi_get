# Sandboxes

# Sandboxes API



**LTI Sandboxes API (Must use [JWT access tokens](jwt_access_tokens.html) with this API).**

Sandboxes are how Canvas creates a new environment based on a template. As part of
creating the new sandbox, all UUIDs are remapped to new values. To avoid confusion
with the original template. This API allows you to download the UUID mapping for
a given sandbox.

## [Download UUID Mapping for this Sandbox](#method.lti/sandbox.uuid_map)

### GET /api/lti/uuid\_map

**Scope:** 
`url:GET|/api/lti/uuid_map`

This endpoint returns a CSV file with the UUID mapping for the sandbox. The CSV has three columns:

```
* `type` - The object type
* `original_uuid` - The UUID of an object from the template
* `new_uuid` - The UUID of the corresponding object in the sandbox

```