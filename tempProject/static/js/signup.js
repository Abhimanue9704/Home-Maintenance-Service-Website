/*toanimate text
const text=document.querySelector(".heads");
const strtext=text.textContent;
const splittext=strtext.split("");
text.textContent="";
for(let i=0;i<splittext.length;i++){
    text.innerHTML+="<span>"+splittext[i]+"</span>";
}
let char = 0;
let timer = setInterval(onTick,50);
function onTick() {
    const span1 = text.querySelectorAll("span")[char];
    span1.classList.add('fade');
    char++;
    if (char >= splittext.length) {
        complete();
        return;
    }
}
function complete() {
    clearInterval(timer);
    timer=null;
}
*/
// console.log("Hello World!");
// var nxt = document.getElementById( "next" );
// var txt = document.getElementById("innertxt");
// console.log(nxt.type);
// nxt.onclick = function () {
//     var user = document.getElementById( "user" );
//     var client = document.getElementById("client");
//     if(user.checked ==  true)
//         location.href = user.value;
//     else if(client.checked==true)
//         location.href = client.value;
//     else
//         txt.innerText = "please select an option!";
// }
// function fun1(){
    
    /*if(user.checked ==  true)
        console.log(user.value);
    else if(client.checked==true)
        console.log(client.value);
    else
        alert("nothing selected!!");*/
// }

// console.log("Hello World!");

// var nxt = document.getElementById("next");
// var txt = document.getElementById("innertxt");
// console.log(nxt.type);

// nxt.onclick = function () {
//     var user = document.getElementById("user");
//     var client = document.getElementById("client");

//     if (user.checked) {
//         location.href = user.value; // Redirect to signupUser.html if "User" is selected
//     } else if (client.checked) {
//         location.href = client.value; // Redirect to signupClient.html if "Client" is selected
//     } else {
//         txt.innerText = "Please select an option!";
//     }
// };

function fun1() {
    var user = document.getElementById("user");
    var client = document.getElementById("client");

    if (user.checked) {
        location.href = "{% url 'serviceProvider_signUp' %}"; // Redirect to signupUser.html if "User" is selected
    } else if (client.checked) {
        location.href = "{% url 'client_signUpPage' %}"; // Redirect to signupClient.html if "Client" is selected
    } else {
        txt.innerText = "Please select an option!";
    }
};

