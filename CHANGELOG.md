# 0.4.0
- Added `POST /logout`

# 0.3.0
- Added `POST /init-forgot-password`
- Added `POST /confirm-forgot-password`
- Fixed bug that allowed consumers to call refresh token endpoint with unknown fields

# 0.2.1
- Migrated with Pyocle

# 0.2.0
- Added refresh endpoint

# 0.1.1
- Fixed bug that raised 500 internal server error when no `oldPassword` field was given when confirming an account.

# 0.1.0
- Added login route
- Added confirm account route
