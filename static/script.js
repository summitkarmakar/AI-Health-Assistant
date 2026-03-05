console.log("JS Loaded Successfully");

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

async function sendMessage() {

    let input = document.getElementById("userInput").value;
    let chatBox = document.getElementById("chatBox");

    chatBox.innerHTML += "<p><b>You:</b> " + input + "</p>";

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ symptom: input })
    });

    const data = await response.json();

    chatBox.innerHTML += "<p><b>AI Doctor:</b> Possible disease: " + data.disease + "</p>";

    document.getElementById("userInput").value = "";
}
function calculateBMI() {
    let weight = document.getElementById("weight").value;
    let height = document.getElementById("height").value / 100;

    let bmi = (weight / (height * height)).toFixed(2);
    document.getElementById("bmiResult").innerText = "Your BMI: " + bmi;
}

function startWaterReminder() {
    document.getElementById("waterStatus").innerText = "Reminder Started (Every 1 hour)";
    setInterval(() => {
        alert("Time to drink water 💧");
    }, 3600000);
}

function setMedicineReminder() {
    let time = document.getElementById("medTime").value;
    document.getElementById("medStatus").innerText = "Medicine reminder set at " + time;
}

function bookAppointment() {
    alert("Appointment booked successfully!");
}

function findHospital() {
    alert("Redirecting to nearby hospitals...");
    window.open("https://www.google.com/maps/search/hospitals");
}

function callEmergency() {
    alert("Calling Ambulance 🚑");
}

