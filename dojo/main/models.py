from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from datetime import datetime

import pytz, logging

from dojo.crest import get_crest_connection, store_connection

log = logging.getLogger('dojo')

class Capsuler(AbstractUser):
    character_name = models.CharField(max_length=255)
    settings = JSONField(blank=True, default={})
    banned = models.BooleanField(default=False)

    def _get_timeout(self, expires):
        return (datetime.fromtimestamp(expires, tz=pytz.UTC) -
                datetime.now(tz=pytz.UTC)).total_seconds()

    def get_character(self):
        character =  cache.get('{}.userdata'.format(self.username), None)
        if character is None:
            crest = self.get_crest()
            character = crest.whoami()
            cache.set('{}.userdata'.format(self.username),
                      character,
                      timeout=self._get_timeout(crest.expires))
        return character

    def get_crest(self):
        conn = cache.get('{}.conndata'.format(self.username), None)
        if conn is None:
            log.debug('{} crest conn has expired'.format(self.character_name))
            return None
        eve = get_crest_connection()
        expires_in = self._get_timeout(conn['expires'])
        crest = eve.temptoken_authorize(conn['access_token'],
                                        expires_in,
                                        conn['refresh_token'])

        if expires_in > 0 and expires_in < 180:
            log.debug('Refreshing token for {0}'.format(self.character_name))
            crest.refresh()
            store_connection(self.username, crest)

        return crest

    def get_location(self):
        crest = self.get_crest()
        character = self.get_character()
        location = crest.get('https://crest-tq.eveonline.com/characters/{0}/location/'.format(
            character['CharacterID']
        ))

        return location
