// src/components/Home.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Home = () => {
    const [buschangesCount, setBuschangesCount] = useState(0);
    const [cities, setCities] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/'); // Adjust if necessary
                setBuschangesCount(response.data.buschanges_count);
                setCities(response.data.cities);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
            <h1>Welcome to the Bus Ticket Booking System</h1>
            <h2>Bus Changes Count: {buschangesCount}</h2>
            <h3>Cities:</h3>
            <ul>
                {cities.map((city, index) => (
                    <li key={index}>{city}</li>
                ))}
            </ul>
        </div>
    );
};

export default Home;
