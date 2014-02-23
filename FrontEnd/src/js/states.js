var ktStates = angular.module('ktStates', ['ui.router',
                                           'ktControllers', 'ktAPI']);

ktStates.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider
    .when('/', '/questions')
    .otherwise('/');

  var tdir = '../templates/';

  $stateProvider
    .state('login', {
      abstract: true,
      templateUrl: tdir + 'loginmaster.html',
      controller: 'LoginController',
      url: '/login'
    })
    .state('login.login', {
      url: '',
      templateUrl: tdir + 'loginmaster.login.html'
    })
    .state('login.forgot', {
      url: '/forgot',
      templateUrl: tdir + 'loginmaster.forgot.html'
    })
    .state('logout', {
      url: '/logout',
      controller: 'LogoutController'
    })

    .state('master', {
      abstract: true,
      templateUrl: tdir + 'master.html'
    })

    .state('master.popular', {
      url: '/popular',
      templateUrl: tdir + 'question.html',
      controller: 'BrowsePopularController'
    })
    .state('master.questions', {
      url: '/questions',
      templateUrl: tdir + 'questions.all.html',
      controller: 'BrowseQuestionsController'
    })
    .state('master.createQuestion', {
      url: '/question/new',
      templateUrl: tdir + 'create_question.html',
      controller: 'CreateQuestionController'
    })
    .state('master.question', {
      url: '/question/:messageId',
      templateUrl: tdir + 'question.html',
      resolve: {
        question: function(QuestionAPI, $stateParams) {
          return QuestionAPI.get({"messageId": $stateParams.messageId});
        }
      },
      controller: 'SingleQuestionController'
    });
});


