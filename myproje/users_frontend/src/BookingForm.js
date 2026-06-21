// src/BookingForm.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BookingForm = () => {
    const [depcity, setDepcity] = useState('');
    const [descity, setDescity] = useState('');
    const [date, setDate] = useState('');
    const [routes, setRoutes] = useState([]);
    const [error, setError] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        
        axios.post('/api/book/', { depcity, descity, date })
            .then(response => {
                setRoutes(response.data.routes);
                setError('');
            })
            .catch(error => {
                setError(error.response?.data.error || "An error occurred.");
                setRoutes([]);
            });
    };

    return (
        <div>
            <h1>Book a Bus Ticket</h1>
            <form onSubmit={handleSubmit} className="search_panel_content d-flex flex-column" style={{ margin: '10px 0', padding: '20px', backgroundColor: 'cyan', width: '200px', maxWidth: '700px' }}>
                <div className="search_item" style={{ margin: '5px 0', width: '100%' }}>
                    <label htmlFor="depcity" style={{ color: 'blue', fontWeight: 'bold' }}>From</label>
                    <input
                        type="text"
                        id="depcity_input"
                        value={depcity}
                        onChange={(e) => setDepcity(e.target.value)}
                        placeholder="Type to search..."
                        style={{ width: '100%', height: '45px', color: 'brown', textAlign: 'center' }}
                    />
                </div>

                <div className="search_item" style={{ margin: '5px 0', width: '100%' }}>
                    <label htmlFor="descity" style={{ color: 'blue', fontWeight: 'bold' }}>To</label>
                    <input
                        type="text"
                        id="descity_input"
                        value={descity}
                        onChange={(e) => setDescity(e.target.value)}
                        placeholder="Type to search..."
                        style={{ width: '100%', height: '45px', color: 'brown', textAlign: 'center' }}
                    />
                </div>

                <div className="search_item" style={{ margin: '5px 0', width: '100%' }}>
                    <label htmlFor="date" style={{ color: 'blue', fontWeight: 'bold' }}>Date</label>
                    <input
                        type="date"
                        id="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                        style={{ width: '100%', height: '45px', color: 'brown' }}
                    />
                </div>

                <div style={{ margin: '10px 0', textAlign: 'left' }}>
                    <button type="submit" style={{ backgroundColor: 'yellow', color: 'black', width: '130px', height: '45px', border: 'none' }}>
                        Search
                    </button>
                </div>
            </form>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {routes.length > 0 && (
                <div id="results">
                    <h2>Available Routes:</h2>
                    <ul>
                        {routes.map(route => (
                            <li key={route.route}>
                                Route ID: {route.route}, Plate Number: {route.plate_no}, Remaining Seats: {route.remaining_seats}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default BookingForm;
