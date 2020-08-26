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
        "paginationDetails": {},
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
        "paginationDetails": {},
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
        "paginationDetails": {},
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
        "paginationDetails": {},
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

### POST /refresh

#### Request Body Schema:
```json
{
  "refreshToken": "(Required)"
}
```

#### Example Successful Response:
```json
{
    "success": true,
    "meta": {
        "message": "Request completed successfully",
        "errorDetails": [],
        "paginationDetails": {},
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
                "fieldName": "refreshToken"
            }
        ],
        "paginationDetails": {},
        "schemas": {
            "requestBody": {
                "title": "RefreshTokenForm",
                "type": "object",
                "properties": {
                    "refreshToken": {
                        "title": "Refreshtoken",
                        "type": "string"
                    }
                },
                "required": [
                    "refreshToken"
                ]
            }
        }
    },
    "data": null
}
```

### POST /init-forgot-password
#### Successful Response
```json
{
    "success": true,
    "meta": {
        "message": "Email has been sent containing password reset confirmation code.",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": null
}
```

#### Failed Response
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [
            {
                "description": "field required",
                "location": "username"
            }
        ],
        "paginationDetails": {},
        "schemas": {
            "requestBody": {
                "title": "InitiateForgotPasswordForm",
                "type": "object",
                "properties": {
                    "username": {
                        "title": "Username",
                        "type": "string"
                    }
                },
                "required": [
                    "username"
                ],
                "additionalProperties": false
            }
        }
    },
    "data": null
}
```

### POST /confirm-forgot-password
#### Successful Response
```json
{
    "success": true,
    "meta": {
        "message": "Password has successfully been reset",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": null
}
```

#### Failed Response
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [
            {
                "description": "field required",
                "location": "confirmationCode"
            },
            {
                "description": "extra fields not permitted",
                "location": "t"
            }
        ],
        "paginationDetails": {},
        "schemas": {
            "requestBody": {
                "title": "ConfirmForgotPasswordForm",
                "type": "object",
                "properties": {
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "newPassword": {
                        "title": "Newpassword",
                        "type": "string"
                    },
                    "confirmationCode": {
                        "title": "Confirmationcode",
                        "type": "string"
                    }
                },
                "required": [
                    "username",
                    "newPassword",
                    "confirmationCode"
                ],
                "additionalProperties": false
            }
        }
    },
    "data": null
}
```