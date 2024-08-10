const text = document.querySelector('.text');
const txt = [
    "欢迎来到 tkintertools 的官方网站 (●'◡'●)，希望本网站能对您有一定的帮助！❤️",
    "Welcome to the official website of tkintertools (●'◡'●), I hope this website can be of some help to you! ❤️"
]; 

var index=0;
var xiaBiao= 0;
var huan = true;

setInterval(function(){
    
    if(huan){      
        text.innerHTML = txt[xiaBiao].slice(0,++index);
        console.log(index);
    }
    else{
        text.innerHTML = txt[xiaBiao].slice(0,index--);
        console.log(index);
    }

    if(index==txt[xiaBiao].length+20) /*20*50 停顿时间*/
    {
        huan = false;
    }
    else if(index<0)
    {
        index = 0;
        huan = true;
        xiaBiao++;
        if(xiaBiao>=txt.length)
        {
            xiaBiao=0; 
        }
    }

},50) /*50间隔时间*/