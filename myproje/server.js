const express = require('express');
const axios = require('axios');
const path = require('path'); // Import path module
const app = express();
const PORT = 3000;

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'build')));

// Define a route for the root URL to serve the React app
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Define a route that connects to the Django backend
app.get('/api', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:8000/api/'); // Adjust as needed
        res.json(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error fetching data from Django backend');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
