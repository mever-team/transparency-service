module.exports = function(config) {
  config.set({
    basePath: '../',

    /* https://github.com/karma-runner/karma-jasmine/pull/211 */
    client: {
      captureConsole: true,
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

      'tests_front/spec/account/mainSpec.js',
      'tests_front/spec/themesSpec.js',
      'tests_front/spec/handbook/mainSpec.js',
      'tests_front/spec/index/mainSpec.js',
      'tests_front/spec/index/filtersSpec.js',
      'tests_front/spec/card/cardSpec.js',
      'tests_front/spec/card/chatSpec.js',
      'tests_front/spec/card/eval_adapterSpec.js',
    ],
    proxies: { 
      // '/js/': 'http://localhost:5000/transparency/js/', 
      '/css/': 'http://localhost:5000/transparency/css/', 
      '/img/': 'http://localhost:5000/transparency/img/', 
      '/templates/': 'http://localhost:5000/transparency/templates/',
      '/transparency/': 'http://localhost:5000/transparency/' 
    },
    plugins: [
      'karma-spec-reporter',
      'karma-*',
      { 'preprocessor:transform': ['factory', require('./karma-transform')] },
    ],
    specReporter: {
      suppressPassed: false,
      suppressFailed: false,
      suppressSkipped: false
    },
    preprocessors: {
      'ui/transparency/js/**/*.js': ['transform', 'coverage']
    },

    reporters: [
      'spec',
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
    // logLevel: config.LOG_DEBUG,
    // autoWatch: true
  });
};