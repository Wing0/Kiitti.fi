var ktControllers = angular.module('ktControllers', []);

ktControllers.controller('MainController', function($scope) {

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

ktControllers.controller('AuthController', function($scope) {

});
