var app = angular.module('app', ['ngResource', 'ngRoute', 'ngAnimate']);

/* CONFIG */

app.config(function($routeProvider, $locationProvider) {

  $routeProvider
    .when('/', {
      templateUrl: 'templates/frontPage2.html',
      controller: 'FrontPageController'
    })
    .otherwise({redirectTo : '/'});

  $locationProvider
    .html5Mode(true)
    .hashPrefix('!');

});

/* CONTROLLERS */

app.controller('FrontPageController', function($scope) {

});

/* DIRECTIVES */

app.directive('tabSet', function() {
  return {
    restrict: 'A',
    template: '<div class="tab-set" ng-transclude></div ng-transclude>',
    replace: true,
    transclude: true,

    controller: function($scope) {
      var tabLinks = [];
      var tabs = [];

      this.addTabLink = function(tabLink) {
        tabLinks.push(tabLink);
      }

      this.addTab = function(tab) {
        tabs.push(tab);
      }

      this.gotOpened = function(selectedTab) {
        angular.forEach(tabLinks, function(tabLink) {
          if (selectedTab === tabLink) tabLink.active = true;
          else tabLink.active = false;
        });

        angular.forEach(tabs, function(tab) {
          if (tab.id === selectedTab.id) tab.showMe = true;
          else tab.showMe = false;
        });
      }
    }
  };
});

app.directive('tabNav', function() {
  return {
    restrict: 'A',
    templateUrl: 'templates/navBar.html',
    require: '^tabSet',
    replace: true,
    transclude: true,
    link: function(scope, element, attrs) {
    }
  };
});

app.directive('tabLink', function() {
  return {
    restrict: 'A',
    scope: { id: '@id' },
    templateUrl: 'templates/tabLink.html',
    require: '^tabSet',
    replace: true,
    transclude: true,

    link: function(scope, element, attrs, tabSetController) {
      tabSetController.addTabLink(scope);
      if (attrs.id === 'projects') scope.active = true;

      scope.open = function open() {
        tabSetController.gotOpened(scope);
        // auto-scroll
        $('html, body').delay(200).animate({
            scrollTop: ($('#tabs').offset().top)
        }, 500);
      }
    }
  };
});

app.directive('tab', function() {
  return {
    restrict: 'A',
    scope: { id: '@id' },
    template: '<div ng-show="showMe" class="tab animate-show" ng-cloak ng-transclude></div>',
    require: '^tabSet',
    replace: true,
    transclude: true,

    link: function(scope, element, attrs, tabSetController) {
      tabSetController.addTab(scope);
      if (attrs.id === 'projects') scope.showMe = true;
    }
  };
});
