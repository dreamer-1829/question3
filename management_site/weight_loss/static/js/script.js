// Just a sample JS for interaction
document.addEventListener("DOMContentLoaded", function() {
    console.log("JS Loaded Successfully!");

    const message = document.getElementById("clickMessage");

    if (message) {
        message.addEventListener("click", function() {
            alert("Keep tracking your weight! You're doing great!");
        });
    }
});
