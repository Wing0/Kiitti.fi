var ktStates = angular.module('ktStates', ['ui.router',
                                           'ktControllers']);

ktStates.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider
    .when('/', '/login')
    .otherwise('/');

  var tdir = '../templates/';

  $stateProvider
    .state('login', {
      abstract: true,
      templateUrl: tdir + 'loginmaster.html',
      controller: 'LoginController',
      url: '/login'
    })
    .state('login.login', {
      url: '',
      templateUrl: tdir + 'loginmaster.login.html'
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


