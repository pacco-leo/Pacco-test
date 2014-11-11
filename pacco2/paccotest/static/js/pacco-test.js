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
         //Something like: http://127.0.0.1:8000/paccotest/gpsPositionForm/gpsPosition

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

paccoApp.controller("ProbeController", function($scope, $http) {

    $scope.myData = {};

    $scope.myData.doClick = function(item, event) {
        var responsePromise = $http.get("probeMeasure");
        //Something like: http://127.0.0.1:8000/paccotest/probesForm/ph/probeMeasure

        responsePromise.success(function(data, status, headers, config) {
            $scope.myData.fromServer = data;

            $("#id_measure").val($scope.myData.fromServer)
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


} );

paccoApp.controller("TabController",function(){
	this.tab = 1;
	this.setTab = function(newValue){
		this.tab = newValue;
	};
	this.isSet = function(tabNum){
		return this.tab === tabNum;
	};
});

