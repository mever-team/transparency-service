module.exports = function(config) {
  config.set({
    basePath: '../',

    /* https://github.com/karma-runner/karma-jasmine/pull/211 */
    client: {
      jasmine: {
        random: true,
        seed: '4321',
        stopOnFailure: true,
        failFast: true,
        timeoutInterval: 30000
      }
    },

    frameworks: [
      'jasmine'
    ],

    files: [
      'https://code.jquery.com/jquery-3.3.1.min.js',
      'https://unpkg.com/mustache@4.2.0/mustache.min.js',
      'ui/transparency/js/index/main.js',
      'ui/transparency/js/index/bearer.js',
      'ui/transparency/js/index/filters.js',
      'ui/transparency/js/themes.js',

      'tests_front/spec/themesSpec.js',
      'tests_front/spec/filtersSpec.js'
    ],
    proxies: { '/js/': 'http://localhost:5000/transparency/js/', 
      '/css/': 'http://localhost:5000/transparency/css/', 
      '/img/': 'http://localhost:5000/transparency/img/', 
      '/templates/': 'http://localhost:5000/transparency/templates/',
      '/transparency/': 'http://localhost:5000/transparency/' 
    },
    // plugins: [
    //   'karma-jasmine',
    //   'karma-chrome-launcher',
    //   'karma-coverage',
    //   'karma-spec-reporter'
    // ],
    preprocessors: {
      'ui/transparency/js/**/*.js': ['coverage']
    },

    reporters: [
      'progress',
      'coverage'
    ],

    coverageReporter: {
      dir: 'coverage/',
      reporters: [
        {
          type: 'html'
        },
        {
          type: 'text-summary'
        }
      ]
    },

    browsers: [
      'ChromeHeadless'
      // 'Chrome'
    ],

    singleRun: true,

    // autoWatch: true
  });
};