This document contains a list of exposed endpoints and descriptions of what they do and how to interact with them. The 
base URL to hit up endpoints for our server is http://savory-backend.herokuapp.com. 

## (GET) /connect?token={facebook_token}

This endpoint is for logging in/creating an account to the Savory platform. If an account already exists under the 
token's Facebook account, a new account will not be created. In exchange for a Facebook token, this endpoint will 
exchange it for a JWT auth token that is used to access our platform.

Requires:
- `facebook_token (URL parameter)`: A Facebook access token retrieved from successfully logging into the Facebook platform.

Returns:
```
{
  'token': <String>. A JWT auth token that provides the client access to other endpoints of our platform
}
```

## (POST) /photo

This endpoint is for uploading photos to the Savory platform. It'll take in a photo, upload it to a S3 bucket, and 
returns a photo object containing information about the photo.

Requires:
- `Authorization (Header)`: A JWT auth token that originated from our backend
- `Content-Type (Header)`: Should be set to `multipart/form-data`
- `image (Body, form-data)`: An image to be posted to the Savory platform

Returns:
```
{
    "id": <Integer>. The id of the photo
    "account_id": <Integer>. The id of the account that posted it
    "photo_url": <String>. The url of the uploaded image
    "creation_date": <Long>. The upload date in epoch time
}
```

## (GET) /account/me

This endpoint is for getting the profile of the token's owner. By exposing this endpoint, this means that the client 
won't need to maintain the account's id as well, and can rely purely on the token to get information.

Requires:
-`Authorization (Header)`: A JWT auth token from the Savory platform

Returns:
```
{
    "account": {
        "id": <Integer> The id of the account
        "first_name": <String> The first name of the account's owner
        "last_name": <String> The last name of the account's owner'
        "profile_image": <String> The account's profile picture,
        "creation_date": <Long>. The account's creation date in epoch time
    },
    "photos": [
        {
            "id": <Integer> The id of the photo
            "account_id": <Integer> The id of the account that posted it
            "photo_url": <String> The url of the photo
            "creation_date": <Long> The upload time in epoch time
        },
        ...
    ]
}
```

## (GET) /account/me/photos?last_id={<photo_id>}

This endpoint is getting a page of 15 photos the token's owner has uploaded after a given photo (last_id represents the 
id of this photo). If last_id is not passed in, the 15 most recently uploaded photos will be returned.

Requires:
- `Authorization (Header)`: A JWT auth token that originated from our backend
- `last_id (URL parameter)`: The id of the photo to fetch relative to.

Returns:
```
[
    {
        "id": <Integer> The id of the photo
        "account_id": <Integer> The id of the account that posted it
        "photo_url": <String> The url of the photo
        "creation_date": <Long> The upload time in epoch time
    },
    ...
]
```