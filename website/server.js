const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ServerApiVersion } = require('mongodb');
// const uri = process.env.MONGODB_CONNECTION;

const app = express();
app.use(bodyParser.json());

const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: true,
      deprecationErrors: true,
    }
  });

async function run() {
  try {
    await client.connect();
    const database = client.db('hackletterpy');
    const collection = database.collection('emails');

    app.post('/submit-email', async (req, res) => {
      const { email } = req.body;
      if (!email) {
        console.log("No email")
        return res.status(400).json({ message: 'Email is required' });
      }
      try {
        await collection.insertOne({ email });
        console.log("Success")
        res.status(200).json({ message: 'Email saved successfully' });
      } catch (error) {
        console.log("Error Saving")
        res.status(500).json({ message: 'Error saving email' });
      }
    });

    app.listen(3000, () => {
      console.log('Server is running on port 3000');
    });

    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}

run().catch(console.dir);