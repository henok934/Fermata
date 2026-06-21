# myapp/serializers.py
from rest_framework import serializers
from .models import Ticket, Bus, Feedback, City, Worker, CustomUser

from rest_framework import serializers
from .models import Route, Bus
class RSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'  # Or specify a list of fields you want to serialize

class BSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'  # Adjust fields as necessary



from rest_framework import serializers

class RecoverBalanceRequestSerializer(serializers.Serializer):
    refund_method = serializers.CharField(max_length=50, required=False, allow_blank=True)
    refund_account = serializers.CharField(max_length=50, required=False, allow_blank=True)
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    plate_no = serializers.CharField(max_length=50, required=False, allow_blank=True)
    side_no = serializers.CharField(max_length=50, required=False, allow_blank=True)
    price = serializers.CharField(max_length=50, required=False, allow_blank=True)
    depcity = serializers.CharField(max_length=50)
    descity = serializers.CharField(max_length=50)
    date = serializers.CharField(max_length=50)

from rest_framework import serializers
class CancelTicketRequestSerializer(serializers.Serializer):
    refund_method = serializers.CharField(max_length=50, help_text="e.g., CBE Birr, Telebirr")
    refund_account = serializers.CharField(max_length=50, help_text="Target bank account string")
    password = serializers.CharField(max_length=128, help_text="Password of the operator/user authorizing cancellation")
    
    # Hidden ticket tracking keys
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    plate_no = serializers.CharField(max_length=50)
    side_no = serializers.CharField(max_length=50)
    price = serializers.CharField(max_length=50, required=False)



"""
from rest_framework import serializers
class UserProfileSerializer(serializers.Serializer):
    # User Profile Fields
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    
    # System Statistics Field
    buschanges_count = serializers.IntegerField(
        help_text="Total number of bus changes recorded in the system"
    )
    class Meta:
        # If you want to link it to the model for more automatic field generation:
        # model = CustomUser
        # fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'buschanges_count']
        pass
"""



from rest_framework import serializers
class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    buschanges_count = serializers.IntegerField()



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        # Important: Mark auto-generated fields as read-only for Swagger
        read_only_fields = ('ticket_id', 'pnr', 'qr_code', 'booked_time')


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


