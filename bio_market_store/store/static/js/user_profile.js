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
