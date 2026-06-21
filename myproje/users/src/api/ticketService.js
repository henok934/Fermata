import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/ticket/';
const GET_TICKETS_URL = 'http://127.0.0.1:8000/api/tickets/';

export const bookTicket = async (ticketData) => {
    const response = await axios.post(API_URL, ticketData);
    return response.data;
};
