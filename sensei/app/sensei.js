(function () {
    'use strict';

    function Configuration($stateProvider, $httpProvider, $urlRouterProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('login', {
                url: '/',
                views: {
                    'top_content': {
                        templateUrl: 'partials/login.html',
                        controller: 'LoginController'
                    }
                }
            })
            .state('banned', {
                url: '/banned',
                views: {
                    'top_content': {
                        templateUrl: 'partials/banned.html'
                    }
                }
            })
            .state('dojo', {
                url: '/dojo',
                views: {
                    'top_content': {
                        templateUrl: 'partials/dojo.html',
                        controller: 'DojoController'
                    }
                }
            })

        ;

    }

    return angular
        .module('senseiApp', [
            'ngRoute',
            'ui.router',
            'ui.bootstrap',
            'ngResource',
            'loginControllers',
            'dojoControllers',
            'dojoServices'
        ])
        .config(['$stateProvider', '$httpProvider', '$urlRouterProvider', Configuration])
        .config(function ($resourceProvider) {
            $resourceProvider.defaults.stripTrailingSlashes = false;
        })
        .run(function ($rootScope) {
            $rootScope.userLoggedIn = false;
        })
})();
