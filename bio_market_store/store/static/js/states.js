const states = [
    "Lower Silesia",
    "Kuyavia-Pomerania",
    "Lodzkie",
    "Lublin",
    "Lubusz",
    "Lesser Poland",
    "Masovia",
    "Subcarpathian",
    "Pomerania",
    "West Pomerania",
    "Greater Poland",
    "Podlaskie",
    "Świętokrzyskie",
    "Opolskie"
];

document.addEventListener("DOMContentLoaded", () => {
    const stateSelect = document.getElementById("state");

    states.forEach(state => {
        const option = document.createElement("option");
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
    });
});