$(document).ready( function() {


});


var paccoApp = angular.module('paccoApp', []);

paccoApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

paccoApp.controller("PositionController", function($scope, $http) {
    $scope.myData = {};

    $scope.myData.doClick = function(item, event) {

        var responsePromise = $http.get("gpsPosition");

        responsePromise.success(function(data, status, headers, config) {
            $scope.myData.fromServer = data;
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


} );


