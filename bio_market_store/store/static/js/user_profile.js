document.addEventListener("DOMContentLoaded", () => {
    let alerts = document.querySelectorAll('.alert');

    if (alerts.length > 0) { 
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.add('fade');
                setTimeout(() => alert.remove(), 500);
            });
            
            setTimeout(() => {
                window.location.href = "/profile";
            }, 1000);
            
        }, 3000);
    }
});