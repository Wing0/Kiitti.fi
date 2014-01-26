var app = angular.module('app', ['ngResource', 'ngAnimate', 'ngSanitize',
                                 'ktStates', 'ktAuth', 'ktControllers']);

/* CONFIG */

app.constant("APIUrl", 'http://0.0.0.0:7000/api/v1');

app.config(function($locationProvider, $httpProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

/* RESOURCES */

app.factory('QuestionFactory', function($resource) {
  return $resource('/testdata/single_question.json', {},
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

