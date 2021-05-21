import os
import requests


#Sandbox Client API Key: 1wkHxJTn17u8tYkuE5ZkAIRoYfk
#Sandbox User API Key: LxkAALygbip+1WP813mm7YfqfuM=
#Sandbox User Email: benjaminm@spotify.com


app_id = os.environ.get('client_api_key', None)
token = os.environ.get('user_api_key', None)



class APIKeyMissingError(Exception):
    pass

if client_api_key is None:
    raise APIKeyMissingError(
        "All methods require an API app id"
    )
elif user_api_key is None:
    raise APIKeyMissingError(
        "All methods require an API auth token."
    )


def rev_auth_str(client_api_key, user_api_key):
    """Returns a Rev Auth string."""
    return 'Rev %s:%s' % (client_api_key, user_api_key)

session = requests.Session()
session.headers['Authorization'] = rev_auth_str(client_api_key, user_api_key)


from .rev import inputs
from .rev import orders
from .rev import attachments
from .rev import single_order
