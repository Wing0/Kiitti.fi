var app = angular.module('app', ['ngResource', 'ngAnimate', 'ngSanitize',
                                 'textAngular',
                                 'ktStates', 'ktAuth', 'ktControllers', 'ktAPI']);

/* CONFIG */

app.constant("APIUrl", 'http://0.0.0.0:8000');

app.config(function($locationProvider, $httpProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

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

app.run(function($rootScope, AuthAPI) {
  AuthAPI.load().success(function(data) {
    $rootScope.user = data.user;
  });
})

/* RESOURCES */

app.factory('QuestionFactory', function($resource, APIUrl) {
  //return $resource('/testdata/single_question.json', {},
  return $resource(APIUrl + '/questions', {},
    { 'get': {method: 'GET', isArray: false} });
});

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

