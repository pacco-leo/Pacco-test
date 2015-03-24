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
        $('#waitingscreen').fadeIn();
        responsePromise.success(function(data, status, headers, config) {
            $scope.myData.fromServer = data;
            $("#id_elevation").val($scope.myData.fromServer.elevation);
            $("#id_latitude").val($scope.myData.fromServer.latitude);
            $("#id_longitude").val($scope.myData.fromServer.longitude);
            $("#id_utc").val($scope.myData.fromServer.utc);
            $('#waitingscreen').fadeOut();
        });
        responsePromise.error(function(data, status, headers, config) {
            $('#waitingscreen').fadeOut();
            alert("AJAX failed!");

        });

    }


});

paccoApp.controller("ProbeController", function($scope, $http) {

    $scope.myData = {};
    $scope.myData.doClick = function(item, event, probeChannel) {
        $('#waitingscreen').fadeIn();



        var responsePromise = $http.get(probeChannel+"/probeMeasure");
        //Something like: http://127.0.0.1:8000/paccotest/probesForm/ph/probeMeasure
        responsePromise.success(function(data, status, headers, config) {
            $scope.myData.fromServer = data;
            //$("#id_measure").val($scope.myData.fromServer)
            $("#resume_result_"+probeChannel).text($scope.myData.fromServer);
            $('#waitingscreen').fadeOut();
            $('.btnA').animate({fontSize:'20px',width:'30%',height:'40px',paddingTop:'20px',left:0,bottom:'50px'});
            $('.btnB').animate({});
            $('.btnC').animate({left:'31%',width:'68%',bottom:'30px'});
                        $('.consigne').css({display:'none'});
        });
        responsePromise.error(function(data, status, headers, config) {
            $('#waitingscreen').fadeOut();
            alert("AJAX failed!");
        });
    }


} );

paccoApp.controller("TabController",function($scope){
	this.tab = 1;
	this.backToResume = false;
	this.lastTab = parseInt($('#lastTabValue').val());
	this.setTab = function(newValue){
		this.tab = newValue;
	};
	this.setTabResume = function(newValue){
		this.tab = newValue;
		this.backToResume = true;
        $('.btnA').css({fontSize:'20px',width:'30%',height:'40px',paddingTop:'20px',left:0,bottom:'50px'});
	};
	this.nextTab = function(newValue,answer){
        $('.btnA').css({fontSize:'45px',width:'49%',height:'170px',paddingTop:'130px',left:'50%',bottom:'15px'});
        $('.btnB').css({});
        $('.btnC').css({left:'50%',width:'50%'});
        $('.consigne').css({display:'block'});
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
});


paccoApp.controller("UploadToServerController", function($scope, $http) {

    $scope.uploadAnswser = {};
    $scope.shutdownAnswer = {};
    $scope.myData = {};

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

    $scope.myData.doPrint = function(item, event) {
        var responsePromise = $http.get("doPrint");
        //Something like: http://127.0.0.1:8000/paccotest/doPrint

    }

});