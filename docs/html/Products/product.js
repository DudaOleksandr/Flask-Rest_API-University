const login_url = "http://127.0.0.1:5000/product";
const reg_url = "http://127.0.0.1:5000/user";
function LoginTrue() {
    if(window.localStorage.getItem('login') === true) {
        (document.getElementById("logincheckID").innerHTML +=
                '<a href="../Auth/login.html">Login</a>\n'+
                '<a href="html/User/UserProfile.html">Profile</a>'
        )
    }
}
LoginTrue();
function sendRequest(method, request_url,body = null) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, request_url);
        xhr.responseType = "json";
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.onload = () => {
            if (xhr.status >= 400) {
                reject(xhr.response);
            } else {
                resolve(xhr.response);
            }
        };
        xhr.onerror = () => reject(xhr.response);
        xhr.send(JSON.stringify(body));
    });
}

sendRequest('GET',login_url).then(data => data.map(
    (d) =>
        (document.getElementById("products").innerHTML +=
            '<div class="col-sm-6 col-md-4">\n' +
            '              <div class="product_frame">\n' +
            '                <a href="#">\n' +
            '                  <div class="product_img">\n' +
            '                    <img src= "'+d.status+'" class="img-responsive" height="250" alt="...">\n' +
            '                  </div>\n' +
            '                  <h5 class="shop-thumb__title">\n' +
                               d.name +
            '                  </h5>\n' +
            '                  <div class="shop-thumb__price">\n' +
            '                    <span class="shop-thumb-price_new">\n' +
                                    d.amount + '$' +
            '                      </span>\n' +
            '                  </div>\n' +
            '                </a>\n' +
            '              </div>\n' +
            '            </div>'
            ))
    .catch((err) => console.log(err)));

