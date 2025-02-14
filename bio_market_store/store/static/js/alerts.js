const success_alert = (display_text) => {
    event.preventDefault();
    let alert_box = document.getElementById('success-alert');
    
    alert_box.innerHTML = `<strong>${display_text}</strong>`
    alert_box.classList.remove("d-none");
    setTimeout(() => {
        alertBox.classList.add("d-none");
    }, 3000);
};