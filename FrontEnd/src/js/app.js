var app = angular.module('app', ['ngResource', 'ngAnimate', 'ngSanitize',
                                 'ktStates', 'ktControllers']);

/* CONFIG */

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

app.controller('SubmitAnswerController', function($scope, QuestionFactory) {

  var answertest = {
    "id": 2,
    "content": "Uuskommenti asglkjgsdlakjgs",
    "user_id": 125,
    "username": "Zorro",
    "votes_up": 12,
    "votes_down": 0,
    "date": "2014-01-02T14:00:00.000Z"
  }

  $scope.send = function() {
    console.log("User: ", $scope.user.name, "Message: ", $scope.message);
    $scope.question.answers.push(answertest);
  };
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