"""
class BusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    class Meta:
        model = Bus
        fields = ['plate_no', 'sideno', 'no_seats', 'level', 'name']

    def create(self, validated_data):
        name = validated_data.pop('name')
        try:
            sc_instance = Sc.objects.get(name=name)
            validated_data['level'] = sc_instance.level
        except Sc.DoesNotExist:
            raise serializers.ValidationError({"name": "The selected name does not exist."})
        return Bus.objects.create(**validated_data)
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'city', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


"""
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
"""



class ActivateRequestSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="The date to fetch bus routes for.")

class RouteDataSerializer(serializers.Serializer):
    departure = serializers.CharField(source='depcity')
    destination = serializers.CharField(source='descity')
    date = serializers.DateField()
    side_no = serializers.CharField()

class ActivateResponseSerializer(serializers.Serializer):
    routes = RouteDataSerializer(many=True)
    buses_count = serializers.IntegerField()






from rest_framework import serializers
class CancelTicketRefundSerializer(serializers.Serializer):
    # Identifying the specific ticket
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    date = serializers.CharField()
    plate_no = serializers.CharField()
    side_no = serializers.CharField()

    # Refund destination details
    refund_method = serializers.ChoiceField(
        choices=['telebirr', 'cbe', 'boa', 'safaricom', 'awash'],
        help_text="The provider receiving the refund"
    )
    refund_account = serializers.CharField(help_text="Bank account or phone number")




from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message'] # Explicitly list fields for security

from rest_framework import serializers
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=['worker', 'user', 'sc'], required=True)

from rest_framework import serializers
from .models import Buschange, Service_fee, Worker, Feedback # and the others
class BuschangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buschange
        fields = '__all__'

class ServiceFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_fee
        fields = '__all__'


from rest_framework import serializers
class PaymentRequestSerializer(serializers.Serializer):
    PAYMENT_CHOICES = [
        ('cbe', 'Commercial Bank of Ethiopia (CBE)'),
        ('boa', 'Bank of Abyssinia (BOA)'),
        ('telebirr', 'Telebirr'),
        ('safaricom', 'M-PESA / Safaricom'),
        ('awash', 'Awash Bank'),
    ]
    payment_method = serializers.ChoiceField(choices=PAYMENT_CHOICES)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


from rest_framework import serializers
class BooksSearchRequestSerializer(serializers.Serializer):
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    date = serializers.CharField(help_text="Travel Date (YYYY-MM-DD)")


from rest_framework import serializers
class ChangePassengerRequestSerializer(serializers.Serializer):
    # Current Data (Identifying the ticket)
    firstname = serializers.CharField(help_text="Current First Name on ticket")
    lastname = serializers.CharField(help_text="Current Last Name on ticket")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    date = serializers.CharField(help_text="Travel Date (YYYY-MM-DD)")
    # New Data (The update)
    new_firstname = serializers.CharField(help_text="New First Name")
    new_lastname = serializers.CharField(help_text="New Last Name")
    new_phone = serializers.CharField(help_text="New Phone Number")
    new_gender = serializers.CharField(help_text="New gender")




"""
from rest_framework import serializers
from .models import Ticket, Sc
class ScSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = '__all__'  # Adjust fields as necessary
"""

from rest_framework import serializers
class ForgotPasswordSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=['user', 'sc'], required=True)


from rest_framework import serializers
class TicketSearchRequestSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="Travel date (YYYY-MM-DD)")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")

from rest_framework import serializers
from .models import Bus
class BusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__' # Or specific fields like ['plate_no', 'level', 'no_seats']

from rest_framework import serializers
from .models import Worker
class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__' # Or list specific fields like ['username', 'fname', 'lname', 'phone']

from rest_framework import serializers
from .models import Ticket, Route  # Adjust the import if your models are in a different location
class TickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # Ensure this is the correct model for tickets
        fields = ['firstname', 'lastname', 'phone', 'plate_no', 'date', 'depcity', 'descity', 'no_seat', 'price', 'side_no', 'passenger_type']

class TSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # Ensure this is the correct model for routes
        fields = '__all__'


from rest_framework import serializers
from .models import Feedback

class CommentteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'  # Or specify fields: ['id', 'user', 'comment', 'created_at']

from rest_framework import serializers
from .models import Route
class RoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'date', 'depcity', 'descity', 'plate_no', 'side_no']  # Include side_no


from rest_framework import serializers
class UpdateTicketRequestSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    depcity = serializers.CharField()
    descity = serializers.CharField()
    phone = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    email = serializers.EmailField()
    gender = serializers.CharField()
    plate_no = serializers.CharField()
    side_no = serializers.CharField()
    da = serializers.CharField(help_text="Original travel date (YYYY-MM-DD)")
    new_date = serializers.CharField(help_text="New travel date (YYYY-MM-DD)")

from rest_framework import serializers
class ActivateRequestSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="The date to check for active routes (YYYY-MM-DD)")


from rest_framework import serializers
class ActivateStatusUpdateSerializer(serializers.Serializer):
    depcity = serializers.CharField()
    descity = serializers.CharField()
    date = serializers.CharField(help_text="YYYY-MM-DD")
    kilometer = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    plate_no = serializers.CharField()
    is_active = serializers.BooleanField(help_text="Set to true to activate")

from rest_framework import serializers
class TelebirrPaymentSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10, min_length=10, help_text="09xxxxxxxx")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField()


from rest_framework import serializers
class TelebirrAuthSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10, help_text="Format: 09xxxxxxxx")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField(help_text="Amount to pay")

"""
from rest_framework import serializers
class CbeAuthSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=13, help_text="13-digit account starting with 1000")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField(help_text="The payment amount")
"""

from rest_framework import serializers
class CbeAuthSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=13, help_text="13-digit account starting with 1000")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField(help_text="The payment amount")

class CbeInputSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=13, help_text="13-digit account starting with 1000")
    price = serializers.FloatField(help_text="The amount to pay")

from rest_framework import serializers
class BoaInputSerializer(serializers.Serializer):
    account = serializers.CharField(
        min_length=8,
        max_length=8,
        help_text="8-digit account number starting with 48"
    )
    price = serializers.FloatField(
        help_text="The payment amount"
    )

from rest_framework import serializers
class BoaAuthSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=8, min_length=8)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField()

from rest_framework import serializers
class AwashInputSerializer(serializers.Serializer):
    account = serializers.CharField(
        max_length=13,
        min_length=13,
        help_text="13-digit Awash account number starting with 1000"
    )
    price = serializers.FloatField(
        help_text="The total amount to be paid"
    )
    
from rest_framework import serializers
class AwashAuthSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=13, min_length=13, help_text="13-digit account number")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    price = serializers.FloatField(help_text="Amount to be paid")

from rest_framework import serializers
class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True, style={'input_type': 'password'})
    newPassword = serializers.CharField(required=True, style={'input_type': 'password'})
    reNewPassword = serializers.CharField(required=True, style={'input_type': 'password'})

from rest_framework import serializers
class SafariPhoneSerializer(serializers.Serializer):
    # 'phone[]' is a common HTML naming convention, but in API logic 
    # we usually map it to 'phone' or 'phone_number'.
    phone = serializers.CharField(max_length=10, min_length=10, help_text="Safaricom phone number starting with 07")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


from rest_framework import serializers
class SafaricomAuthSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10, min_length=10)
    password = serializers.CharField(write_only=True)
    price = serializers.FloatField()

from rest_framework import serializers
from .models import Route, City  # Import your models
class RouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['depcity', 'descity', 'date', 'plate_no']  # Include necessary



from rest_framework import serializers
class TelebirrInitiateSerializer(serializers.Serializer):
    # Using 'phone' as the key; if your HTML uses name="phone[]", 
    # the serializer can still map it.
    phone = serializers.CharField(
        help_text="Phone number starting with 09 (e.g., 0912345678)",
        max_length=10,
        min_length=10
    )
    price = serializers.DecimalField(
        help_text="The payment amount",
        max_digits=10, 
        decimal_places=2
    )


"""
from rest_framework import serializers
class BusChangeInputSerializer(serializers.Serializer):
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    side_no = serializers.CharField(required=True)
    new_side_no = serializers.CharField(required=True)

