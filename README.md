# Portfolio Security Service
![](https://github.com/jsexton-portfolio/security-service/workflows/build/badge.svg)

Service used for various security actions involving portfolio user base.

- [Endpoint Summary](#endpoint-summary)
- [Login](#login)
- [Logout](#logout)
- [Confirm Account](#confirm-account)
- [Refresh](#refresh)
- [Initiate Forgot Password](#initiate-forgot-password)
- [Confirm Forgot Password](#confirm-forgot-password)

## Endpoint Summary
Base path: https://api.justinsexton.net/security

- POST /login
- POST /confirm-account
- POST /refresh
- POST /init-forgot-password
- POST /confirm-forgot-password

## Login

Authenticates a users credentials and responds with access tokens.  

URL: https://api.justinsexton.net/security/login

### Request Body Schema:
```json
{
  "username": "(Required)",
  "password": "(Required)"
}
```

### Example Successful Response:
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

### Note
On first login if credentials are valid the response will be 200 OK but the data field will be null. 
This means the account needs to be confirmed before authenticating.

### Example Failed Response:
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

## Logout

When logging out, all tokens should be invalidated. Calling the logout endpoint with the tokens that need to
be invalidated will not allow requesters to continue using the tokens to authenticate requests.

URL: POST https://api.justinsexton.net/security/logout

### Request Body Schema:
```json
{
  "accessToken": "(Required)",
  "idToken": "(Required)",
  "refreshToken": "(Required)"
}
```

### Successful Response
```json
{
    "success": true,
    "meta": {
        "message": "User was successfully logged out",
        "errorDetails": [],
        "paginationDetails": {},
        "schemas": {}
    },
    "data": null
}
```

### Failed Response
```json
{
    "success": false,
    "meta": {
        "message": "Given inputs were incorrect. Consult the below details to address the issue.",
        "errorDetails": [
            {
                "description": "field required",
                "location": "idToken"
            },
            {
                "description": "field required",
                "location": "refreshToken"
            },
            {
                "description": "field required",
                "location": "accessToken"
            }
        ],
        "paginationDetails": {},
        "schemas": {
            "requestBody": {
                "title": "LogoutForm",
                "type": "object",
                "properties": {
                    "idToken": {
                        "title": "Idtoken",
                        "type": "string"
                    },
                    "refreshToken": {
                        "title": "Refreshtoken",
                        "type": "string"
                    },
                    "accessToken": {
                        "title": "Accesstoken",
                        "type": "string"
                    }
                },
                "required": [
                    "idToken",
                    "refreshToken",
                    "accessToken"
                ],
                "additionalProperties": false
            }
        }
    },
    "data": null
}
```

## Confirm Account

First time login will require the confirmation of the account and a password reset.  

URL: POST https://api.justinsexton.net/security/confirm-account

### Request Body Schema:
```json
{
  "username": "(Required)",
  "oldPassword": "(Required)",
  "newPassword": "(Required - Cant equal old password)"
}
```

### Example Successful Response:
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

### Example Failed Response:
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

## Refresh

When tokens expire, they will need to be renewed. This can be accomplish by re-authenticating with a
username and password. Or, by sending a refresh token. When re-authenticating with a refresh token this is the
endpoint to use.  

URL: POST https://api.justinsexton.net/security/refresh

### Request Body Schema:
```json
{
  "refreshToken": "(Required)"
}
```

### Example Successful Response:
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

### Example Failed Response:
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

## Initiate Forgot Password

When a password is forgot for a particular account, a reset code can be dispatched to the account's email.
The code can then be used to authorize a password reset.  

URL: POST https://api.justinsexton.net/security/init-forgot-password

### Request Body Schema:
```json
{
  "username": "(Required)"
}
```

### Successful Response
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

### Failed Response
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

## Confirm Forgot Password

Upon initiating a password reset with the `init-forgot-password` endpoint, once the confirmation code is retrieved,
it can be used to reset the accounts password.

URL: POST https://api.justinsexton.net/security/confirm-forgot-password

### Request Body Schema:
```json
{
  "username": "(Required)",
  "confirmationCode": "(Required)",
  "newPassword": "(Required)"
}
```

### Successful Response
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

### Failed Response
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