var ktControllers = angular.module('ktControllers', []);

ktControllers.controller('MainController', function($rootScope) {
  $rootScope.$on('event:auth-loginRequired', function() {
    console.log("! login required");
    $state.go('login');
  });
  $rootScope.$on('event:auth-loginConfirmed', function() {
    console.log("login confirmed");
    $state.go('master.popular');
  });
});

ktControllers.controller('SubmitAnswerController', function($scope, QuestionFactory) {

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

ktControllers.controller('BrowsePopularController', function($scope, QuestionFactory) {

  /*var questions = QuestionFactory.get(function(data) {
  $scope.questions = data.questions;
  });*/

  $scope.question = QuestionFactory.get();

  /*var questions = QuestionFactory.get(function(data) {
  console.log(data);
  });*/

});

