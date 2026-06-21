import React, { useState, useEffect } from 'react';
import { bookTicket, getTickets } from '../api/ticketService';

const BookingForm = () => {
    const [formData, setFormData] = useState({
        firstname: '',
        lastname: '',
        phone: '',
        depcity: '',
        descity: '',
        date: '',
        no_seat: '',
        price: '',
        side_no: '',
        plate_no: ''
    });

    const [tickets, setTickets] = useState([]);
    const [ticketInfo, setTicketInfo] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await bookTicket(formData);
            setTicketInfo(response);
            fetchTickets(); // Fetch updated tickets after booking
            resetForm();
        } catch (error) {
            setError('Error: ' + (error.response ? error.response.data : 'Network error'));
        }
    };

    const fetchTickets = async () => {
        try {
            const response = await getTickets();
            setTickets(response);
        } catch (error) {
            setError('Error fetching tickets: ' + (error.response ? error.response.data : 'Network error'));
        }
    };

    const resetForm = () => {
        setFormData({
            firstname: '',
            lastname: '',
            phone: '',
            depcity: '',
            descity: '',
            date: '',
            no_seat: '',
            price: '',
            side_no: '',
            plate_no: ''
        });
    };

    useEffect(() => {
        fetchTickets(); // Fetch tickets when the component mounts
    }, []);

    return (
        <div>
            <h1>Book a Ticket</h1>
            <form onSubmit={handleSubmit}>
                {Object.keys(formData).map((key) => (
                    <div key={key}>
                        <label>{key.charAt(0).toUpperCase() + key.slice(1)}:</label>
                        <input
                            type={key === 'date' ? 'date' : 'text'}
                            name={key}
                            value={formData[key]}
                            onChange={handleChange}
                            required
                        /><br />
                    </div>
                ))}
                <button type="submit">Book Ticket</button>
            </form>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {ticketInfo && (
                <div>
                    <h2>Ticket Booked Successfully!</h2>
                    <pre>{JSON.stringify(ticketInfo, null, 2)}</pre>
                </div>
            )}

            <h2>Booked Tickets</h2>
            <ul>
                {tickets.map((ticket) => (
                    <li key={ticket.id}>
                        {ticket.firstname} {ticket.lastname} - {ticket.date}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default BookingForm;
