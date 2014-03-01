var app = angular.module('app', [
  'ngResource', 'ngAnimate', 'ngSanitize', 'ngCookies', // Angular
  'textAngular', // 3rd party
  'ktStates', 'ktControllers', 'ktServices', 'ktDirectives', 'ktFilters', 'ktAPI' // Kiitti
]);

/* CONFIG */

app.constant("APIUrl", 'http://127.0.0.1:8000');
app.constant("AuthToken", 'tursas');

app.config(function($locationProvider, $httpProvider, $cookiesProvider) {

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

  // Messages interceptor
  $httpProvider.interceptors.push(function($q, httpBuffer, MessageFactory) {
    return {
      'response': function(response) {
          if (response.data.messages) {
            var messages = response.data.messages;
            // set type for messages
            angular.forEach(messages, function(value, key) {
              value.type = "success";
            });
            MessageFactory.addList(messages);
          }
          return response || $q.when(response); // default behaviour
        },
      'responseError': function(rejection) {
        if (rejection.data.messages) {
          var messages = rejection.data.messages;
          // set type for messages
          angular.forEach(messages, function(value, key) {
            value.type = "error";
          });
          MessageFactory.addList(messages);
        }
        return $q.reject(rejection); // default behaviour
      }
    };
  });
});

app.run(function($rootScope, $cookieStore, $http, AuthAPI, MessageFactory, AuthToken) {

  $rootScope.$on('$stateChangeStart', function() {
    MessageFactory.clear();
  });

  /* Get user if already logged in */
  if ($cookieStore.get(AuthToken)) {
    $http.defaults.headers.common['Authorization'] = 'Token ' + $cookieStore.get(AuthToken);
    AuthAPI.load().success(function(data) {
      $rootScope.user = data.user;
    });
  }
})
