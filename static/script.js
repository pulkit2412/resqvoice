const BASE_URL = "http://127.0.0.1:5000";

// -------- REGISTER --------
async function register() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    alert(data.message);
}

// -------- LOGIN --------
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.success) {
        localStorage.setItem("user", email);
        window.location.href = "index.html";
    } else {
        alert("Invalid credentials");
    }
}

// -------- ADD CONTACT --------
async function addContact() {
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const user = localStorage.getItem("user");

    const res = await fetch(`${BASE_URL}/add_contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, name, phone })
    });

    const data = await res.json();
    alert(data.message);
}

// -------- SOS BUTTON --------
function sendSOS() {
    const user = localStorage.getItem("user");

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(async (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const res = await fetch(`${BASE_URL}/sos`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user,
                latitude,
                longitude
            })
        });

        const data = await res.json();
        alert("🚨 SOS SENT TO " + data.contacts_notified + " CONTACTS");
    });
}
