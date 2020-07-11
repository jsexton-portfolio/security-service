# Portfolio Security Service
![](https://github.com/jsexton-portfolio/security-service/workflows/build/badge.svg)

Service used to authenticate portfolio user base

## Endpoints
Base path: https://api.justinsexton.net/security

### POST /login

Authenticates a users credentials and responds with access tokens.

#### Request Body Schema:
```json
{
  "username": "(Required)",
  "password": "(Required)"
}
```

#### Example Successful Response:
```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "schemas": {}
    },
    "data": {
        "accessToken": "access token",
        "refreshToken": "(refresh token)",
        "idToken": "(id token)",
        "tokenType": "Bearer"
    }
}
```

#### Note
On first login if credentials are valid the response will be 200 OK but the data field will be null. 
This means the account needs to be confirmed before authenticating.

#### Example Failed Response:
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [
            {
                "description": "field required",
                "fieldName": "password"
            }
        ],
        "schemas": {
            "requestBody": {
                "title": "LoginForm",
                "type": "object",
                "properties": {
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "password": {
                        "title": "Password",
                        "type": "string"
                    }
                },
                "required": [
                    "username",
                    "password"
                ],
                "additionalProperties": false
            }
        }
    },
    "data": null
}
```

### POST /confirm-account

First time login will require the confirmation of the account and a password reset.

#### Request Body Schema:
```json
{
  "username": "(Required)",
  "oldPassword": "(Required)",
  "newPassword": "(Required - Cant equal old password)"
}
```

#### Example Successful Response:
```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "schemas": {}
    },
    "data": {
        "accessToken": "access token",
        "refreshToken": "(refresh token)",
        "idToken": "(id token)",
        "tokenType": "Bearer"
    }
}
```

#### Example Failed Response:
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [
            {
                "description": "field required",
                "fieldName": "oldPassword"
            }
        ],
        "schemas": {
            "requestBody": {
                "title": "PasswordUpdateForm",
                "type": "object",
                "properties": {
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "oldPassword": {
                        "title": "Oldpassword",
                        "type": "string"
                    },
                    "newPassword": {
                        "title": "Newpassword",
                        "type": "string"
                    }
                },
                "required": [
                    "username",
                    "oldPassword",
                    "newPassword"
                ],
                "additionalProperties": false
            }
        }
    },
    "data": null
}
```
