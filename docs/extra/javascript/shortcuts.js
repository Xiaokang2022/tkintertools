// 键盘左键上一页
keyboard$.subscribe(function (key) {
  if (key.mode === "global" && key.type === "ArrowLeft") {
    var elements = document.getElementsByClassName(
      "md-footer__link md-footer__link--prev"
    );
    if (elements.length) elements[0].click();
    key.claim();
  }
});

// 键盘右键下一页
keyboard$.subscribe(function (key) {
  if (key.mode === "global" && key.type === "ArrowRight") {
    var elements = document.getElementsByClassName(
      "md-footer__link md-footer__link--next"
    );
    if (elements.length) elements[0].click();
    key.claim();
  }
});
