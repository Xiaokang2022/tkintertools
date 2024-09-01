const txt = [
  "Welcome to the official website of tkintertools, I hope this website can be of some help to you!",
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
