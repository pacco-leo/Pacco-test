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

            $("#id_elevation").val($scope.myData.fromServer.elevation)
            $("#id_latitude").val($scope.myData.fromServer.latitude)
            $("#id_longitude").val($scope.myData.fromServer.longitude)
            $("#id_utc").val($scope.myData.fromServer.utc)
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


} );


