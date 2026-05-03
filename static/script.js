const BASE_URL = "https://resqvoice.onrender.com";

// ADD CONTACT
async function addContact() {
    const user = localStorage.getItem("user");
    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;

    const res = await fetch(`${BASE_URL}/add_contact`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user, name, phone })
    });

    const data = await res.json();
    alert(data.message);

    loadContacts(); // refresh
}

// LOAD CONTACTS
async function loadContacts() {
    const user = localStorage.getItem("user");

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
    const user = localStorage.getItem("user");

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
