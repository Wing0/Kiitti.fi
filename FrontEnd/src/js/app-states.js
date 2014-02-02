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
      controller: function($location, AuthAPI) {
        console.log("test");
        AuthAPI.logout()
        .success(function() {
          console.log("logout");
          $location.path('/');
        })
        .error(function(data, status) {
          console.log("data", data);
          console.log("status", status);
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


