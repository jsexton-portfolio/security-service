import pyocle
from botocore.exceptions import ClientError
from pycognito.exceptions import ForceChangePasswordException


def error_handler(decorated):
    """
    Wraps functions with error handling capabilities. Be sure to include this decoration after all other decorators.

    @app.route('/)
    @error_handler
    def route():
        # route logic that potentially raises errors
    :param decorated: The function implementation that will be extended with error handling
    :return: The decorated function wrapped with error handling capabilities
    """

    @pyocle.response.error_handler
    def wrapped_handler(*args, **kwargs):
        try:
            return decorated(*args, **kwargs)
        except ForceChangePasswordException:
            meta = pyocle.response.metadata(message='Update password before authenticating')
            return pyocle.response.response(200, meta=meta)
        except ClientError as ex:
            error = ex.response['Error']
            if error['Code'] == 'NotAuthorizedException':
                meta = pyocle.response.metadata(message=error['Message'])
                return pyocle.response.response(401, meta=meta)

            raise ex
        except Exception as ex:
            raise ex

    return wrapped_handler
