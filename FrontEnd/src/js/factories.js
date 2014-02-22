var module = angular.module('ktFactories', []);

module.factory('MessageFactory', function() {
  var messages = [];
  return {
    add: function(type, message) {
      messages = [];
      messages.push({"type": type, "content": message});
    },
    get: function() {
      return messages;
    },
    clear: function() {
      messages = [];
    }
  }
});
