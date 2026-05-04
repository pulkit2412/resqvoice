// -------- REGISTER --------
async function register() {
  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    const res = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    alert(data.message);

  } catch (err) {
    console.error("Register Error:", err);
    alert("Something went wrong in register");
  }
}


// -------- LOGIN --------
async function login() {
  try {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    const res = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.success) {
      localStorage.setItem("user", email);
      window.location.href = "/dashboard";
    } else {
      alert("Invalid credentials");
    }

  } catch (err) {
    console.error("Login Error:", err);
    alert("Something went wrong in login");
  }
}


// -------- SKIP --------
function skip() {
  window.location.href = "/dashboard";
}
