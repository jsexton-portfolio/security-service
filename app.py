from typing import Dict

import pyocle
from chalice import Chalice
from pycognito import Cognito

from chalicelib.error import error_handler
from chalicelib.form import LoginForm, PasswordUpdateForm

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


@app.route('/confirm', methods=['POST'], cors=True)
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