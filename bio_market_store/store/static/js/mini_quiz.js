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

document.addEventListener("DOMContentLoaded", () => {

    let progress = localStorage.getItem("quizProgress") ? parseInt(localStorage.getItem("quizProgress")) : 0;

    function updateProgressBar() {
        let progressBar = document.getElementById("progressBar");
        if (progressBar) {
            progressBar.style.width = progress + "%";
            progressBar.innerText = progress + "%";
            progressBar.setAttribute("aria-valuenow", progress);
        }
    }

    updateProgressBar();

    let nextButton = document.getElementById("nextBtn");
    if (nextButton) {
        nextButton.addEventListener("click", function () {
            if (progress < 100) {
                progress += 20;
                localStorage.setItem("quizProgress", progress);
                updateProgressBar();
            }
        });
    }

    let retryButton = document.getElementById("retryBtn");
    if (retryButton) {

        retryButton.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("Retry Quiz Clicked!");

            localStorage.removeItem("quizProgress");
            progress = 0;
            updateProgressBar();

            setTimeout(() => {
                window.location.href = retryButton.getAttribute("href");
            }, 100);
        });
    } else {
        console.log("Retry button NOT found! Check your HTML.");
    }
});
