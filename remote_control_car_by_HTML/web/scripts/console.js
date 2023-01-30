var oDiv = document.getElementById('console');
var btn_forward = document.getElementById('forward');
var btn_back = document.getElementById('back');
var btn_left = document.getElementById('left');
var btn_right = document.getElementById('right');
var esp32state = document.getElementById('state');
var state_text = document.getElementById('state_text');
var maxText = 50;    //控制台最多存在多少行文本
var ajax = new XMLHttpRequest();

ajax.onreadystatechange = () => {
    if (ajax.readyState !== 3) return;
    if ((ajax.status >= 200 && ajax.status < 300) || ajax.status === 304) {
        var recv = ajax.responseText
        if (recv == "esp_true"){
            changeState(true)
        }
        else if (recv == "esp_false"){
            changeState(false)
        }
        console.log(recv);
     }
 };
 

//获取当前时间
function onTime(){
     var now = new Date();
     var time = ("[" + now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds() + "]>>");
     return time
}

//控制台输出一条消息
function conWrite(text){
    var para = document.createElement("p");
    var node = document.createTextNode(onTime() + text);
    para.appendChild(node);
    para.classList.add("context");
    oDiv.appendChild(para);
    oDiv.scrollTop = oDiv.scrollHeight;
}

//删除最上面的消息
function delText(){
    var arrP = oDiv.getElementsByTagName("p");
    for(var i = arrP.length;i>maxText;i--){
        arrP[0].parentNode.removeChild(arrP[0]);
    }
}

//改变esp32连接显示状态
function changeState(bool){
    if (bool){
        esp32state.style.backgroundColor = 'green';
        state_text.innerHTML = "esp32已连接";
        conWrite("esp32已连接");
    }
    else {
        esp32state.style.backgroundColor = 'crimson';
        state_text.innerHTML = "esp32未连接";
        conWrite("esp32未连接");
    }
}

//获取esp32连接状态
function askLink(){
    ajax.open('GET','/car?move=state',true);
    ajax.send();
}


setInterval(delText, 1000);  //定时删除消息

esp32state.onclick = askLink;

esp32state.onmousedown = function (e){
    disX = e.clientX - esp32state.offsetLeft;
    disY = e.clientY - esp32state.offsetTop;

    document.onmousemove = function (e){
        esp32state.style.left = e.clientX - disX + "px";
        esp32state.style.top = e.clientY - disY + "px";
    }

    document.onmouseup = function (e){
        document.onmousemove = null;
        document.onmouseup = null;
    }

    return false;
}

esp32state.ontouchstart = function (e){
    var pos = e.touches[0];
    disX = pos.pageX - esp32state.offsetLeft;
    disY = pos.pageY - esp32state.offsetTop;

    document.ontouchmove = function (e){
        var pos = e.touches[0];
        esp32state.style.left = pos.pageX - disX + "px";
        esp32state.style.top = pos.pageY - disY + "px";
    }

    document.ontouchend = function (e){
        document.ontouchmove = null;
        document.ontouchend = null;
    }
}

document.addEventListener('touchmove', event => {
    event.preventDefault()
}, { passive: false })

btn_forward.onmousedown = function (){
    forwardStart();
    
    btn_forward.onmouseup = function (){
        btn_forward.onmouseup=null;
        btn_forward.onmouseout=null;
        forwardEnd();
    }
    
    btn_forward.onmouseout = function (){
        btn_forward.onmouseup=null;
        btn_forward.onmouseout=null;
        forwardEnd();
    }
}

btn_forward.ontouchstart = function (){
    forwardStart();
}
btn_forward.ontouchend = function (){
    forwardEnd();
}


btn_back.onmousedown = function (){
    backStart();
    
    btn_back.onmouseup = function (){
        btn_back.onmouseup=null;
        btn_back.onmouseout=null;
        backEnd();
    }
    
    btn_back.onmouseout = function (){
        btn_back.onmouseup=null;
        btn_back.onmouseout=null;
        backEnd();
    }
}

btn_back.ontouchstart = function (){
    backStart();
}
btn_back.ontouchend = function (){
    backEnd();
}


btn_left.onmousedown = function (){
    leftStart();
    
    btn_left.onmouseup = function (){
        btn_left.onmouseup=null;
        btn_left.onmouseout=null;
        leftEnd();
    }
    
    btn_left.onmouseout = function (){
        btn_left.onmouseup=null;
        btn_left.onmouseout=null;
        leftEnd();
    }
}

btn_left.ontouchstart = function (){
    leftStart();
}
btn_left.ontouchend = function (){
    leftEnd();
}


btn_right.onmousedown = function (){
    rightStart();
    
    btn_right.onmouseup = function (){
        btn_right.onmouseup=null;
        btn_right.onmouseout=null;
        rightEnd();
    }
    
    btn_right.onmouseout = function (){
        btn_right.onmouseup=null;
        btn_right.onmouseout=null;
        rightEnd();
    }
}

btn_right.ontouchstart = function (){
    rightStart();
}
btn_right.ontouchend = function (){
    rightEnd();
}



function forwardStart(){
    ajax.open('GET','/car?move=forward',true);
    ajax.send();
    conWrite("前进开始");
}

function forwardEnd(){
    ajax.open('GET','/car?move=stop',true);
    ajax.send();
    conWrite("前进结束");
}

function backStart(){
    ajax.open('GET','/car?move=back',true);
    ajax.send();
    conWrite("后退开始");
}

function backEnd(){
    ajax.open('GET','/car?move=stop',true);
    ajax.send();
    conWrite("后退结束");
}

function leftStart(){
    ajax.open('GET','/car?move=left',true);
    ajax.send();
    conWrite("左转开始");
}

function leftEnd(){
    ajax.open('GET','/car?move=stop',true);
    ajax.send();
    conWrite("左转结束");
}

function rightStart(){
    ajax.open('GET','/car?move=right',true);
    ajax.send();
    conWrite("右转开始");
}

function rightEnd(){
    ajax.open('GET','/car?move=stop',true);
    ajax.send();
    conWrite("右转结束");
}