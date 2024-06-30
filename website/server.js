const express = require('express');
const mongoose = require('mongoose');
const path = require('path')
require('dotenv').config();

const uri = process.env.MONGODB_CONNECTION; //connection string

const app = express();
const port = process.env.PORT || 5000;

app.use(express.static(__dirname))
app.use(express.urlencoded({ extended: true }))

mongoose.connect(uri)
const db = mongoose.connection;

db.once('open', () => { //make sure it's connected
  console.log('Connected to MongoDB');
});

// Schema and Model
const emailSchema = new mongoose.Schema({
  email: String
})

const Email = mongoose.model('Email', emailSchema);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/post", async (req, res) => {
  const { email } = req.body;

  // Check if the email already exists
  const existingEmail = await Email.findOne({ email });

  if (existingEmail) {
    return res.status(400).send("Email already exists");
  }

  const newEmail = new Email({
    email
  });

  newEmail.save();
  console.log(newEmail); //testing

  res.send("You're in, first Hackletters are coming soon ...");
});

app.post("/unsubscribe", async (req, res) => {
  const { email } = req.body;
  const existingEmail = await Email.findOne({ email });

  if (existingEmail) {
    await Email.findOneAndDelete({ email });
    res.send("You're unsubscribed, sorry to see you go. To resubscribe, just visit hackletter.co and re-enter your email.");
  } else {
    res.status(404).send("Email not found");
  }
});

app.listen(port, () => {
  console.log('Server is running on port 3000');
});