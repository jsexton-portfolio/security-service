import copy
from typing import Dict, Any, Type

import pyocle
import pytest
from pydantic import BaseModel, ValidationError

from chalicelib.form import LoginForm, PasswordUpdateForm, RefreshTokenForm


@pytest.fixture
def login_form() -> Dict[str, Any]:
    valid_form = {
        'username': 'username',
        'password': 'Password1.'
    }

    return copy.deepcopy(valid_form)


@pytest.fixture
def password_update_form() -> Dict[str, Any]:
    valid_form = {
        'username': 'username',
        'oldPassword': 'oldPassword',
        'newPassword': 'Password1.'
    }

    return copy.deepcopy(valid_form)


@pytest.fixture
def refresh_token_form() -> Dict[str, Any]:
    valid_form = {
        'refreshToken': 'refreshToken'
    }

    return copy.deepcopy(valid_form)


@pytest.fixture
def get_fixture(request):
    def _get_fixture_by_name(name):
        return request.getfixturevalue(name)

    return _get_fixture_by_name


@pytest.fixture
def empty_username_login_form(login_form):
    login_form['username'] = None
    return login_form


@pytest.fixture
def empty_password_login_form(login_form):
    login_form['password'] = None
    return login_form


@pytest.fixture
def empty_username_and_password_login_form(login_form):
    login_form['username'] = None
    login_form['password'] = None
    return login_form


@pytest.fixture
def extra_field_login_form(login_form):
    login_form['extra'] = 'extra'
    return login_form


@pytest.fixture
def empty_username_password_update_form(password_update_form):
    password_update_form['username'] = None
    return password_update_form


@pytest.fixture
def empty_old_password_password_update_form(password_update_form):
    password_update_form['oldPassword'] = None
    return password_update_form


@pytest.fixture
def empty_new_password_password_update_form(password_update_form):
    password_update_form['newPassword'] = None
    return password_update_form


@pytest.fixture
def empty_username_and_passwords_password_update_form(password_update_form):
    password_update_form['username'] = None
    password_update_form['oldPassword'] = None
    password_update_form['newPassword'] = None
    return password_update_form


@pytest.fixture
def new_password_equals_old_password_password_update_form(password_update_form):
    password_update_form['newPassword'] = 'oldPassword'
    return password_update_form


@pytest.fixture
def extra_field_password_update_form(password_update_form):
    password_update_form['extra'] = 'extra'
    return password_update_form


@pytest.fixture
def empty_token_refresh_token_form(refresh_token_form):
    refresh_token_form['refreshToken'] = None
    return refresh_token_form


# See https://docs.pytest.org/en/latest/proposals/parametrize_with_fixtures.html
# See https://github.com/pytest-dev/pytest/issues/349
@pytest.mark.parametrize('fixture_name,error_count', [
    pytest.param('empty_username_login_form', 1),
    pytest.param('empty_password_login_form', 1),
    pytest.param('empty_username_and_password_login_form', 2),
    pytest.param('extra_field_login_form', 1),

    pytest.param('empty_username_password_update_form', 1),
    pytest.param('empty_old_password_password_update_form', 1),
    pytest.param('empty_new_password_password_update_form', 1),
    pytest.param('empty_username_and_passwords_password_update_form', 3),
    pytest.param('new_password_equals_old_password_password_update_form', 1),
    pytest.param('extra_field_password_update_form', 1),

    pytest.param('empty_token_refresh_token_form', 1)
])
def test_that_form_validation_rules_are_correctly_applied(get_fixture, fixture_name, error_count):
    form = get_fixture(fixture_name)

    with pytest.raises(pyocle.response.FormValidationError) as exception_info:
        # Retrieves the desired base model from the fixture name
        form_type = _get_form_type(fixture_name)
        pyocle.form.resolve_form(form, form_type)

    exception = exception_info.value
    assert exception.message == 'Form was not validated successfully'
    assert len(exception.errors) == error_count


def _get_form_type(fixture_name: str) -> Type[BaseModel]:
    """
    Determines which form type should be used based on the end of a given fixture name.
    Currently supports: login_form, password_update_form

    :param fixture_name: The fixture name that will be used to determine the form type.
    :return: The form type determined by the fixture name. Runtime error if the type could not be determined.
    """
    if fixture_name.endswith('login_form'):
        return LoginForm
    if fixture_name.endswith('password_update_form'):
        return PasswordUpdateForm
    if fixture_name.endswith('refresh_token_form'):
        return RefreshTokenForm

    raise RuntimeError(f'Form type could not be determined by fixture name: {fixture_name}')


@pytest.mark.parametrize('password,valid', [
    (None, False),
    ('', False),
    ('123', False),
    ('PASSWORD1.', False),
    ('Password1', False),
    ('password1', False),
    ('Password1.Password1.Password1.Password1.Password1.Password1.Password1.Password1.Password1.Password1.', False),

    ('Password1.', True),
    ('Passwo1.', True),
])
def test_password_policy_validation(password_update_form, password: str, valid: bool):
    password_update_form['newPassword'] = password

    if valid:
        PasswordUpdateForm(**password_update_form)
    else:
        with pytest.raises(ValidationError):
            PasswordUpdateForm(**password_update_form)
