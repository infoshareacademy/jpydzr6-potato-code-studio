document.addEventListener("DOMContentLoaded", () => {
    let alerts = document.querySelectorAll(".alert");

    if (alerts.length > 0) { 
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.add("fade");
                setTimeout(() => alert.remove(), 500);
            });           
        }, 3000);
    }
});
