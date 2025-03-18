document.addEventListener("DOMContentLoaded", () => {
    let alerts = document.querySelectorAll(".alert");

    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.add("fade");
                setTimeout(() => alert.remove(), 500);
            });

            let successAlert = document.querySelector(".alert.alert-success");

            if (successAlert) {
                setTimeout(() => {
                    window.location.href = "/";
                }, 1000);
            }

        }, 3000);
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const togglePassword1 = document.getElementById("togglePassword1");
    const password = document.getElementById("password");

    const togglePassword2 = document.getElementById("togglePassword2");
    const confirm_password = document.getElementById("confirm_password");

    const toggleVisibility = (inputField, icon) => {
      if (inputField.type === "password") {
        inputField.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
      } else {
        inputField.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
      }
    }

    togglePassword1.addEventListener("click", () => {
        toggleVisibility(password, togglePassword1)
    })

    togglePassword2.addEventListener("click", () => {
        toggleVisibility(confirm_password, togglePassword2)
    })

})