class BusChangeResponseSerializer(serializers.Serializer):
    success = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    total_seats = serializers.IntegerField(required=False)
    booked_seats = serializers.IntegerField(required=False)
    remaining_seats = serializers.IntegerField(required=False)
    unbooked_seats = serializers.ListField(child=serializers.IntegerField(), required=False)
    booked_seat_list = serializers.ListField(child=serializers.IntegerField(), required=False)
    routes = serializers.ListField(child=serializers.DictField())
    buses = serializers.ListField(child=serializers.DictField())
"""


from rest_framework import serializers
class ActivateRequestSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="The date to check for active routes (YYYY-MM-DD)")
class RouteDisplaySerializer(serializers.Serializer):
    # This ensures Swagger shows the names you want
    departure = serializers.CharField(source='depcity') 
    destination = serializers.CharField(source='descity')
    date = serializers.DateField()
    side_no = serializers.CharField()

class ActivateResponseSerializer(serializers.Serializer):
    routes = RouteDisplaySerializer(many=True)
    buses_count = serializers.IntegerField()

from rest_framework import serializers
class ActivateRequestSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="The date to check for active routes (YYYY-MM-DD)")

class RouteDisplaySerializer(serializers.Serializer):
    # Mapping database field names to your desired Swagger display names
    departure = serializers.CharField(source='depcity') 
    destination = serializers.CharField(source='descity')
    date = serializers.DateField()
    side_no = serializers.CharField()

class ActivateResponseSerializer(serializers.Serializer):
    routes = RouteDisplaySerializer(many=True)
    buses_count = serializers.IntegerField()





from rest_framework import serializers
# This defines what one "Route" looks like in Swagger
class RouteListDisplaySerializer(serializers.Serializer):
    departure = serializers.CharField(source='depcity') # Maps depcity to "departure"
    destination = serializers.CharField(source='descity') # Maps descity to "destination"
    date = serializers.DateField()
    side_no = serializers.CharField()



from rest_framework import serializers
class WorkerDeleteRequestSerializer(serializers.Serializer):
    fname = serializers.CharField(required=True)
    lname = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)

class WorkerListSerializer(serializers.Serializer):
    fname = serializers.CharField()
    lname = serializers.CharField()
    username = serializers.CharField()
    phone = serializers.CharField()

class WorkerDeleteResponseSerializer(serializers.Serializer):
    success = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    admins = WorkerListSerializer(many=True, required=False)


from rest_framework import serializers
from rest_framework import serializers
# For GET response: List of cities
class CityListSerializer(serializers.Serializer):
    cities = serializers.ListField(child=serializers.CharField())

# For POST request: The search form fields
class TicketSearchRequestSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="YYYY-MM-DD")
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)

# For POST response: Error message structure
class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()



from rest_framework import serializers
# This serializer defines exactly what a single ticket looks like
class TicketDetailSerializer(serializers.Serializer):
    first_name = serializers.CharField(source='fname') # Maps fname to first_name
    last_name = serializers.CharField(source='lname')   # Maps lname to last_name
    phone = serializers.CharField()
    departure = serializers.CharField(source='depcity')
    destination = serializers.CharField(source='descity')
    date = serializers.DateField()
    plate_no = serializers.CharField()

# This defines the input fields for the Swagger UI form
class TicketDeleteSearchSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="YYYY-MM-DD")
    plate_no = serializers.CharField(required=True)
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)

# The final response structure for Swagger
class DeleteTicketsResponseSerializer(serializers.Serializer):
    route = TicketDetailSerializer(many=True, required=False)
    routes = serializers.ListField(child=serializers.DictField(), required=False)
    error = serializers.CharField(required=False)
from rest_framework import serializers

from rest_framework import serializers
# To describe individual bus change objects
class BusChangeDetailSerializer(serializers.Serializer):
    # Adjust these fields to match your actual Buschange model attributes
    date = serializers.DateField()
    old_bus = serializers.CharField(required=False)
    new_bus = serializers.CharField(required=False)
    reason = serializers.CharField(required=False)

# To describe the POST input (Search by date)
class BusChangeSearchSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="YYYY-MM-DD")

# To describe the final Response structure
class BusChangeResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False)
    buschange = BusChangeDetailSerializer(many=True, required=False)
    buschanges_count = serializers.IntegerField(required=False)
    error1 = serializers.CharField(required=False)
    # City names for the dropdown
    des = serializers.ListField(child=serializers.CharField(), required=False)


from rest_framework import serializers

# Renamed to avoid conflicts with other views
class BusManagementDisplaySerializer(serializers.Serializer):
    plate_no = serializers.CharField(label="Plate Number")
    sideno = serializers.CharField(label="Side Number")
    no_seats = serializers.IntegerField(label="Total Seats")

# Specific serializer for the Update/Post action
class BusChangeRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True)
    new_sideno = serializers.CharField(required=True)
    no_seats = serializers.IntegerField(required=True)




from rest_framework import serializers
# For the POST Request (The Search/Update Form)
class BusUpdateActionUniqueSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True)
    sideno = serializers.CharField(required=True, help_text="Current side number")
    new_sideno = serializers.CharField(required=True, help_text="The new side number to enter")
    no_seats = serializers.IntegerField(required=True)

# For the Response / Table Display
class BusManagementDisplayUniqueSerializer(serializers.Serializer):
    plate_no = serializers.CharField()
    sideno = serializers.CharField()
    no_seats = serializers.IntegerField()


from rest_framework import serializers

# POST Request: Defines the input fields in Swagger
class BusUpdateActionSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True)
    sideno = serializers.CharField(required=True, help_text="Current Side Number")
    new_sideno = serializers.CharField(required=True, help_text="Enter new side number here")
    no_seats = serializers.IntegerField(required=True)

# GET Response: Defines the table array format
class BusTableResponseSerializer(serializers.Serializer):
    plate_no = serializers.CharField()
    sideno = serializers.CharField()
    no_seats = serializers.IntegerField()



from rest_framework import serializers

# The "Fallback" route display when no tickets are found
class AvailableRouteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    depcity = serializers.CharField()
    descity = serializers.CharField()
    date = serializers.DateField()
    plate_no = serializers.CharField()
    side_no = serializers.CharField()

# The structured response for when tickets are NOT found
class TicketNotFoundErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
    routes = AvailableRouteSerializer(many=True)
    name = serializers.CharField(required=False)
    side = serializers.CharField(required=False)



from rest_framework import serializers

# Use this for both GET and POST responses to keep them consistent
class BusDeleteDisplaySerializer(serializers.Serializer):
    plate_no = serializers.CharField()
    sideno = serializers.CharField()
    no_seats = serializers.IntegerField()

from rest_framework import serializers

# Use this for both GET and POST responses to keep them consistent
class BusDeleteDisplaySerializer(serializers.Serializer):
    plate_no = serializers.CharField()
    sideno = serializers.CharField()
    no_seats = serializers.IntegerField()


from rest_framework import serializers
# Specific for Delete action: removes new_sideno
class BusDeleteActionSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True, help_text="Plate number of the bus to delete")
    sideno = serializers.CharField(required=True, help_text="Current side number")
    no_seats = serializers.IntegerField(required=True)

from rest_framework import serializers
# Controls the POST input in Swagger (Removes new_sideno)
class BusDeleteActionSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True)
    sideno = serializers.CharField(required=True)
    no_seats = serializers.IntegerField(required=True)

# Controls the table/array display in Swagger GET
class BusDeleteDisplaySerializer(serializers.Serializer):
    plate_no = serializers.CharField()
    sideno = serializers.CharField()
    no_seats = serializers.IntegerField()



"""
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bus, Sc
from .serializers import BusDeleteDisplaySerializer, BusUpdateActionSerializer

