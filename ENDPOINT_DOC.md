This document contains a list of exposed endpoints and descriptions of what they do and how to interact with them. The 
base URL to hit up endpoints for our server is http://savory-backend.herokuapp.com. 

## /connect?token={facebook_token}

This endpoint is for logging in/creating an account to the Savory platform. If an account already exists under the 
token's Facebook account, a new account will not be created. In exchange for a Facebook token, this endpoint will 
exchange it for a JWT auth token that is used to access our platform.

Requires:
- `facebook_token`: A Facebook access token retrieved from successfully logging into the Facebook platform.

Returns:
```json
{
  'token': <String>. A JWT auth token that provides the client access to other endpoints of our platform.
}
```

