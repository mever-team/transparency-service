// karma-transform.js
const path = require('path');

module.exports = function () {
  return function (content, file, done) {
    let js = content;

    js = js.replaceAll("window.location.reload()", "// window.location.reload()"); // prevent reloads and redirect
    js = js.replace(/window\.location\.href\s*=\s*/g, "");
    js = js.replaceAll('window.open', "//window.open");
    js = js.replaceAll("urlParams.get('id')", "karmaTestCardId");
    js = js.replaceAll('urlParams.get("id")', "karmaTestCardId");

    done(js);
  };
};

module.exports.$inject = [];