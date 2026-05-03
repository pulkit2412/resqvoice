const BASE_URL = "https://resqvoice.onrender.com";

// GET USER SAFELY
function getUser() {
    const user = localStorage.getItem("user");

    if (!user) {
        alert("User not found. Please login again.");
        window.location.href = "/";
        return null;
    }

    return user.trim(); // 🔥 FIX: remove spaces/issues
}

// ADD CONTACT
async function addContact() {
    const user = getUser();
    if (!user) return;

    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();

    console.log("ADDING CONTACT FOR:", user); // DEBUG

    const res = await fetch(`${BASE_URL}/add_contact`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user, name, phone })
    });

    const data = await res.json();
    alert(data.message);

    loadContacts();
}

// LOAD CONTACTS
async function loadContacts() {
    const user = getUser();
    if (!user) return;

    console.log("LOADING CONTACTS FOR:", user); // DEBUG

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

// SOS
function sendSOS() {
    const user = getUser();
    if (!user) return;

    console.log("SENDING SOS FOR:", user); // DEBUG

    navigator.geolocation.getCurrentPosition(async (pos) => {
        const res = await fetch(`${BASE_URL}/sos`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user,
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude
            })
        });

        const data = await res.json();
        alert(`🚨 SOS SENT TO ${data.contacts_notified} CONTACTS`);
    });
}
