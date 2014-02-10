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

ktControllers.controller('LoginController', function($rootScope, $scope, $http, authService, AuthAPI, $location, $cookieStore) {

  /* do not show messages from redirect errors */
  delete $rootScope.messages;

  $scope.login = function(user) {
    AuthAPI.login(user)
      .success(function(data, status, headers, config) {
        /* set token into cookies */
        $cookieStore.put('tursas', data.token);
        $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;

        /* confirm login */
        authService.loginConfirmed();

        /* load user data */
        AuthAPI.load().success(function(data) {
          $rootScope.user = data.user;

          /* redirect */
          $location.path('/');
        }).error(function(response) {
          $rootScope.messages = [{"content": "Odottamaton virhe. Ole hyvä ja yritä uudelleen.", "type": "error"}];
        });
      })
      .error(function(data, status, headers, config) {
        $rootScope.messages = [{"content": "Väärä käyttäjänimi ja/tai salasana.", "type": "error"}];
      });
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

ktControllers.controller('CreateQuestionController', function($scope, QuestionFactory) {
  $scope.send = function() {
    console.log($scope.question);
    QuestionFactory.save($scope.question);
  }
});

ktControllers.controller('BrowseQuestionsController', function($scope, QuestionFactory) {
  $scope.data = QuestionFactory.get();
});

ktControllers.controller('SingleQuestionController', function($scope, data) {
  $scope.question = data;
});

ktControllers.controller('BrowsePopularController', function($scope, QuestionFactory, AnswerFactory) {

  //$scope.questions = AnswerFactory.get({"questionId": 1});

  /*var questions = QuestionFactory.get(function(data) {
  $scope.questions = data.questions;
  });*/

  $scope.question = QuestionFactory.get();

});

