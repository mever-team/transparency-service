const isInIframe = () => {
  try {
    return window.self !== window.top;
  } catch (e) {
    return true;
  }
};

if (isInIframe()) {
  document.body.classList.add('in-iframe');
}