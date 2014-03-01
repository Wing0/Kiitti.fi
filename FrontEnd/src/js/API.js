var module = angular.module('ktAPI', ['ngResource', 'ngCookies']);

module.factory('AuthAPI', function($http, APIUrl, AuthToken, authService, $cookieStore, $log) {
  var user;
  var Methods = {};

  Methods.user = function() {
    return user;
  };

  Methods.setToken = function(token) {
    /* set token into cookies */
    $cookieStore.put(AuthToken, token);
    $http.defaults.headers.common['Authorization'] = 'Token ' + token;
  }

  Methods.unSetToken = function() {
    $cookieStore.remove(AuthToken);
    delete $http.defaults.headers.common['Authorization'];
    delete user;
  };

  Methods.load = function() {
    return $http.get(APIUrl + '/auth/load')
      .success(function(data) {
        user = data;
      })
      .error(function(response) {
        $log.error("Could not load user");
        Methods.unSetToken();
      });
  };

  Methods.logout = function() {
    return $http.get(APIUrl + '/auth/logout')
      .success(function(data) {
        Methods.unSetToken();
      });
  };

  Methods.login = function(user) {
    return $http.post(APIUrl + '/auth/login', user)
      .success(function(data) {
        /* set token into cookies */
        try { var authtokenData = data.token; }
        catch(TypeError) {
          $log.info("Already logged in.")
        };

        if (authtokenData) {
          // set token
          Methods.setToken(authtokenData);

          // get user data
          Methods.load(function() {
            /* confirm login only after getting user data */
            authService.loginConfirmed();
          }, function() {
            $log.error("Unexpected error in loading user")
          });
        }
      });
  };

  Methods.register = function(user) {
    return $http.post(APIUrl + '/auth/register', user);
  };

  return Methods;
});

module.factory('QuestionAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/questions/:rid', {rid: '@rid'});
});

module.factory('AnswerAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/answers/:rid', {rid: '@rid'});
});

module.factory('CommentAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/comments/:ridType/:rid',
                   {rid: '@rid', ridType: '@ridType'});
});

module.factory('VoteAPI', function($resource, APIUrl) {
  return $resource(APIUrl + '/votes/:ridType/:rid',
                   {rid: '@rid', ridType: '@ridType'});
});
