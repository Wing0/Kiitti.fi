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
      }, true);
    }
  }
});

module.directive('ktConversationMessage', function() {
  return {
    restrict: 'AE',
    scope: {
      message: '=message',
      ridType: '@ridType'
    },
    transclude: false,
    templateUrl: '../templates/partial_conversation.message.html',
    controller: function($scope, CommentAPI, VoteAPI) {
      $scope.comment = {};
      $scope.submitMessage = {};

      $scope.submitComment = function() {
        $scope.comment.rid = $scope.message.rid;
        $scope.comment.ridType = $scope.ridType;
        $scope.comment.parentId = $scope.message.messageId;

        CommentAPI.save($scope.comment, function(comment) {
          $scope.message.comments.push(comment);
          $scope.comment.content = "";
          $scope.submitMessage.type = "success";
          $scope.submitMessage.content = "Kommentin lisääminen onnistui.";
          $scope.showCommentInput = false;
        }, function() {
          $scope.submitMessage.type = "error";
          $scope.submitMessage.content = "Kommentin lisääminen ei onnistunut.";
        });
      };

      $scope.vote = function(direction) {
        var vote = {
          "rid": $scope.message.rid,
          "ridType": $scope.ridType,
          "direction": direction
        };

        VoteAPI.save(vote, function(vote) {
          $scope.message.votes_up = vote.votes_up;
          $scope.message.votes_down = vote.votes_down;
          $scope.message.user_vote = vote.user_vote;
        });
      };
    } // /controller
  }
});

