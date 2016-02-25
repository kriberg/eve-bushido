(function () {
    'use strict';

    function DojoController($log, $scope, $rootScope, $interval, $state, Dojo) {
        var vm = this;
        $scope.userLoggedIn = $rootScope.userLoggedIn;
        $scope.selectedShip = {};
        $scope.enemyShips = {};
        $scope.shipClassCombinations = {
            'Rookie ships': ['t1'],
            'Frigate': ['t1', 't2', 'faction'],
            'Destroyer': ['t1', 't2', 't3'],
            'Industrial': ['t1', 't2'],
            'Cruiser': ['t1', 't2', 't3', 'faction'],
            'Battlecruiser': ['t1', 't2'],
            'Battleship': ['t1', 't2', 'faction']
        };

        $scope.getCapsuler = function () {
            Dojo.Capsuler.get().then(
                function (capsuler) {
                    $log.debug('Fetched capsuler', capsuler.data);
                    $scope.capsuler = capsuler.data;
                    $rootScope.userLoggedIn = true;
                },
                function (error) {
                    $rootScope.userLoggedIn = false;
                    $log.debug('Logging user out');
                    $interval.cancel(vm.capsulerTimer);
                    $interval.cancel(vm.locationTimer);
                    $state.go('login');
                });
        };

        $scope.getLocation = function () {
            Dojo.Location.get().then(
                function (location) {
                    if(!location.data.hasOwnProperty('solarSystem')) {
                        $scope.online = false;
                    } else {
                        $scope.online = true;
                        $scope.location = location.data;
                        $log.debug('Location:', location.data)
                    }
                },
                function (error) {
                    $scope.online = false;
                    $log.debug('Could not fetch location', error);
                });
        };

        $scope.getCapsuler();
        $scope.getLocation();
        vm.capsulerTimer = $interval($scope.getCapsuler, 120000); //Every two minutes
        vm.locationTimer = $interval($scope.getLocation, 30000); //Every 30 seconds

        $scope.findOpponent = function () {

        };
    }

    angular.module('dojoControllers', []).controller('DojoController', [
        '$log',
        '$scope',
        '$rootScope',
        '$interval',
        '$state',
        'Dojo',
        DojoController
    ]);
})();