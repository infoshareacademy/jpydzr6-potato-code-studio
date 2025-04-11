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
                    window.location.href = "/profile";
                }, 1000);
            }
            
        }, 3000);
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const togglePassword1 = document.getElementById("togglePassword1");
    const password = document.getElementById("confirm-delete-password");

    const toggleVisibility = (inputField, icon) => {
      if (inputField.type === "confirm-delete-password") {
        inputField.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
      } else {
        inputField.type = "confirm-delete-password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
      }
    }

    togglePassword1.addEventListener("click", () => {
        toggleVisibility(password, togglePassword1)
    })
})

document.addEventListener("DOMContentLoaded", () => {
    const togglePassword = document.getElementById("toggle_old_password");
    const old_password = document.getElementById("id_old_password");

    const togglePassword1 = document.getElementById("toggle_new_password");
    const new_password = document.getElementById("id_new_password1");

    const togglePassword2 = document.getElementById("toggle_new_password2");
    const confirm_password = document.getElementById("id_new_password2");

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
        toggleVisibility(old_password, togglePassword)
    })

    togglePassword1.addEventListener("click", () => {
        toggleVisibility(new_password, togglePassword1)
    })

    togglePassword2.addEventListener("click", () => {
        toggleVisibility(confirm_password, togglePassword2)
    })
})


const toggleDeleteButton = () => {
    const inputPasswordField = document.getElementById("confirm-delete-password")
    const deleteButton = document.getElementById("delete-button")
    deleteButton.disabled = inputPasswordField.value.trim() === ""
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.list-group-item[data-bs-toggle="tab"]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            new bootstrap.Tab(link).show();
        });
    });

    const hash = window.location.hash;
    if (hash) {
        const trigger = document.querySelector(`a[href="${hash}"]`);
        if (trigger) new bootstrap.Tab(trigger).show();
    }

    const alerts = document.querySelectorAll(".alert");
    if (alerts.length) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.add("fade");
                setTimeout(() => alert.remove(), 500);
            });

            const successAlert = document.querySelector(".alert.alert-success");
            if (successAlert) {
                setTimeout(() => {
                    window.location.href = "/profile#discount-vouchers";
                }, 1000);
            }
        }, 3000);
    }
});
