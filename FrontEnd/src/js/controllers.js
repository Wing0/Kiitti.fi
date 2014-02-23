var module = angular.module('ktControllers', ['http-auth-interceptor', 'ktAPI']);

// master controller
module.controller('MainController', function($rootScope, $scope, AuthAPI, MessageFactory, $state) {

  /* Bind scope user to authenticated user */
  $scope.$watch(function() { return AuthAPI.user(); }, function(data) {
    $scope.user = data;
  }, true);

  /* Bind scope messages to message factory */
  $scope.$watch(function() { return MessageFactory.get(); }, function(data) {
    $scope.messages = data;
  }, true);

  /* Authentication handling */
  $rootScope.$on('event:auth-loginRequired', function() {
    console.log("! login required");
    $state.go('login.login');
  });
  $rootScope.$on('event:auth-loginConfirmed', function() {
    console.log("login confirmed");
    $state.go('master.popular');
  });
});

module.controller('LoginController', function(MessageFactory, AuthAPI, $scope, $location) {

  // check if user has already logged in and redirect
  AuthAPI.load().success(function() {
    $location.path('/');
  });

  $scope.login = function(user) {
    AuthAPI.login(user)
      .success(function(data, status, headers, config) {
        $location.path('/');
      })
      .error(function(data, status, headers, config) {
        MessageFactory.add("error", "Väärä käyttäjänimi ja/tai salasana.");
      });
    $scope.messages = MessageFactory.get();
  }
});

module.controller('LogoutController', function(AuthAPI, $log, $location, MessageFactory) {
  AuthAPI.logout()
    .success(function() {
      MessageFactory.clear()
      $location.path('/');
    })
    .error(function(data, status) {
      $log.error("User could not be logged out");
      $location.path('/');
    });
});

module.controller('SubmitAnswerController', function($scope, QuestionAPI) {

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

module.controller('CreateQuestionController', function($scope, QuestionAPI, $location) {
  $scope.send = function() {
    QuestionAPI.save($scope.question, function(data) {
      $location.path('/question/'+data.messageId);
    });
  }
});

module.controller('BrowseQuestionsController', function($scope, QuestionAPI) {
  $scope.data = QuestionAPI.get();
});

module.controller('SingleQuestionController', function($scope, data) {
  $scope.question = data;
});

module.controller('BrowsePopularController', function($scope, QuestionAPI, AnswerAPI) {

  //$scope.questions = AnswerAPI.get({"questionId": 1});

  /*var questions = QuestionAPI.get(function(data) {
  $scope.questions = data.questions;
  });*/

  $scope.question = QuestionAPI.get();

});

