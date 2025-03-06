document.addEventListener("DOMContentLoaded", function () {
    let tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    let minDate = tomorrow.toISOString().split("T")[0];
        document.getElementById("expDate").setAttribute("min", minDate);
        });