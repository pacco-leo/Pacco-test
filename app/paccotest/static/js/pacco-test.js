$(document).ready( function() {


});


var paccoApp = angular.module('paccoApp', ['ngAnimate']);

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


});

paccoApp.controller("ProbeController", function($scope, $http) {

    $scope.myData = {};
    $scope.myData.doClick = function(item, event, probeChannel) {
        var responsePromise = $http.get(probeChannel+"/probeMeasure");
        //Something like: http://127.0.0.1:8000/paccotest/probesForm/ph/probeMeasure
        responsePromise.success(function(data, status, headers, config) {
            $scope.myData.fromServer = data;
            //$("#id_measure").val($scope.myData.fromServer)
            $("#resume_result_"+probeChannel).text($scope.myData.fromServer);
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


} );

paccoApp.controller("TabController",function($scope){
	this.tab = 1;
	this.backToResume = false;
	this.hideResult = false;
	this.lastTab = parseInt($('#lastTabValue').val());
	this.setTab = function(newValue){
		this.tab = newValue;
	};
	this.setTabResume = function(newValue){
		this.tab = newValue;
		this.backToResume = true;
	    this.hideResult = true;
	};
	this.nextTab = function(newValue,answer){
	    $('.resumeAnswer_'+newValue).css('display','none');
	    $('#resumeAnswer_'+newValue+'_'+answer).css('display','inline');
        if(this.backToResume)
	    {
		    this.tab = this.lastTab;
	    }
        else
	    {
		    this.tab = newValue + 1;
	    }
	    
	};
	this.isSet = function(tabNum){
		return this.tab === tabNum;
	};
	this.hideresult = function(){
	    this.hideResult = false;
	};
});


paccoApp.controller("UploadToServerController", function($scope, $http) {

    $scope.uploadAnswser = {};
    $scope.shutdownAnswer = {};

    $scope.uploadAnswser.doUploadClick = function(item, event) {
        var responsePromise = $http.get("uploadToServerClick");
         //Something like: http://127.0.0.1:8000/paccotest/uploadToServer/uploadToServerClick

        responsePromise.success(function(data, status, headers, config) {
            $scope.uploadAnswser.fromServer = data;
            $("#uploadCountLeft").val($scope.uploadAnswser.fromServer.uploadCountLeft)
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }

    $scope.shutdownAnswer.doShutdownClick = function(item, event) {
        var responsePromise = $http.get("doShutdown");
         //Something like: http://127.0.0.1:8000/paccotest/uploadToServer/doShutdown

        responsePromise.success(function(data, status, headers, config) {
            $scope.shutdownAnswer.fromServer = data;
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


});

paccoApp.controller("CompleteController", function($scope, $http) {

    $scope.shutdownAnswer = {};

    $scope.shutdownAnswer.doShutdownClick = function(item, event) {
        var responsePromise = $http.get("doShutdown");
         //Something like: http://127.0.0.1:8000/paccotest/uploadToServer/doShutdown

        responsePromise.success(function(data, status, headers, config) {
            $scope.shutdownAnswer.fromServer = data;
        });
        responsePromise.error(function(data, status, headers, config) {
            alert("AJAX failed!");
        });
    }


});