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
    const tabLinks = document.querySelectorAll('.list-group-item[data-bs-toggle="tab"]');

    tabLinks.forEach(link => {
        link.addEventListener('click', function () {
            tabLinks.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
        });
    });

    const hash = window.location.hash;
    if (hash) {
        const tabTrigger = document.querySelector(`a[href="${hash}"]`);
        if (tabTrigger) {
            new bootstrap.Tab(tabTrigger).show();
            tabTrigger.classList.add('active');
        }
    }
});
