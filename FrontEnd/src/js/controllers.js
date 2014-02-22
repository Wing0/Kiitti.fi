var ktControllers = angular.module('ktControllers', ['http-auth-interceptor', 'ktAPI']);

ktControllers.controller('MainController', function($rootScope, $location, $log, $http, $cookieStore) {
  $rootScope.$on('event:auth-loginRequired', function() {
    $log.warn("Login required for access");
    $location.path('/login');
  });
  $rootScope.$on('event:auth-loginConfirmed', function() {
    $log.info("Login successful");
  });
});

ktControllers.controller('LoginController', function(MessageFactory, AuthAPI, $rootScope, $scope, $location) {

  $scope.login = function(user) {
    AuthAPI.login(user)
      .success(function(data, status, headers, config) {
        $rootScope.user = AuthAPI.user();
        $location.path('/');
      })
      .error(function(data, status, headers, config) {
        MessageFactory.add("error", "Väärä käyttäjänimi ja/tai salasana.");
      });
    $scope.messages = MessageFactory.get();
  }
});

ktControllers.controller('LogoutController', function(AuthAPI, $http, $rootScope, $log, $location, $cookieStore) {
  AuthAPI.logout()
    .success(function() {
      $log.info("User " + $rootScope.user.username + " logged out");
      $cookieStore.remove('tursas');
      delete $http.defaults.headers.common['Authorization'];
      delete $rootScope.user;
      delete $rootScope.messages;
      $location.path('/');
    })
    .error(function(data, status) {
      $log.error("User " + $rootScope.user.username + " could not be logged out")
    });
});

ktControllers.controller('SubmitAnswerController', function($scope, QuestionAPI) {

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

ktControllers.controller('CreateQuestionController', function($scope, QuestionAPI, $location) {
  $scope.send = function() {
    QuestionAPI.save($scope.question, function(data) {
      $location.path('/question/'+data.messageId);
    });
  }
});

ktControllers.controller('BrowseQuestionsController', function($scope, QuestionAPI) {
  $scope.data = QuestionAPI.get();
});

ktControllers.controller('SingleQuestionController', function($scope, data) {
  $scope.question = data;
});

ktControllers.controller('BrowsePopularController', function($scope, QuestionAPI, AnswerAPI) {

  //$scope.questions = AnswerAPI.get({"questionId": 1});

  /*var questions = QuestionAPI.get(function(data) {
  $scope.questions = data.questions;
  });*/

  $scope.question = QuestionAPI.get();

});

