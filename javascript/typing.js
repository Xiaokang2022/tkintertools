const txt = [
  "欢迎来到 tkintertools 的官方网站，希望本网站能对您有一定的帮助！",
];

const txt_en = [
  "Welcome to the official website of tkintertools, I hope this website can be of some help to you!",
];

var index = 0;
var i = 0;
var switch_flag = true;

var index_en = 0;
var i_en = 0;
var switch_flag_en = true;

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

setInterval(function () {
  if (switch_flag_en) {
    document.querySelector(".text_en").innerHTML = txt_en[i_en].slice(
      0,
      ++index_en
    );
  } else {
    document.querySelector(".text_en").innerHTML = txt_en[i_en].slice(
      0,
      index_en--
    );
  }

  if (index_en == txt_en[i_en].length + 25) {
    /*25*40 停顿时间*/
    switch_flag_en = false;
  } else if (index_en == 0) {
    index_en = 0;
    switch_flag_en = true;
    i_en++;
    if (i_en >= txt_en.length) {
      i_en = 0;
    }
  }
}, 40); /*50间隔时间*/