class BusDeleteViews(APIView):
    # This ensures the POST body stays correct as per your screenshot
    serializer_class = BusUpdateActionSerializer 

    def get_user_from_session(self, request):
        user_id = request.session.get('sc_id')
        return Sc.objects.filter(id=user_id).first() if user_id else None

    @extend_schema(
        summary="List buses available for deletion (Array Format)",
        responses={200: BusDeleteDisplaySerializer(many=True)} 
    )
    def get(self, request):
        sc_user = self.get_user_from_session(request)
        if not sc_user:
            return Response({"error": "Unauthorized"}, status=401)

        # Logic to get buses (reusing your existing filtering)
        buses = Bus.objects.filter(sideno__startswith=sc_user.side[:1]) 
        
        # This converts the data into the clean Array format you want
        serializer = BusDeleteDisplaySerializer(buses, many=True)
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'users/busdelete.html', {'buses': serializer.data})
            
        return Response(serializer.data)

    @extend_schema(
        summary="Delete a bus based on plate number",
        request=BusUpdateActionSerializer,
        responses={200: BusDeleteDisplaySerializer(many=True)}
    )
    def post(self, request):
        # Your existing delete logic...
        plate_no = request.data.get('plate_no')
        Bus.objects.filter(plate_no=plate_no).delete()
        
        # Return updated list in clean format
        sc_user = self.get_user_from_session(request)
        updated_buses = Bus.objects.filter(sideno__startswith=sc_user.side[:1])
        return Response(BusDeleteDisplaySerializer(updated_buses, many=True).data)
