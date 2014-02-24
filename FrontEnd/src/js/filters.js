var module = angular.module('ktFilters', []);

module.filter('slice', function() {
  return function(content, params) {

    // find slicing position (character " ")
    var slicePosition = params.length;
    while (true) {
      if (slicePosition > content.length) break;
      if (content[slicePosition] == " " || content[slicePosition] == "\n") break;
      else slicePosition++;
    }

    // slice
    var sliced = content.slice(0, slicePosition);
    if (content.length > slicePosition)
      sliced = sliced + " …"

    return sliced;
  }
});
