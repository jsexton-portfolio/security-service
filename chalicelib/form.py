from pydantic import BaseModel, Extra, validator


class LoginForm(BaseModel):
    username: str
    password: str

    class Config:
        extra = Extra.forbid


class PasswordUpdateForm(BaseModel):
    username: str
    old_password: str
    new_password: str

    @validator('new_password')
    def passwords_match(cls, v, values, **kwargs):
        if v == values['old_password']:
            raise ValueError('password cannot be the same as old password')

        return v

    class Config:
        extra = Extra.forbid
        fields = {
            'old_password': 'oldPassword',
            'new_password': 'newPassword'
        }