"""


from rest_framework import serializers
# For the GET response city list
class CityInfoSerializer(serializers.Serializer):
    cities = serializers.ListField(child=serializers.CharField())

# For the POST search form
class TicketInfoSearchSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="YYYY-MM-DD")
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)

# For the POST response route list
class TicketInfoResponseSerializer(serializers.Serializer):
    routes = serializers.ListField(child=serializers.DictField(), required=False)
    error = serializers.CharField(required=False)

class DeleteTicketsActionSerializer(serializers.Serializer):
    # Search fields
    date = serializers.DateField(required=True)
    plate_no = serializers.CharField(required=True)
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)
    
    # Optional fields for actual deletion
    firstname = serializers.CharField(required=False, help_text="First name of ticket holder to delete")
    lastname = serializers.CharField(required=False, help_text="Last name of ticket holder to delete")

class TicketTableDisplaySerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    phone = serializers.CharField()
    depcity = serializers.CharField()
    descity = serializers.CharField()
    date = serializers.DateField()
    plate_no = serializers.CharField()



from rest_framework import serializers
class TicketDeleteSearchSerializer(serializers.Serializer):
    date = serializers.DateField(required=True, help_text="YYYY-MM-DD")
    plate_no = serializers.CharField(required=True)
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)

class TicketDeleteResponseSerializer(serializers.Serializer):
    route = serializers.ListField(child=serializers.DictField(), required=False)
    routes = serializers.ListField(child=serializers.DictField(), required=False)
    error = serializers.CharField(required=False)


# serializers.py
from rest_framework import serializers

# ... other serializers ...

class RouteResponseSerializer(serializers.Serializer):
    routes = serializers.ListField(child=serializers.DictField(), required=False)
    error = serializers.CharField(required=False)
    cities = serializers.ListField(child=serializers.CharField(), required=False)

from rest_framework import serializers
class ServiceFeeSimpleSerializer(serializers.Serializer):
    service_fee = serializers.CharField()

class ServiceUpdateInputSerializer(serializers.Serializer):
    service_fee = serializers.CharField(required=True, help_text="The current fee to change")
    new_service_fee = serializers.CharField(required=True, help_text="The new fee value")


from rest_framework import serializers
class RouteDataSerializer(serializers.Serializer):
    # Mapping the database fields to the names you want in Swagger
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    date = serializers.DateField()
    side_no = serializers.CharField()
    plate_no = serializers.CharField()

class BusDataSerializer(serializers.Serializer):
    sideno = serializers.CharField()
    plate_no = serializers.CharField()
    no_seats = serializers.IntegerField()

class BusChangeInputSerializer(serializers.Serializer):
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    side_no = serializers.CharField(required=True)
    new_side_no = serializers.CharField(required=True)

class BusChangeResponseSerializer(serializers.Serializer):
    success = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    total_seats = serializers.IntegerField(required=False)
    booked_seats = serializers.IntegerField(required=False)
    remaining_seats = serializers.IntegerField(required=False)
    unbooked_seats = serializers.ListField(child=serializers.IntegerField(), required=False)
    booked_seat_list = serializers.ListField(child=serializers.IntegerField(), required=False)
    # Use the specific serializers here instead of DictField
    routes = RouteDataSerializer(many=True)
    buses = BusDataSerializer(many=True)




"""
from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


from rest_framework import serializers
from .models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'fname', 'lname', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
"""
"""
from rest_framework import serializers
class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker  # Replace with your actual model
        fields = '__all__'  # or a list of fields  BusesSerializer
"""


from rest_framework import serializers
class BusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus  # Replace with your actual model
        fields = '__all__'  # or a list of fields  BusesSerializer


from rest_framework import serializers
class CommentteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Replace with your actual model
        fields = '__all__'  # or a list of fields




"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Bus, Sc
class BusSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  # Ensure name is included
    class Meta:
        model = Bus
        fields = ['plate_no', 'sideno', 'no_seats', 'level', 'name', 'firstname', 'lastname', 'phone']

    def create(self, validated_data):
        # Retrieve the name from validated data
        name = validated_data.get('name')
        # Get the corresponding Sc instance
        try:
            sc_instance = Sc.objects.get(name=name)
            validated_data['level'] = sc_instance.level  # Set the level from Sc
        except Sc.DoesNotExist:
            raise serializers.ValidationError({"name": "The selected name does not exist."})
        # Create the Bus instance with the updated validated_data
        bus = Bus.objects.create(**validated_data)
        return bus
"""


