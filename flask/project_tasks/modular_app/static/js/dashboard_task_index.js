btn_logout = document.getElementById('btn_logout');
btn_logout.onclick = 
function logout(){
    let http = new XMLHttpRequest();
    let url = "http://127.0.0.1:5000/logout";

    http.open("POST", url);

    http.onload = function(){
        window.location = http.responseText
    };

    http.send();
};