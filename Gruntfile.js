module.exports = function(grunt) {
  'use strict';

  require('load-grunt-tasks')(grunt);
  var productRoot = 'collective/portlet/mybookmarks/browser';
  grunt.initConfig({
    cssmin: {
      target: {
        files: {
          './collective/portlet/mybookmarks/browser/stylesheets/mybookmarks.min.css': [
            `${productRoot}/stylesheets/mybookmarks.css`
          ]
        }
      },
      options: {
        sourceMap: true
      }
    },
    // requirejs: {
    //   'mybookmarks': {
    //     options: {
    //       baseUrl: './',
    //       generateSourceMaps: true,
    //       preserveLicenseComments: false,
    //       paths: {
    //         jquery: 'empty:',
    //         'pat-base': 'empty:',
    //         'pat-registry': 'empty:',
    //         'mockup-patterns-modal': 'empty:',
    //       },
    //       wrapShim: true,
    //       name: `${productRoot}/javascripts/bundle.js`,
    //       exclude: ['jquery'],
    //       out: `${productRoot}/tiles-management-compiled.js`,
    //       optimize: 'none'
    //     }
    //   }
    // },
    babel: {
      options: {
        sourceMap: true,
        presets: ['es2015']
      },
      dist: {
        files: {
          './collective/portlet/mybookmarks/browser/javascripts/mybookmarks.min.js':
            './collective/portlet/mybookmarks/browser/javascripts/mybookmarks.js'
        }
      }
    },

    uglify: {
      mybookmarks: {
        options: {
          sourceMap: true,
          sourceMapName: `./${productRoot}/javascripts/mybookmarks.js.map`,
          sourceMapIncludeSources: false
        },
        files: {
          './collective/portlet/mybookmarks/browser/javascripts/mybookmarks.min.js': [
            './collective/portlet/mybookmarks/browser/javascripts/mybookmarks.min.js'
          ]
        }
      }
    },
    watch: {
      scripts: {
        files: [`${productRoot}`],
        tasks: ['uglify'],
        options: {
          livereload: true
        }
      }
      // css: {
      //   files: `${productRoot}/static/integration.css`,
      //   tasks: ['cssmin'],
      //   options: {
      //     livereload: true
      //   }
      // }
    }
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('compile', ['cssmin', 'babel', 'uglify']);
};
