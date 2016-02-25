from django.conf import settings
from django.core.cache import cache
import pycrest
from datetime import datetime


def get_crest_connection():
    return pycrest.EVE(client_id=settings.CREST_CLIENTID,
                       api_key=settings.CREST_SECRET_KEY,
                       redirect_uri=settings.CREST_CALLBACK_URL)


def store_connection(username, connection):
    timeout = (datetime.utcfromtimestamp(connection.expires) -
               datetime.now()).total_seconds()

    cache.set('{}.conndata'.format(username), {
        'access_token': connection.token,
        'refresh_token': connection.refresh_token,
        'expires_in': timeout,
        'expires': connection.expires
    }, timeout)
