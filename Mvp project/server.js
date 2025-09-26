const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const path = require("path");

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));
app.use(session({
  secret: "mvp-secret",
  resave: false,
  saveUninitialized: true
}));

// Temporary in-memory storage (replace with DB later)
let users = [];

// Home page
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Register route
app.post("/register", (req, res) => {
  const { username, password } = req.body;

  // Check if user already exists
  if (users.find(u => u.username === username)) {
    return res.send("User already exists! <a href='/register.html'>Try again</a>");
  }

  users.push({ username, password });
  res.redirect("/login.html");
});

// Login route
app.post("/login", (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);

  if (user) {
    req.session.user = user;
    res.redirect("/dashboard.html");
  } else {
    res.send("Invalid credentials. <a href='/login.html'>Try again</a>");
  }
});

// Logout route
app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/");
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
