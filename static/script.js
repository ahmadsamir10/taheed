let currentTab = 0;
showTab(currentTab);

function showTab(n) {
let x = document.getElementsByClassName("step");
x[n].style.display = "block";
let progress = (n / (x.length - 1)) * 100;
document.querySelector(".progress-bar").style.width = progress + "%";
document
    .querySelector(".progress-bar")
    .setAttribute("aria-valuenow", progress);
// if (n == 0) {
//   document.getElementById("prevBtn").style.display = "none";
// } else {
//   document.getElementById("prevBtn").style.display = "inline";
// }
if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Submit";
} else {
    document.getElementById("nextBtn").innerHTML =
    'التالي<img src="./arrow-left.svg" />';
}
}

async function nextPrev(n) {
let x = document.getElementsByClassName("step");
if (n == 1 && !(await validateForm())) return false;
x[currentTab].style.display = "none";
currentTab += n;
if (currentTab >= x.length) {
    document.querySelector(".progress-bar").style.width = "100%";
    document
    .querySelector(".progress-bar")
    .setAttribute("aria-valuenow", 100);
    resetForm();
    return false;
}
showTab(currentTab);
}

async function validateForm() {
let valid = true;
let x = document.getElementsByClassName("step");
let y = x[currentTab].getElementsByTagName("input");
for (let i = 0; i < y.length; i++) {
    if (y[i].value == "") {
    y[i].className += " invalid";
    valid = false;
    }
}

if (valid) {
    if (currentTab === 0) {
    localStorage.setItem(
        "email",
        document.getElementById("email-input").value
    );
    }
    return await callAPIForStep(currentTab);
}
return valid;
}

async function callAPIForStep(step) {
let apiUrl;
let data;

switch (step) {
    case 0:
    apiUrl = "http://127.0.0.1:8000/users/register/";
    data = { email: localStorage.getItem("email") };
    console.log({data});
    break;
    case 1:
    apiUrl = "http://127.0.0.1:8000/users/verify/";
    data = {
        code: document.getElementById("code-input").value,
        email: localStorage.getItem("email"),
    };
    break;
    case 2:
    apiUrl = "http://127.0.0.1:8000/users/add-phone-number/";
    data = { 
        phone: document.getElementById("phone-input").value,
        email: localStorage.getItem("email")
     };
    break;
    case 3:
    apiUrl = "http://127.0.0.1:8000/users/add-personal-info/";
    data = {
        full_name: document.getElementById("name-input").value,
        id_number: document.getElementById("identification-input")
        .value,
        email: localStorage.getItem("email")
    };
    break;
    case 4:
    apiUrl = "http://127.0.0.1:8000/users/add-motorcycle-count/";
    data = {
        count: document.getElementById("motorcycle-count-input").value,
        email: localStorage.getItem("email")
    };
    break;
    // Add more cases for other steps as needed
}


if (apiUrl && data) {
    try {
    let response = await fetch(apiUrl, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    let result = await response.json();
    if (!response.ok) {
        handleError(step, result.message);
        return false;
    }
    } catch (error) {
    handleError(step, error.message);
    return false;
    }
}
return true;
}

function handleError(step, message) {
let x = document.getElementsByClassName("step");
let errorMessageElement = x[step].querySelector(".error-message");
if (errorMessageElement) {
    errorMessageElement.textContent = message;
}
}

function resetForm() {
let x = document.getElementsByClassName("step");
for (let i = 0; i < x.length; i++) {
    x[i].style.display = "none";
}
let inputs = document.querySelectorAll("input");
inputs.forEach((input) => {
    input.value = "";
    input.className = "";
});
currentTab = 0;
showTab(currentTab);
document.querySelector(".progress-bar").style.width = "0%";
document
    .querySelector(".progress-bar")
    .setAttribute("aria-valuenow", 0);
}
