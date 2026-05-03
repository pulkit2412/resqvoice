const BASE_URL = "https://resqvoice.onrender.com";

// -------- GET USER --------
function getUser() {
    const user = localStorage.getItem("user");

    if (!user) {
        alert("Please login first");
        window.location.href = "/";
        return null;
    }

    return user.trim();
}

// -------- ADD CONTACT --------
async function addContact() {
    const user = getUser();
    if (!user) return;

    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();

    const res = await fetch(`${BASE_URL}/add_contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, name, phone })
    });

    const data = await res.json();
    alert(data.message);

    loadContacts();
}

// -------- LOAD CONTACTS --------
async function loadContacts() {
    const user = getUser();
    if (!user) return;

    const res = await fetch(`${BASE_URL}/get_contacts/${user}`);
    const data = await res.json();

    const list = document.getElementById("contacts");
    list.innerHTML = "";

    data.forEach(c => {
        const li = document.createElement("li");
        li.innerText = `${c.name} - ${c.phone}`;
        list.appendChild(li);
    });
}

// -------- SOS (WHATSAPP) --------
function sendSOS() {
    const user = getUser();
    if (!user) return;

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(async (pos) => {

        const res = await fetch(`${BASE_URL}/sos`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user,
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude
            })
        });

        const data = await res.json();

        const lat = data.latitude;
        const lon = data.longitude;

        const message = `🚨 SOS ALERT!
I need help!
Location: https://maps.google.com/?q=${lat},${lon}`;

        // 🔥 Open WhatsApp for each contact
        data.contacts.forEach(contact => {
            const phone = contact[1].replace("+", ""); // remove +
            const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;

            window.open(url, "_blank");
        });

        alert("WhatsApp opened for all contacts");
    });
}
