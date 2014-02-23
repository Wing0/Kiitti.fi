var module = angular.module('ktServices', []);

module.factory('MessageFactory', function() {
  var messages = [];
  return {
    add: function(type, message) {
      messages.push({"type": type, "content": message});
    },
    addList: function(listOfMessages) {
      messages.concat(listOfMessages);
    },
    get: function() {
      return messages;
    },
    clear: function() {
      messages = [];
    }
  }
});
