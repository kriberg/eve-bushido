from .models import Capsuler
import logging
from datetime import datetime
from dojo.crest import get_crest_connection, store_connection

from django.core.cache import cache

log = logging.getLogger(__name__)


class CrestAuthenticationBackend(object):

    def get_user(self, user_id):
        try:
            return Capsuler.objects.get(pk=user_id)
        except Capsuler.DoesNotExist:
            return None

    def authenticate(self, token=None):
        if not token:
            return None

        try:
            eve = get_crest_connection()
            crest_con = eve.authorize(token)
            userdata = crest_con.whoami()
            log.debug('{} logged in, username {}.'.format(userdata['CharacterName'],
                                                          userdata['CharacterOwnerHash']))
        except:
            log.error('Could not authenticate with CREST.')
            return None

        capsuler, created = Capsuler.objects.get_or_create(username=userdata['CharacterOwnerHash'],
                                                           character_name=userdata['CharacterName'])
        if created:
            log.info('Created user "{}" for character "{}".'.format(
                capsuler.username,
                capsuler.character_name
            ))

        timeout = (datetime.utcfromtimestamp(crest_con.expires) -
                   datetime.now()).total_seconds()

        cache.set('{}.userdata'.format(capsuler.username), userdata, timeout)
        store_connection(capsuler.username, crest_con)

        return capsuler
