var module = angular.module('ktDirectives', []);

module.directive('ktMessages', function() {
  return {
    restrict: 'AE',
    scope: {},
    transclude: false,
    templateUrl: '../templates/partial_messages.html',
    controller: function($scope, MessageFactory) {
      /* Bind scope messages to message factory */
      $scope.$watch(function() { return MessageFactory.get(); }, function(data) {
        $scope.messages = data;
        console.log($scope.messages);
      }, true);
    }
  }
});

module.directive('ktConversationMessage', function() {
  return {
    restrict: 'AE',
    scope: {
      message: '=message'
    },
    transclude: false,
    templateUrl: '../templates/partial_conversation.message.html'
  }
});

