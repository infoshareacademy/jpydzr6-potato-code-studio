const success_alert = (display_text) => {
    event.preventDefault();
    let alert_box = document.getElementById('success-alert');
    
    alert_box.innerHTML = `<strong>${display_text}</strong>`
    alert_box.classList.remove("d-none");
    setTimeout(() => {
        alert_box.classList.add("d-none");
        window.location.href = "/";
    }, 3000);
};

setTimeout(() => {
      let alerts = document.querySelectorAll(".alert");
      alerts.forEach(alert => {
        alert.classList.add("fade-out");
        setTimeout(() => alert.remove(), 500);
      });
}, 3000);