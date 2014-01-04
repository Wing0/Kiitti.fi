var app = angular.module('app', ['ngResource', 'ngRoute', 'ngAnimate']);

/* CONFIG */

app.config(function($routeProvider, $locationProvider) {

  $routeProvider
    .when('/', {
      templateUrl: 'templates/frontPage.html',
      controller: 'FrontPageController'
    })
    .otherwise({redirectTo : '/'});

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

});

/* CONTROLLERS */

app.controller('FrontPageController', function($scope) {

});
