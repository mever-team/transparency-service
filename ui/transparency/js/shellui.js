const isInIframe = () => {
  try {
    return window.self !== window.top;
  } catch (e) {
    return true;
  }
};
document.addEventListener('DOMContentLoaded', () => {
  if (isInIframe()) {
    document.body.classList.add('in-iframe');
  }
});