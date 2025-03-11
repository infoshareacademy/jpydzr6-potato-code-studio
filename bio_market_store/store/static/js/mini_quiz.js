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

    let progressBar = document.getElementById("progressBar");
    let nextButton = document.getElementById("nextBtn");
    let submitButton = document.querySelector('button[name="submit"]');
    let radioButtons = document.querySelectorAll('input[type="radio"][name="answer"]');

    if (submitButton && nextButton) {
        if (submitButton.disabled) {
            nextButton.style.display = "inline-block";
        } else {
            nextButton.style.display = "none";
        }
    }

    if (radioButtons.length > 0 && submitButton) {
        radioButtons.forEach(radio => {
            radio.addEventListener('change', () => {
                submitButton.disabled = false;
            });
        });
    }

    let retryButton = document.getElementById("retryBtn");
    if (retryButton) {
        retryButton.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("Retry Quiz Clicked!");

            window.location.href = retryButton.getAttribute("href");
        });
    }
});
