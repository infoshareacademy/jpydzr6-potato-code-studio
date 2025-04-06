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
                    window.location.href = "/product_list";
                }, 1000);
            }
            
        }, 3000);
    }
});

const togglePassword = () => {
    const togglePassword = document.getElementById("togglepassword");
    const password = document.getElementById("id_password");

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

    togglePassword.addEventListener("click", () => {
        toggleVisibility(password, togglePassword)
    })
}