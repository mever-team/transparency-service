var json = {
    "password": "admin",
    "username": "admin"
}
let token = "";


setInterval(function hello() {
    $.ajax({
        url: "http://127.0.0.1:5000/login",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(json),
        success: function (response) {
            token = response.token;
        },
        error: function (xhr, status, error) {
            alert("ERROR LOGIN");
        }
    });
    return hello;
}(), 3500000);