from rest_framework import serializers
class SelectRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(help_text="Plate number of the bus")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    date = serializers.CharField(help_text="Date of travel (YYYY-MM-DD)")

class SelectResponseSerializer(serializers.Serializer):
    routes = serializers.ListField()
    levels = serializers.CharField()
    remaining_seats = serializers.IntegerField()
    unbooked_seats = serializers.ListField(child=serializers.IntegerField())
    booked_seats = serializers.ListField(child=serializers.IntegerField())
    all_seats = serializers.ListField(child=serializers.IntegerField())


from rest_framework import serializers
from .models import Route

# 1. This defines the input fields in the Swagger UI
class SeatLookupRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(max_length=20, help_text="Bus Plate Number")
    depcity = serializers.CharField(max_length=100, help_text="Departure City")
    descity = serializers.CharField(max_length=100, help_text="Destination City")
    date = serializers.CharField(max_length=20, help_text="Travel Date (YYYY-MM-DD)")

# 2. This defines the output structure in the Swagger UI
class SeatInfoResponseSerializer(serializers.Serializer):
    routes = serializers.ListField(child=serializers.DictField())
    levels = serializers.CharField()
    remaining_seats = serializers.IntegerField()
    unbooked_seats = serializers.ListField(child=serializers.IntegerField())
    booked_seats = serializers.ListField(child=serializers.IntegerField())
    all_seats = serializers.ListField(child=serializers.IntegerField())


from rest_framework import serializers

class TicketSearchSerializer(serializers.Serializer):
    plate_no = serializers.CharField(max_length=50, help_text="Bus Plate Number")
    side_no = serializers.CharField(max_length=50, help_text="Bus Side Number")
    date = serializers.CharField(max_length=20, help_text="Travel Date (YYYY-MM-DD)")
    depcity = serializers.CharField(max_length=100, help_text="Departure City")
    descity = serializers.CharField(max_length=100, help_text="Destination City")



from rest_framework import serializers

# This creates the input form in Swagger
class TicketSearchRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(required=True, help_text="Bus Plate Number")
    side_no = serializers.CharField(required=True, help_text="Bus Side Number")
    date = serializers.CharField(required=True, help_text="Travel Date (YYYY-MM-DD)")
    depcity = serializers.CharField(required=True, help_text="Departure City")
    descity = serializers.CharField(required=True, help_text="Destination City")

# This documents the API response structure
class TicketSearchResponseSerializer(serializers.Serializer):
    error = serializers.CharField(required=False)
    routes = serializers.ListField(child=serializers.DictField(), required=False)
    tickets = serializers.ListField(child=serializers.DictField(), required=False)



from rest_framework import serializers

class BookRequestSerializer(serializers.Serializer):
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    date = serializers.CharField(help_text="Travel Date (YYYY-MM-DD)")

class BookResponseSerializer(serializers.Serializer):
    routes = serializers.ListField(child=serializers.DictField())
    levels = serializers.CharField(required=False)
    buschanges_count = serializers.IntegerField()


from rest_framework import serializers
class TicketSearchSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    depcity = serializers.CharField(max_length=100)
    descity = serializers.CharField(max_length=100)
    date = serializers.DateField()


from rest_framework import serializers
from .models import Ticket

class TicketSearchSerializer(serializers.Serializer):
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    depcity = serializers.CharField(required=True)
    descity = serializers.CharField(required=True)
    date = serializers.DateField(required=True)

    def validate(self, data):
        """Cross-field validation for cities and names."""
        if data['depcity'] == data['descity']:
            raise serializers.ValidationError("Departure and Destination cannot be the same!")
        if data['firstname'] == data['lastname']:
            raise serializers.ValidationError("Firstname and Lastname cannot be the same!")
        return data

class TSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

from rest_framework import serializers

class AboutSerializer(serializers.Serializer):
    buschanges_count = serializers.IntegerField(help_text="The total number of bus changes available.")


from rest_framework import serializers
class TicketSearchRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(help_text="Bus Plate Number")
    side_no = serializers.CharField(help_text="Bus Side Number")
    date = serializers.CharField(help_text="Travel Date (YYYY-MM-DD)")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")


from rest_framework import serializers
"""
# For the POST request body
class BalanceSearchSerializer(serializers.Serializer):
    date = serializers.ListField(
        child=serializers.DateField(),
        help_text="List of dates to aggregate balance"
    )

# For the Response structure
class UserBalanceSerializer(serializers.Serializer):
    total_balance = serializers.FloatField()
    city = serializers.CharField()

class TotalBalanceResponseSerializer(serializers.Serializer):
    # This handles the dictionary output where keys are usernames
    totals = serializers.DictField(child=UserBalanceSerializer())
"""


from rest_framework import serializers
from .models import Ticket

# Used for the Swagger input schema
class BalanceSearchSerializer(serializers.Serializer):
    date = serializers.ListField(
        child=serializers.DateField(),
        help_text="List of dates (e.g. ['2026-01-19'])"
    )




