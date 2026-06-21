from django.test import TestCase, Client
from django.urls import reverse
from .models import Ticket

class TicketIntegrationTest(TestCase):
    def setUp(self):
        # Setup a dummy client and a sample ticket
        self.client = Client()
        self.ticket = Ticket.objects.create(
            plate_no="1234ET", 
            date="2026-03-20",
            firstname="Teklemariam",
            lastname="Mossie",
            phone="0911000000",
            depcity="Addis Ababa",
            descity="Hawassa"
        )

    def test_delete_ticket_logic(self):
        # 1. Simulate a session (since your view checks for user_id)
        session = self.client.session
        session['user_id'] = 1
        session.save()

        # 2. Call the API logic
        response = self.client.post(reverse('delete_tickets_api_execution'), {
            'plate_no': "1234ET",
            'date': "2026-03-20",
            'firstname': "Teklemariam",
            'lastname': "Mossie",
            'phone': "0911000000",
            'depcity': "Addis Ababa",
            'descity': "Hawassa"
        })

        # 3. Assert the ticket is actually gone from the database
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.count(), 0)
