const express = require('express');
const mongoose = require('mongoose');
const path = require('path')
require('dotenv').config();

const uri = process.env.MONGODB_CONNECTION; //connection string

const app = express();
const port = 3000;
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
  const { email } = req.body
  const newEmail = new Email({
    email
  })

  newEmail.save()
  console.log(newEmail) //testing

  res.send("Form Submission Successful")
});

app.listen(port, () => {
  console.log('Server is running on port 3000');
});