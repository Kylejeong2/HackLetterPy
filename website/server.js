const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// PostgreSQL connection pool
const pool = new Pool({
    user: 'yourusername',
    host: 'localhost',
    database: 'yourdatabase',
    password: 'yourpassword',
    port: 5432,
});


app.use(bodyParser.urlencoded({ extended: true }));

app.post('/submit-email', async (req, res) => {
    const email = req.body.email;
    try {
        await pool.query('INSERT INTO emails (email) VALUES ($1)', [email]);
        res.send('Email submitted successfully!');
    } catch (err) {
        console.error(err);
        res.status(500).send('Error saving email to database.');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});