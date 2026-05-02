function sendSOS() {
  navigator.geolocation.getCurrentPosition(position => {
    fetch('/sos', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      })
    })
    .then(res => res.json())
    .then(data => {
      alert("🚨 SOS SENT SUCCESSFULLY");
      console.log(data);
    });
  });
}