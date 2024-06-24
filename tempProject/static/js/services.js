console.log("Hello World!");
var nxt = document.getElementById( "choose-btn" );
var txt = document.getElementById("innertxt");
console.log(nxt.type);
nxt.onclick = function () {
    var serv1 = document.getElementById("service1");
    var serv2 = document.getElementById("service2");
    var serv3 = document.getElementById("service3");
    if(serv1.checked ==  true)
        location.href = serv1.value;
    else if(serv2.checked==true)
        location.href = serv2.value;
    else if(serv3.checked==true)
        location.href = serv3.value;
    else
        txt.innerText = "please select an option!";
        setTimeout(()=>{
            const mesag = document.getElementById("innertxt")
            mesag.style.display = 'none';
          },5000)
}