function getUser() {
  return localStorage.getItem("user");
}

async function addContact() {
  const user = getUser();
  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;

  const res = await fetch("/add_contact", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ user, name, phone })
  });

  const data = await res.json();
  alert(data.message);
  loadContacts();
}

async function loadContacts() {
  const user = getUser();

  const res = await fetch(`/get_contacts/${user}`);
  const data = await res.json();

  const list = document.getElementById("contacts");
  list.innerHTML = "";

  data.forEach(c => {
    const li = document.createElement("li");
    li.innerText = `${c.name} - ${c.phone}`;
    list.appendChild(li);
  });
}

function sendSOS() {
  const user = getUser();

  navigator.geolocation.getCurrentPosition(async (pos) => {

    const res = await fetch("/sos", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        user,
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      })
    });

    const data = await res.json();

    const message = `🚨 SOS ALERT! Location: https://maps.google.com/?q=${data.latitude},${data.longitude}`;

    data.contacts.forEach(c => {
      const phone = c[1].replace("+", "");
      window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`);
    });
  });
}

window.onload = loadContacts;
