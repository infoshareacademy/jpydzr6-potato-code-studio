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
    if (!stateSelect) {
        return `Element ${stateSelect} not found!`;
    }
    states.forEach(state => {
        const option = document.createElement("option");
        option.value = state;
        option.textContent = state;
        if(!option){
            return `Element ${option} not found!`;
        }

        stateSelect.appendChild(option);
    });
});
