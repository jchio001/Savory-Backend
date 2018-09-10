This document contains a list of exposed endpoints and descriptions of what they do and how to interact with them. The 
base URL to hit up endpoints for our server is http://savory-backend.herokuapp.com. 

## (GET) /connect?token={facebook_token}

This endpoint is for logging in/creating an user to the Savory platform. If an user already exists under the 
token's Facebook user, a new user will not be created. In exchange for a Facebook token, this endpoint will 
exchange it for a JWT auth token that is used to access our platform.

Requires:
- `facebook_token (URL parameter)`: A Facebook access token retrieved from successfully logging into the Facebook platform.

Returns:
```
{
  'token': <String>. A JWT auth token that provides the client access to other endpoints of our platform
}
```

## (GET) /token

This endpoint is for exchanging a JWT auth token from our platform for a newer one.

Requires:
- `Authorization (Header)`: A JWT auth token that originated from our backend

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
- `yelp_id (Body, form_data)`: The Yelp id of the restaurant the photo is attached to. This will be validated 
server-sided.

Returns:
```
{
    "id": <Integer>. The id of the photo
    "user_id": <Integer>. The id of the user that posted it
    "photo_url": <String>. The url of the uploaded image
    "yelp_id": <String>. The Yelp id of the restaurant this photo maps to
    "restaurant_name": <String>. The name of the restaurant this photo maps to
    "creation_date": <Long>. The upload date in epoch time
}
```

## (GET) /user/me

This endpoint is for getting the profile of the token's owner. By exposing this endpoint, this means that the client 
won't need to maintain the user's id as well, and can rely purely on the token to get information.

Requires:
-`Authorization (Header)`: A JWT auth token from the Savory platform

Returns:
```
{
    "user": {
        "id": <Integer> The id of the user
        "first_name": <String> The first name of the user's owner
        "last_name": <String> The last name of the user's owner'
        "profile_image": <String> The user's profile picture,
        "creation_date": <Long>. The user's creation date in epoch time
    },
    "photos": [
        {
            "id": <Integer> The id of the photo
            "user_id": <Integer> The id of the user that posted it
            "photo_url": <String> The url of the photo
            "yelp_id": <String>. The Yelp id of the restaurant this photo maps to
            "restaurant_name": <String>. The name of the restaurant this photo maps to
            "creation_date": <Long> The upload time in epoch time
        },
        ...
    ]
}
```

## (GET) /user/me/following

This endpoint retrieves the users the token's owner is currently following.

Requires:
-`Authorization (Header)`: A JWT auth token from the Savory platform

Returns:
```
[
    "user": {
        "id": <Integer> The id of the user
        "first_name": <String> The first name of the user's owner
        "last_name": <String> The last name of the user's owner'
        "profile_image": <String> The user's profile picture,
        "creation_date": <Long>. The user's creation date in epoch time
    },
    ...
]
```

## (GET) /user/me/photos?last_id={<photo_id>}

This endpoint is getting a page of 15 photos the token's owner has uploaded with ids less than last_Id. If last_id is 
not passed in, the 15 most recently uploaded photos will be returned.

Requires:
- `Authorization (Header)`: A JWT auth token that originated from our backend
- `last_id (URL parameter)`: The id of the photo to fetch relative to.

Returns:
```
[
    {
        "id": <Integer> The id of the photo
        "user_id": <Integer> The id of the user that posted it
        "photo_url": <String> The url of the photo
        "yelp_id": <String>. The Yelp id of the restaurant this photo maps to
        "restaurant_name": <String>. The name of the restaurant this photo maps to
        "creation_date": <Long> The upload time in epoch time
    },
    ...
]
```

## (GET) /following/photos

This endpoint is for retrieving a page of 10 photos for the user's feed. Photos are fetched from all users an
user is following (this includes the user in question as well!). If last_id is not passed in, the 10 most 
recently uploaded photos are returned. Else, the 10 most recently uploaded photos with an id less than last_id will be 
returned.

Requires:
- `Authorization (Header)`: A JWT auth token that originated from our backend
- `last_id (URL parameter)`: The id of the photo to fetch relative to.

Returns:
```
[
    {
        "id": <Integer> The id of the photo
        "user_id": <Integer> The id of the user that posted it
        "photo_url": <String> The url of the photo
        "yelp_id": <String>. The Yelp id of the restaurant this photo maps to
        "restaurant_name": <String>. The name of the restaurant this photo maps to
        "creation_date": <Long> The upload time in epoch time
    },
    ...
]
```