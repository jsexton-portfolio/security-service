from typing import Dict

import pyocle
from chalice import Chalice
from pycognito import Cognito

from chalicelib.form import LoginForm, PasswordUpdateForm, RefreshTokenForm, InitiateForgotPasswordForm, \
    ConfirmForgotPasswordForm
from chalicelib.response import error_handler

app = Chalice(app_name='security-service')


@app.route('/login', methods=['POST'], cors=True)
@error_handler
def login():
    """
    Authenticates given credentials

    :return: Successful authenticated response
    """
    resolved_form = pyocle.form.resolve_form(app.current_request.raw_body, LoginForm)

    cognito = _client_from_env(username=resolved_form.username)
    cognito.authenticate(resolved_form.password)

    data = _token_response(cognito)
    return pyocle.response.ok(data)


@app.route('/confirm-account', methods=['POST'], cors=True)
@error_handler
def confirm():
    """
    Confirms a pending user and updates their temporary password

    :return: Successful authenticated response
    """
    resolved_form = pyocle.form.resolve_form(app.current_request.raw_body, PasswordUpdateForm)

    cognito = _client_from_env(username=resolved_form.username)
    cognito.new_password_challenge(resolved_form.old_password, resolved_form.new_password)

    data = _token_response(cognito)
    return pyocle.response.ok(data)


@app.route('/refresh', methods=['POST'], cors=True)
@error_handler
def refresh():
    resolved_form = pyocle.form.resolve_form(app.current_request.raw_body, RefreshTokenForm)

    cognito = _client_from_env(refresh_token=resolved_form.refresh_token)
    cognito.renew_access_token()

    data = _token_response(cognito)
    return pyocle.response.ok(data)


@app.route('/init-forgot-password', methods=['POST'], cors=True)
@error_handler
def initialize_forgot_password():
    resolved_form = pyocle.form.resolve_form(app.current_request.raw_body, InitiateForgotPasswordForm)

    cognito = _client_from_env(username=resolved_form.username)
    cognito.initiate_forgot_password()
    return pyocle.response.response(
        status_code=200,
        meta=pyocle.response.metadata('Email has been sent containing password reset confirmation code.')
    )


@app.route('/confirm-forgot-password', methods=['POST'], cors=True)
@error_handler
def confirm_forgot_password():
    resolved_form = pyocle.form.resolve_form(app.current_request.raw_body, ConfirmForgotPasswordForm)

    cognito = _client_from_env(username=resolved_form.username)
    cognito.confirm_forgot_password(
        confirmation_code=resolved_form.confirmation_code,
        password=resolved_form.new_password
    )
    return pyocle.response.response(
        status_code=200,
        meta=pyocle.response.metadata('Password has successfully been reset')
    )


def _token_response(cognito: Cognito) -> Dict[str, str]:
    """
    Constructs token response from authenticated cognito instance

    :param cognito:
    :return:
    """
    return {
        'accessToken': cognito.access_token,
        'refreshToken': cognito.refresh_token,
        'idToken': cognito.id_token,
        'tokenType': cognito.token_type
    }


def _client_from_env(**kwargs) -> Cognito:
    """
    Constructs cognito client from required environment variables and any other given attributes

    :param kwargs: Any configuration attributes for cognito client instance
    :return:
    """
    user_pool_id = pyocle.config.env_var('USER_POOL_ID')
    client_id = pyocle.config.encrypted_env_var('APP_CLIENT_ID')
    return Cognito(user_pool_id=user_pool_id, client_id=client_id, **kwargs)
