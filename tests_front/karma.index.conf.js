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
      'tests_front/globals.js',
      {
        pattern: 'ui/transparency/*.html',
        included: false
      },
      {
        pattern: 'ui/transparency/js/**/*.js',
        included: false,
        served: true
      },

      'tests_front/spec/themesSpec.js',
      'tests_front/spec/index/filtersSpec.js',
      'tests_front/spec/index/mainSpec.js'
    ],
    proxies: { 
      // '/js/': 'http://localhost:5000/transparency/js/', 
      '/css/': 'http://localhost:5000/transparency/css/', 
      '/img/': 'http://localhost:5000/transparency/img/', 
      '/templates/': 'http://localhost:5000/transparency/templates/',
      '/transparency/': 'http://localhost:5000/transparency/' 
    },
    preprocessors: {
      'ui/transparency/js/**/*.js': ['coverage']
    },

    reporters: [
      'progress',
      'coverage'
    ],

    coverageReporter: {
      dir: 'coverage/',
      subdir: '.',
      reporters: [
        {type: 'html'},
        {type: 'text-summary'},
        { type: 'lcovonly' }
      ]
    },

    browsers: [
      'ChromeHeadlessNoSandbox'
      // 'ChromeHeadless'
      // 'Chrome'
    ],
    customLaunchers: {
      ChromeHeadlessNoSandbox: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox']
      }
    },
    singleRun: true,

    // autoWatch: true
  });
};