from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

# Define the inner data structure
class UserBalanceSerializer(serializers.Serializer):
    total_balance = serializers.FloatField()
    city = serializers.CharField()

# The decorator below is the key to fixing the Warning
@extend_schema_serializer(component_name="TotalBalanceResponse")
class TotalBalanceResponseSerializer(serializers.Serializer):
    totals = serializers.DictField(child=UserBalanceSerializer())

# Your existing Ticket Serializer
class TSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

"""
from rest_framework import serializers
from .models import Sc, Service_fee
class scSerializer(serializers.ModelSerializer):  # Kept lowercase 's' to match your view implementation
    # Explicitly marking logo as an image field that is not required (optional)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Sc
        fields = '__all__'

    def create(self, validated_data):
        # 1. Pull the password out of the dictionary safely before instance initialization
        password = validated_data.pop('password', None)

        # 2. Initialize the Sc instance object with all remaining validated data (including files like logo)
        instance = Sc(**validated_data)

        # 3. Hash the password using the custom function built into your model
        if password:
            instance.set_password(password)

        # 4. Save to the database (This step triggers your custom dynamic file renaming function)
        instance.save()
        return instance
"""



class ServiceFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_fee
        fields = '__all__'

# For the POST request body
class ServiceUpdateInputSerializer(serializers.Serializer):
    service_fee = serializers.CharField(help_text="The current service fee value to change")
    new_service_fee = serializers.CharField(help_text="The new service fee value")


from rest_framework import serializers
from .models import Route

class SpecificFilterSerializer(serializers.Serializer):
    # Using 'from' and 'to' as field names to match your logic
    start_date = serializers.DateField(source='from', help_text="Start date (YYYY-MM-DD)")
    end_date = serializers.DateField(source='to', help_text="End date (YYYY-MM-DD)")

class RoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


from rest_framework import serializers

class TicketSearchSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Format: YYYY-MM-DD")
    plate_no = serializers.CharField(required=False, allow_blank=True)
    depcity = serializers.CharField()
    descity = serializers.CharField()




from rest_framework import serializers

class TicketSearchSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Format: YYYY-MM-DD")
    depcity = serializers.CharField(max_length=100)
    descity = serializers.CharField(max_length=100)


from rest_framework import serializers
class TicketDeletionSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Format: YYYY-MM-DD")
    plate_no = serializers.CharField(max_length=50)
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    depcity = serializers.CharField(max_length=100)
    descity = serializers.CharField(max_length=100)

from rest_framework import serializers
# Response Serializer: Fixes the 'SchemaValidationError'
class MessageSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="The response message from the server.")



class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True, min_length=8)
    reNewPassword = serializers.CharField(required=True)

    def validate(self, data):
        if data['newPassword'] != data['reNewPassword']:
            raise serializers.ValidationError({"reNewPassword": "Passwords do not match."})
        if data['currentPassword'] == data['newPassword']:
            raise serializers.ValidationError({"newPassword": "New password cannot be same as old."})
        return data




from rest_framework import serializers
"""
# FIX: This Serializer solves the "oneOf" SchemaValidationError
class PasswordStatusSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, help_text="Success message")
    error = serializers.CharField(required=False, help_text="Error message")
"""

class PasswordStatusSerializer(serializers.Serializer):
    # Use 'detail' to match the actual output the auditor found
    detail = serializers.CharField(help_text="Success or error message")
"""
# Input validation for the password change logic
class ChangePasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True, min_length=8)
    reNewPassword = serializers.CharField(required=True)
"""


from rest_framework import serializers
# 1. Used for Swagger Input fields
class SelectBusRequestSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="Date of travel (YYYY-MM-DD)")
    plate_no = serializers.CharField(help_text="Bus plate number")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")

# 2. Used to document the API response in Swagger
class SelectBusResponseSerializer(serializers.Serializer):
    route = serializers.ListField(required=False, help_text="List of found tickets")
    routes = serializers.ListField(required=False, help_text="Alternative available routes if no tickets found")
    error = serializers.CharField(required=False)




from rest_framework import serializers
from .models import Sc, Bus

"""
class ScSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = '__all__'
"""


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

# This serializer is specifically for the Swagger POST body documentation
class ScUpdateInputSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    new_email = serializers.EmailField()

from rest_framework import serializers

class ScUpdateSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(help_text="Current Email")
    new_email = serializers.EmailField(help_text="New Email to update")





from rest_framework import serializers
from .models import Sc
class ScSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = '__all__'  # Or list specific fields like ['firstname', 'lastname', 'email']


from rest_framework import serializers
class ScDeleteRequestSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)


from rest_framework import serializers
from .models import Bus, Route, Ticket, Buschange
class BusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buschange
        fields = ['plate_no', 'side_no', 'new_plate_no', 'new_side_no', 'date', 'depcity', 'descity']

class CSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['depcity']  # Adjust fields as needed

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['username', 'phone', 'password', 'fname', 'lname', 'city', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)




class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['username', 'phone', 'password', 'fname', 'lname', 'city', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Sc
class scSerializer(serializers.ModelSerializer):  # Matches your lowercase view implementation
    # 1. CRITICAL: Explicitly define the logo field so DRF registers binary streams
    logo = serializers.ImageField(required=False, allow_null=True)

    # 2. RELAX RULES: Prevents DRF validation failures if fields are left empty in the form
    firstname = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lastname = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Sc
        # 3. CRITICAL: Added 'logo' explicitly to the fields list
        fields = [
            'username', 'phone', 'password', 'name', 'side',
            'firstname', 'email', 'level', 'lastname', 'gender', 'logo'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # 4. Hash the password securely using your current setup
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        # 5. Save everything (including the logo file object) to the database
        return super().create(validated_data)









"""
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Worker, Service_fee
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['username', 'phone', 'password', 'fname', 'lname', 'city', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
"""


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['depcity']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_fee
        fields = ['service_fee']



"""
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Worker, Sc
class scSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sc
        fields = ['username', 'phone', 'password', 'name', 'side', 'firstname', 'email', 'level', 'lastname', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
"""


# This serializer is specifically for the Swagger POST request to match your HTML form
class RouteDeleteRequestSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="The travel date from the table")
    depcity = serializers.CharField(help_text="Departure City")
    descity = serializers.CharField(help_text="Destination City")
    plate_no = serializers.CharField(help_text="Vehicle Plate Number")
    side_no = serializers.CharField(help_text="Vehicle Side Number")



from rest_framework import serializers
from .models import Bus
class BusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['plate_no', 'sideno', 'no_seats']

"""
from rest_framework import serializers
from .models import Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message']
"""


"""
from rest_framework import serializers
class CommentDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email of the user")
    name = serializers.CharField(max_length=255, help_text="Name of the user")
    phone = serializers.CharField(max_length=15, help_text="Phone number of the user")
    registration_id = serializers.CharField(help_text="Unique registration ID of the comment")

"""


"""
from rest_framework import serializers
from .models import Route

# For the POST request body in Swagger
class SeatLookupRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(help_text="Plate number of the bus")
    depcity = serializers.CharField(help_text="Departure city")
    descity = serializers.CharField(help_text="Destination city")
    date = serializers.CharField(help_text="Travel date (e.g., YYYY-MM-DD)")

# For the response containing seat arrays
class SeatInfoResponseSerializer(serializers.Serializer):
    routes = serializers.ListField()
    levels = serializers.CharField()
    remaining_seats = serializers.IntegerField()
    unbooked_seats = serializers.ListField(child=serializers.IntegerField())
    booked_seats = serializers.ListField(child=serializers.IntegerField())
    all_seats = serializers.ListField(child=serializers.IntegerField())
"""

from rest_framework import serializers
from .models import Route

# For the POST request body in Swagger
class SeatLookupRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(help_text="Plate number of the bus")
    depcity = serializers.CharField(help_text="Departure city")
    descity = serializers.CharField(help_text="Destination city")
    date = serializers.CharField(help_text="Travel date (e.g., YYYY-MM-DD)")

# For the response containing seat arrays
class SeatInfoResponseSerializer(serializers.Serializer):
    routes = serializers.ListField()
    levels = serializers.CharField()
    remaining_seats = serializers.IntegerField()
    unbooked_seats = serializers.ListField(child=serializers.IntegerField())
    booked_seats = serializers.ListField(child=serializers.IntegerField())
    all_seats = serializers.ListField(child=serializers.IntegerField())


from rest_framework import serializers
from .models import CustomUser

class USerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Include the fields you want to see in Swagger/JSON
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'email']


class BusDeleteRequestSerializer(serializers.Serializer):
    plate_no = serializers.CharField(help_text="The plate number of the bus")
    sideno = serializers.CharField(help_text="The side number of the bus")
    no_seats = serializers.IntegerField(help_text="Number of seats in the bus")


from rest_framework import serializers
class CommentDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email of the user")
    name = serializers.CharField(max_length=255, help_text="Name of the user")
    phone = serializers.CharField(max_length=15, help_text="Phone number of the user")
    registration_id = serializers.CharField(help_text="Unique registration ID of the comment")


from rest_framework import serializers
from .models import CustomUser
# Serializer for the Response (shows all user data)
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'phone', 'email'] # Adjust fields as needed

# Serializer for the Request (Matches your HTML hidden inputs)
class AdminDeleteRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(help_text="First Name of the admin")
    last_name = serializers.CharField(help_text="Last Name of the admin")
    username = serializers.CharField(help_text="Username of the admin")
    phone = serializers.CharField(help_text="Phone number of the admin")


from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

