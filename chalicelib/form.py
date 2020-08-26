import re

from pydantic import BaseModel, Extra, validator, Field


class LoginForm(BaseModel):
    username: str
    password: str

    class Config:
        extra = Extra.forbid


class PasswordUpdateForm(BaseModel):
    username: str
    old_password: str
    new_password: str = Field(
        description=('Must conform to password policy.'
                     ' Passwords must contain at least one lower case,'
                     ' one uppercase, one digit and one special character'),
        min_length=8, max_length=99)

    @validator('new_password')
    def passwords_do_not_match(cls, value, values, **kwargs):
        old_password_exists = 'old_password' in values
        if old_password_exists and value == values['old_password']:
            raise ValueError('password cannot be the same as old password')

        return value

    @validator('new_password')
    def password_validator(cls, value):
        # Regex representing cognito's password policy
        # At least one lower case letter
        # At least one upper case letter
        # At least one digit
        # At least one special character
        # Minimum length of 8
        # Maximum length of 99
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\^$*.\[\]{}\(\)?\-“!@#%&/,><\’:;|_~`])\S{8,99}$')
        if not regex.match(value):
            raise ValueError('password does not conform to policy')

        return value

    class Config:
        extra = Extra.forbid
        fields = {
            'old_password': 'oldPassword',
            'new_password': 'newPassword'
        }


class RefreshTokenForm(BaseModel):
    refresh_token: str

    class Config:
        extra = Extra.forbid
        fields = {
            'refresh_token': 'refreshToken'
        }


class InitiateForgotPasswordForm(BaseModel):
    username: str

    class Config:
        extra = Extra.forbid


class ConfirmForgotPasswordForm(BaseModel):
    username: str
    new_password: str
    confirmation_code: str

    class Config:
        extra = Extra.forbid
        fields = {
            'new_password': 'newPassword',
            'confirmation_code': 'confirmationCode'
        }
