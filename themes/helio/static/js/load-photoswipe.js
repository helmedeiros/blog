/*
Documentation and licence at https://github.com/liwenyip/hugo-easy-gallery/
*/
(function () {
  var cdn = 'https://cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.3/';
  var files = [
    ['photoswipe.min.css', 'sha512-yxWNfGm+7EK+hqP2CMJ13hsUNCQfHmOuCuLmOq2+uv/AVQtFAjlAJO8bHzpYGQnBghULqnPuY8NEr7f5exR3Qw=='],
    ['default-skin/default-skin.min.css', 'sha512-Rck8F2HFBjAQpszOB9Qy+NVLeIy4vUOMB7xrp46edxB3KXs2RxXRguHfrJqNK+vJ+CkfvcGqAKMJTyWYBiBsGA=='],
    ['photoswipe.min.js', 'sha512-2R4VJGamBudpzC1NTaSkusXP7QkiUYvEKhpJAxeVCqLDsgW4OqtzorZGpulE3eEA7p++U0ZYmqBwO3m+R2hRjA=='],
    ['photoswipe-ui-default.min.js', 'sha512-SxO0cwfxj/QhgX1SgpmUr0U2l5304ezGVhc0AO2YwOQ/C8O67ynyTorMKGjVv1fJnPQgjdxRz6x70MY9r0sKtQ==']
  ];
  var ready = null;

  function fetchFile(file) {
    return new Promise(function (resolve, reject) {
      var css = /\.css$/.test(file[0]);
      var el = document.createElement(css ? 'link' : 'script');
      if (css) {
        el.rel = 'stylesheet';
        el.href = cdn + file[0];
      } else {
        el.src = cdn + file[0];
      }
      el.integrity = file[1];
      el.crossOrigin = 'anonymous';
      el.onload = resolve;
      el.onerror = reject;
      document.head.appendChild(el);
    });
  }

  function loadPhotoSwipe() {
    ready = ready || Promise.all(files.map(fetchFile));
    return ready;
  }

  function figures() {
    return Array.prototype.filter.call(document.querySelectorAll('figure'), function (figure) {
      return !figure.classList.contains('no-photoswipe') && figure.querySelector('img');
    });
  }

  function slide(figure) {
    var img = figure.querySelector('img');
    var link = figure.querySelector('a[itemprop="contentUrl"]') || figure.querySelector('a');
    var thumb = img.currentSrc || img.src;
    var size = link && link.getAttribute('data-size');
    if (size) {
      size = size.split('x');
      return { src: link.href, w: +size[0], h: +size[1], title: img.alt, msrc: thumb };
    }
    return { src: thumb, w: img.naturalWidth || 800, h: img.naturalHeight || 600, title: img.alt, msrc: thumb };
  }

  document.addEventListener('click', function (event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!event.target.closest || event.target.closest('figcaption a')) return;
    var figure = event.target.closest('figure');
    var list = figures();
    var index = list.indexOf(figure);
    var root = document.querySelector('.pswp');
    if (index < 0 || !root) return;
    event.preventDefault();
    var slides = list.map(slide);
    loadPhotoSwipe().then(function () {
      new PhotoSwipe(root, PhotoSwipeUI_Default, slides, { index: index, bgOpacity: 0.8, showHideOpacity: true }).init();
    }, function () {
      ready = null;
      window.location.href = slides[index].src;
    });
  });
})();
