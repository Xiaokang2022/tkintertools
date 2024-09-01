const txt = [
  "欢迎来到 tkintertools 的官方网站，希望本网站能对您有一定的帮助！",
];

var index = 0;
var i = 0;
var switch_flag = true;

setInterval(function () {
  if (switch_flag) {
    document.querySelector(".text").innerHTML = txt[i].slice(0, ++index);
  } else {
    document.querySelector(".text").innerHTML = txt[i].slice(0, index--);
  }

  if (index == txt[i].length + 25) {
    /*25*40 停顿时间*/
    switch_flag = false;
  } else if (index == 0) {
    index = 0;
    switch_flag = true;
    i++;
    if (i >= txt.length) {
      i = 0;
    }
  }
}, 40); /*50间隔时间*/
