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

    const submitButton = document.querySelector('button[name="submit');
    const nextButton = document.getElementById("nextBtn");
    const retryButton = document.getElementById("retryBtn");

    document.querySelectorAll('input[type="radio"][name="answer"]').forEach(radio => {
        radio.addEventListener("change", () => {
            submitButton.disables = false;
        });
    });

    if (submitButton && nextButton) {
        nextButton.style.display = submitButton.disabled ? "inline-block" : "none";
    }

    if (retryButton) {
        retryButton.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = retryButton.getAttribute("href");
            setTimeout(() => location.reload(true), 500);
        });
    }
});
