from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

log = logging.getLogger('dojo')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        code = request.query_params.get('code', None)

        if code is None:
            return HttpResponseRedirect('/#/')

        capsuler = authenticate(token=code)
        login(request, capsuler)

        if capsuler is None:
            log.warning('Something tried logging in with code "{}".'.format(code))
            return HttpResponseRedirect('/#/')

        if capsuler.banned:
            log.info('Banned capsuler "{}" tried logging in.'.format(capsuler.character_name))
            return HttpResponseRedirect('/#/banned')

        log.info('Capsuler "{}" entered the dojo.'.format(capsuler.character_name))
        return HttpResponseRedirect('/#/dojo')


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/#/')


class CapsulerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        character = request.user.get_character()
        log.debug(character, 'checking in')
        return Response({
            'characterName': character['CharacterName'],
            'characterID': character['CharacterID']
        })


class LocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        location = request.user.get_location()
        log.debug(request.user.character_name, 'at', location)
        return Response(location)