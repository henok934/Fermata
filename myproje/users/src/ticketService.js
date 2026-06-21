import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/ticket/';

export const bookTicket = async (ticketData) => {
    const response = await axios.post(API_URL, ticketData); // Ensure this is a POST request
    return response.data; // Return the response data
};
