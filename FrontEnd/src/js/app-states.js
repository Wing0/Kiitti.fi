var ktStates = angular.module('ktStates', ['ui.router',
                                           'ktControllers']);

ktStates.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider
    .when('/', '/popular')
    .otherwise('/');

  var tdir = '../templates/';

  $stateProvider
    .state('login', {
      abstract: true,
      templateUrl: tdir + 'loginmaster.html',
      url: '/login'
    })
    .state('login.login', {
      url: '',
      templateUrl: tdir + 'loginmaster.login.html',
      controller: 'AuthController'
    })
    .state('login.forgot', {
      url: '/forgot',
      templateUrl: tdir + 'loginmaster.forgot.html'
    })

    .state('master', {
      abstract: true,
      templateUrl: tdir + 'master.html'
    })

    .state('master.popular', {
      url: '/popular',
      templateUrl: tdir + 'question.html',
      controller: 'BrowsePopularController'
    })
});


