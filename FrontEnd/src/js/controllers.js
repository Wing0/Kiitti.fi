var module = angular.module('ktControllers', ['http-auth-interceptor', 'ktAPI']);

// master controller
module.controller('MainController', function($rootScope, $scope, AuthAPI, MessageFactory, $state, $log) {

  /* Bind scope user to authenticated user */
  $scope.$watch(function() { return AuthAPI.user(); }, function(data) {
    $scope.user = data;
  }, true);

  /* Authentication handling */
  $rootScope.$on('event:auth-loginRequired', function() {
    $log.warn("Login required");
    $state.go('login.login');
  });
  $rootScope.$on('event:auth-loginConfirmed', function() {
    $log.success("Login confirmed");
    $state.go('master.popular');
  });
});

module.controller('LoginController', function(MessageFactory, AuthAPI, $scope, $location) {

  /* Check if user has already logged in and redirect */
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

module.controller('CreateQuestionController', function($scope, QuestionAPI, $location) {
  $scope.send = function() {
    QuestionAPI.save($scope.question, function(question) {
      $location.path('/question/'+question.rid);
    });
  }
});

module.controller('BrowseQuestionsController', function($scope, QuestionAPI) {
  $scope.data = QuestionAPI.get();
});

module.controller('SingleQuestionController', function($scope, question, AnswerAPI, MessageFactory) {

  $scope.question = question;
  $scope.answer = {"message": {}};
  $scope.submitMessage = {};

  $scope.submitAnswer = function() {
    $scope.answer.questionId = $scope.question.messageId;

    AnswerAPI.save($scope.answer, function(answer) {
      $scope.question.answers.push(answer);
      $scope.submitMessage.type = "success";
      $scope.submitMessage.content = "Vastaus lisätty onnistuneesti.";
      $scope.answer.content = "";
    }, function(response) {
      $scope.submitMessage.type = "error";
      $scope.submitMessage.content = "Vastauksen lisääminen ei onnistunut.";
      MessageFactory.addList(response.data.messages);
    });
  }
});

module.controller('BrowsePopularController', function($scope, QuestionAPI, AnswerAPI) {

});

