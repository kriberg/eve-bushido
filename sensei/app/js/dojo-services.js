(function () {
    'use strict';

    function Dojo($http) {
        var service = {};

        service.Capsuler = {
            get: function () {
                return $http.get('/dojo/capsuler/');
            }
        };

        service.Location = {
            get: function () {
                return $http.get('/dojo/location/');
            }
        };


        return service;
    }

    angular.
        module('dojoServices', []).
        factory('Dojo', ['$http', Dojo]);
})();
