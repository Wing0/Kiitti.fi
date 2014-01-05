var app = angular.module('app', ['ngResource', 'ngRoute', 'ngAnimate']);

/* CONFIG */

app.config(function($routeProvider, $locationProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  $routeProvider
    .when('/', {
      templateUrl: '../templates/question.html',
      controller: 'BrowsePopularController'
    })
    .when('/popular', {
      templateUrl: '../templates/question.html',
      controller: 'BrowsePopularController'
    })
    .when('/new', {
      templateUrl: '../templates/question.html',
      controller: 'BrowsePopularController'
    })
    .when('/interesting', {
      templateUrl: '../templates/question.html',
      controller: 'BrowsePopularController'
    })
    .when('/browse', {
      templateUrl: '../templates/question.html',
      controller: 'BrowsePopularController'
    })
    .otherwise({redirectTo : '/'});

});

/* RESOURCES */

app.factory('QuestionFactory', function($resource) {
  return $resource('/testdata/single_question.json', {},
    { 'get': {method: 'GET', isArray: false} });
});

/* CONTROLLERS */

app.controller('BrowsePopularController', function($scope, QuestionFactory) {

  /*var questions = QuestionFactory.get(function(data) {
    $scope.questions = data.questions;
  });*/

  $scope.question = QuestionFactory.get();

  /*var questions = QuestionFactory.get(function(data) {
    console.log(data);
  });*/

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

