document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            validateLogin();
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            event.preventDefault();
            validateRegister();
        });
    }
});

// Function to validate login input
function validateLogin() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();
    const usernameError = document.getElementById("login-username-error");
    const passwordError = document.getElementById("login-password-error");

    usernameError.textContent = "";
    passwordError.textContent = "";

    if (username === "") {
        usernameError.textContent = "Username is required.";
        return;
    }
    if (password.length < 6) {
        passwordError.textContent = "Password must be at least 6 characters.";
        return;
    }

    fetch("login.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Database connection failed. Please try again later.");
            } else if (data.success) {
                alert("Login successful!");
                window.location.href = "dashboard.html"; // Redirect to user dashboard
            } else {
                alert("Invalid username or password.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
        });
}

// Function to validate and register a new user
function validateRegister() {
    const username = document.getElementById("register-username").value.trim();
    const password = document.getElementById("register-password").value.trim();
    const usernameError = document.getElementById("register-username-error");
    const passwordError = document.getElementById("register-password-error");

    usernameError.textContent = "";
    passwordError.textContent = "";

    if (username === "") {
        usernameError.textContent = "Username is required.";
        return;
    }
    if (password.length < 6) {
        passwordError.textContent = "Password must be at least 6 characters.";
        return;
    }

    fetch("register.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Database connection failed. Please try again later.");
            } else if (data.success) {
                alert("Registration successful! You can now log in.");
                window.location.href = "login.html"; // Redirect to login page
            } else {
                alert(data.message || "Registration failed.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
        });
}
