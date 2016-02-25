(function () {
    'use strict';

    function LoginController($log, $scope, $rootScope, $http) {
        $scope.clientID = Config.clientID;
        $scope.callbackURL = Config.callbackURL;
        $scope.userLoggedIn = $rootScope.userLoggedIn;
        $http.get('/dojo/capsuler/',
            function (capsuler) {
                $scope.capsuler = capsuler;
                $rootScope.userLoggedIn = true;
            },
            function (error) {
                $log.error(error);
                $rootScope.userLoggedIn = false;
            }
        )

    }

    angular.module('loginControllers', []).controller('LoginController', [
        '$log',
        '$scope',
        '$rootScope',
        '$http',
        LoginController
    ]);
})();