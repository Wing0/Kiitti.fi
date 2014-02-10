var app = angular.module('app', ['ngResource', 'ngAnimate', 'ngSanitize', 'ngCookies',
                                 'textAngular',
                                 'ktStates', 'ktControllers', 'ktAPI']);

/* CONFIG */

app.constant("APIUrl", 'http://127.0.0.1:8000');

app.config(function($locationProvider, $httpProvider, $cookiesProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  // $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  // $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  // $httpProvider.defaults.headers.common['X-CSRFToken'] = $cookiesProvider.csrftoken;

  // $httpProvider.defaults.withCredentials = true;

  // Messages interceptor
  $httpProvider.interceptors.push(function($rootScope, $q, httpBuffer) {
    return {
      'response': function(response) {
          if (response.data.messages) {
            $rootScope.messages = response.data.messages;
            angular.forEach($rootScope.messages, function(value, key) {
              value.type = "success";
            });
          }
          return response || $q.when(response); // default behaviour
        },
      'responseError': function(rejection) {
        if (rejection.data.messages) {
          $rootScope.messages = rejection.data.messages;
          angular.forEach($rootScope.messages, function(value, key) {
            value.type = "error";
          });
        }
        return $q.reject(rejection); // default behaviour
      }
    };
  });
});

app.run(function($rootScope, $cookieStore, $http, AuthAPI) {

  /* Get user if already logged in */
  if ($cookieStore.get('tursas')) {
    $http.defaults.headers.common['Authorization'] = 'Token ' + $cookieStore.get('tursas');
    AuthAPI.load().success(function(data) {
      $rootScope.user = data.user;
    });
  }
})


/* DIRECTIVES */

app.directive('qnaComment', function() {
  return {
    restrict: 'A',
    scope: {
      comment: '=comment'
    },
    templateUrl: '../templates/qna-comment.html',
    replace: true
  }
})

app.directive('qnaVotes', function() {
  return {
    restrict: 'A',
    scope: {
      votes_up: '=votesUp',
      votes_down: '=votesDown'
    },
    templateUrl: '../templates/qna-votes.html',
    replace: true
  }
})

