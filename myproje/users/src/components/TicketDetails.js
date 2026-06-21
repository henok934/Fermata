import React from 'react';

const TicketDetails = ({ ticketInfo }) => {
    return (
        <div>
            <h2>Ticket Details</h2>
            <pre>{JSON.stringify(ticketInfo, null, 2)}</pre>
        </div>
    );
};

export default TicketDetails;
