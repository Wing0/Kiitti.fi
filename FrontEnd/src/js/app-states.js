var ktStates = angular.module('ktStates', ['ui.router',
                                           'ktControllers', 'ktAPI']);

ktStates.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider
    .when('/', '/popular')
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
    .state('logout', {
      url: '/logout',
      controller: function($location, AuthAPI, $rootScope, $log) {
        AuthAPI.logout()
        .success(function() {
          $log.info("User " + $rootScope.user.username + " logged out");
          $rootScope.messages = "";
          $location.path('/login');
        })
        .error(function(data, status) {
          $log.error("User " + $rootScope.user.username + " could not be logged out")
        });
      }
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


