// Generated on 2014-01-22 using generator-angular 0.7.1
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // modRewrite for middleware to redirect all requests to root (AngularJS HTML5 mode)
  var modRewrite = require('connect-modrewrite');

  // Define the configuration for all the tasks
  grunt.initConfig({

    // configurable paths
    pkg: grunt.file.readJSON('package.json'),
    app: {
      name:     'Kiitti QnA',
      src:      'src',
      dist:     'dist',
      styles:   'styles',
      sass:     'sass',
      fonts:    'fonts',
      images:   'images',
      scripts:  'js',
      tmp:      '.tmp'
    },

    // Watches files for changes and runs tasks based on the changed files
    watch: {
      compass: {
        files: ['<%= app.src %>/<%= app.sass %>/{,*/}*.{scss,sass}'],
        tasks: ['compass:server']
      },
      styles: {
        files: ['<%= app.src %>/<%= app.styles %>/{,*/}*.css'],
        tasks: ['copy:styles']
      },
      gruntfile: {
        files: ['Gruntfile.js']
      }
      // ,
      // livereload: {
      //   options: {
      //     livereload: '<%= connect.options.livereload %>'
      //   },
      //   files: [
      //     '<%= app.src %>/*.html',
      //     '.tmp/<%= app.styles %>/{,*/}*.css',
      //     '{.tmp,<%= app.src %>}/<%= app.styles %>/{,*/}*.js',
      //     '<%= app.src %>/<%= app.images %>/{,*/}*.{gif,jpeg,jpg,png,svg,webp}'
      //   ]
      // }
    },

    // The actual grunt server settings
    connect: {
      options: {
        port: 9000,
        base: '<%= app.src %>',
        // change this to '0.0.0.0' to access the server from outside
        hostname: '0.0.0.0',
        livereload: 35729,
        middleware: function (connect, options) {
          var middlewares = [];
          var directory = options.directory || options.base[options.base.length - 1];

          // enable Angular's HTML5 mode
          middlewares.push(modRewrite(['!\\.html|\\.js|\\.svg|\\.css|\\.png|\\.jpg|\\.jpeg$ /index.html [L]']));

          if (!Array.isArray(options.base)) {
            options.base = [options.base];
          }
          options.base.forEach(function(base) {
            // Serve static files.
            middlewares.push(connect.static(base));
          });

          // Make directory browse-able.
          middlewares.push(connect.directory(directory));

          return middlewares;
        }
      },
      livereload: {
        options: {
          open: true,
          base: [
            '.tmp',
            '<%= app.src %>'
          ]
        }
      },
      dev: {
        options: {
          base: [
            '.tmp',
            '<%= app.src %>'
          ]
        }
      },
      test: {
        options: {
          port: 9001,
          base: [
            '.tmp',
            'test',
            '<%= app.src %>'
          ]
        }
      },
      dist: {
        options: {
          base: '<%= app.dist %>'
        }
      }
    },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= app.dist %>/*',
            '!<%= app.dist %>/.git*'
          ]
        }]
      },
      server: '.tmp'
    },

    // Automatically inject Bower components into the app
    'bower-install': {
      app: {
        html: '<%= app.src %>/index.html',
        ignorePath: '<%= app.src %>/'
      }
    },

    compass: {
      options: {
        sassDir: '<%= app.src %>/<%= app.sass %>',
        cssDir: '<%= app.tmp %>/<%= app.styles %>',
        generatedImagesDir: '<%= app.tmp %>/<%= app.images %>/generated',
        imagesDir: '<%= app.src %>/<%= app.images %>',
        javascriptsDir: '<%= app.src %>/<%= app.scripts %>',
        fontsDir: '<%= app.src %>/<%= app.fonts %>',
        importPath: '<%= app.src %>/bower_components',
        httpImagesPath: '/<%= app.images %>',
        httpGeneratedImagesPath: '/<%= app.images %>/generated',
        httpFontsPath: '/<%= app.fonts %>',
        relativeAssets: false,
        assetCacheBuster: false,
        raw: 'Sass::Script::Number.precision = 10\n'
      },
      dist: {
        options: {
          generatedImagesDir: '<%= app.dist %>/<%= app.images %>/generated'
        }
      },
      server: {
        options: {
          debugInfo: true
        }
      }
    },

    // Renames files for browser caching purposes
    rev: {
      dist: {
        files: {
          src: [
            '<%= app.dist %>/<%= app.scripts %>/{,*/}*.js',
            '<%= app.dist %>/<%= app.styles %>/{,*/}*.css',
            '<%= app.dist %>/<%= app.images %>/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
            '<%= app.dist %>/<%= app.fonts %>/*'
          ]
        }
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: '<%= app.src %>/index.html',
      options: {
        dest: '<%= app.dist %>'
      }
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      html: ['<%= app.dist %>/{,*/}*.html'],
      css: ['<%= app.dist %>/<%= app.css %>/{,*/}*.css'],
      options: {
        assetsDirs: ['<%= app.dist %>']
      }
    },

    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= app.src %>/<%= app.images %>',
          src: '{,*/}*.{png,jpg,jpeg,gif}',
          dest: '<%= app.dist %>/<%= app.images %>'
        }]
      }
    },
    svgmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= app.src %>/<%= app.images %>',
          src: '{,*/}*.svg',
          dest: '<%= app.dist %>/<%= app.images %>'
        }]
      }
    },
    htmlmin: {
      dist: {
        options: {
          collapseWhitespace: false,
          collapseBooleanAttributes: false,
          removeComments: false,
          removeCommentsFromCDATA: true,
          removeOptionalTags: false
        },
        files: [{
          expand: true,
          cwd: '<%= app.dist %>',
          src: ['*.html', 'views/{,*/}*.html'],
          dest: '<%= app.dist %>'
        }]
      }
    },

    // Allow the use of non-minsafe AngularJS files. Automatically makes it
    // minsafe compatible so Uglify does not destroy the ng references
    ngmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= app.tmp %>/concat/<%= app.scripts %>',
          src: '*.js',
          dest: '<%= app.tmp %>/concat/<%= app.scripts %>'
        }]
      }
    },

    uflify: {
      options: {
        mangle: true
      }
    },

    // Replace Google CDN references
    cdnify: {
      dist: {
        html: ['<%= app.dist %>/*.html']
      }
    },

    // Put files not handled in other tasks here
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= app.src %>',
          dest: '<%= app.dist %>',
          src: [
            '*.{ico,png,txt}',
            '*.html',
            '{templates,ngtemplates,views}/{,*/}*.html',
            //'bower_components/**/*',
            '<%= app.fonts %>/{,*/}*.{eot,svg,ttf,woff}',
            '<%= app.styles %>/{,*/}*.css',
            '<%= app.images %>/{,*/}*.{webp,gif,jpg,jpeg,png}'
          ]
        }]
      },
      styles: {
        expand: true,
        cwd: '<%= app.src %>/<%= app.styles %>',
        dest: '.tmp/<%= app.styles %>/',
        src: '{,*/}*.css'
      },

    },

    // Run some tasks in parallel to speed up the build process
    concurrent: {
      server: [
        'compass:server'
      ],
      test: [
        'compass'
      ],
      dist: [
        'compass:dist',
        'imagemin:dist',
        'svgmin:dist'
      ]
    },

    // By default, your `index.html`'s <!-- Usemin block --> will take care of
    // minification. These next options are pre-configured if you do not wish
    // to use the Usemin blocks.
    // cssmin: {
    //   dist: {
    //     files: {
    //       '<%= app.dist %>/styles/main.css': [
    //         '.tmp/styles/{,*/}*.css',
    //         '<%= app.src %>/styles/{,*/}*.css'
    //       ]
    //     }
    //   }
    // },
    // uglify: {
    //   dist: {
    //     files: {
    //       '<%= app.dist %>/scripts/scripts.js': [
    //         '<%= app.dist %>/scripts/scripts.js'
    //       ]
    //     }
    //   }
    // },
    // concat: {
    //   dist: {}
    // },
  });


  grunt.registerTask('serve', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['build', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      'clean:server',
      'bower-install',
      'concurrent:server',
      'connect:dev',
      'watch'
    ]);
  });

  grunt.registerTask('server', function () {
    grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
    grunt.task.run(['serve']);
  });

  grunt.registerTask('build', [
    'clean:dist',
    'bower-install',
    'useminPrepare',
    'concurrent:dist',
    'concat', // useminPrepare
    'ngmin:dist',
    'copy:dist',
    'cdnify:dist',
    'cssmin', // useminPrepare
    'uglify', // useminPrepare
    'rev:dist',
    'usemin',
    'htmlmin:dist'
  ]);

  grunt.registerTask('default', [
    //'jshint',
    //'test',
    'build'
  ]);
};
