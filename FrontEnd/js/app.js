var app = angular.module('app', ['ngResource', 'ngRoute', 'ngAnimate']);

/* CONFIG */

app.config(function($routeProvider, $locationProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  $routeProvider
    .when('/', {
      templateUrl: '../templates/tab.html',
      controller: 'BrowsePopularController'
    })
    .when('/popular', {
      templateUrl: '../templates/tab.html',
      controller: 'BrowsePopularController'
    })
    .when('/new', {
      templateUrl: '../templates/tab.html',
      controller: 'BrowsePopularController'
    })
    .when('/interesting', {
      templateUrl: '../templates/tab.html',
      controller: 'BrowsePopularController'
    })
    .when('/browse', {
      templateUrl: '../templates/tab.html',
      controller: 'BrowsePopularController'
    })
    .otherwise({redirectTo : '/'});

});

/* RESOURCES */

app.factory('QuestionFactory', function($resource) {
  return $resource('/testdata/questions.json', {},
    { 'get': {method: 'GET', isArray: false} });
});

/* CONTROLLERS */

app.controller('BrowsePopularController', function($scope, QuestionFactory) {

  var questions = QuestionFactory.get(function(data) {
    $scope.questions = data.questions;
  });

});
