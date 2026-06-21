from django.urls import path
from .import views
from .views import Workerdelet,Special_activates,Subspecific,SubshowTicketsViewss,SpecialDeleteTickets, SpecialDeleteTicketsView, SpecialDeleteTicket, SpecialBuschange, Special_route_DeleteViews, Special_route, Special_active, BusDeleteViews, Recover_balanceView, CancelTicketView, ProfileView, LogoutView, DeleteTicketViews, TicketBookingViews, DeleteTicketsView, SeeView, Changepassenger, Activates, Activate, TicketBookingViews, Books, Totalballance,  Specific, Serviceupdate, MyBus, ServicInsertView, UpdateTicketViews, ScDeleteViews, Scchange,  Sce, SelView, MyRoute, BusInsertView, ShowTicketsViewss,ScInsertViews, BusInsertViews, Safaricompassword, ForgotPasswordView, Boapassword, Cbepassword, Awashpassword, Telebirrpassword, ShowTicketsViews,TelebirrPaymentView, SafariPaymentView, AwashPaymentView, CbePaymentView, BoaPaymentView, ProcessPaymentView, SelectView,ChangesBusView, ChangePasswordView, ChangeBusesViews, DeleteTickets, BusUpdateViewss, CommentDeleteViews, WorkerDeleteViews, RouteDeleteViews, CityDeleteViews, About, AdminDeleteViews, LoginView, HomeViews, BookView, GetTicketViews, CommentsView,  CityInsertView, RoutesInsertView, UrRegisterView, Workers, TicketInfoView, SelectBusView, Buse, Com, Rout, Use, Drivers, RouteView, SelectBusView, SelectView, ChangePasswordView, CommentsView, SelectBusView,  RouteView
from django.views.generic import RedirectView
from django.urls import path
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin  # ADD THIS LINE
from django.urls import path
urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('about/', About.as_view(), name='about'),
    path('cancel-ticket/', CancelTicketView.as_view(), name='cancel_ticket'),
    path('recover/', Recover_balanceView.as_view(), name='recover'),
    path('api/about/', About.as_view(), name='api_about'),  # Updated to 'api/about/'
    path('Select/', SelectView.as_view(), name='Select'),
    path('Sel/', SelView.as_view(), name='Sel'), # Unique name
    path('api/Sel/', SelView.as_view(), name='sel_api'), # Unique name    
    path('see/', SeeView.as_view(), name='see'),
    path('api/see/', SeeView.as_view(), name='api_see'),
    path('updatebus/', BusUpdateViewss.as_view(), name='updatebus'),
    path('special_active/', Special_active.as_view(), name='special_active'),
    #path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('specialdeletetickets/', SpecialDeleteTicketsView.as_view(), name='specialdeletetickets'),  # Use 'pk' to capture the ID
    path('Special_activates/', Special_activates.as_view(), name='special_activates'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    #path('login/forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),  # Existing line
    path('api/forgot_password/', ForgotPasswordView.as_view(), name='api_forgot_password'),
    path('comment/', CommentsView.as_view(), name='comment'),
    path('api/comment/', CommentsView.as_view(), name='api_comment'),
    path('subshowTicketsViewss/', SubshowTicketsViewss.as_view(), name='subshowTicketsViewss'),
    path('book/', BookView.as_view(), name='book'),
    path('api/book/', BookView.as_view(), name='api_book'),
    path('telebirr/', TelebirrPaymentView.as_view(), name='telebirr'),
    path('safari/', SafariPaymentView.as_view(), name='safari'),
    path('cbe/', CbePaymentView.as_view(), name='cbe'),
    path('boa/', BoaPaymentView.as_view(), name='boa'),
    path('awash/', AwashPaymentView.as_view(), name='awash'),
    path('cbepassword/', Cbepassword.as_view(), name='cbepassword'),
    path('boapassword/', Boapassword.as_view(), name='boapassword'),
    path('awashpassword/', Awashpassword.as_view(), name='awashpassword'),
    path('special_bus_change/', SpecialBuschange.as_view(), name='special_bus_change'),
    path('workerdelete/', Workerdelet.as_view(), name='workerdelete'),
    path('specialdeleteticket/', SpecialDeleteTicket.as_view(), name='specialdeleteticket'),  # Route for the JSON API
    path('special_route_delete/', Special_route_DeleteViews.as_view(), name='special_route_delete'),  # Serve form.html
    path('specialdeletetickets/', SpecialDeleteTickets.as_view(), name='specialdeletetickets'),  # Serve form.html
    #path('delete-tickets/', DeleteTicketsView.as_view(), name='delete_tickets'),
    path('delete_tickets/', DeleteTickets.as_view(), name='delete_tickets_web_search'),
    # 2. The Execution/Action View
    path('delete-tickets/', DeleteTicketsView.as_view(), name='delete_tickets_api_execution'),
    path('citydelete/', CityDeleteViews.as_view(), name='citydelete'), 
    #path('api/citydelete/', CityDeleteViews.as_view(), name='city_delete'),
    path('api/citydelete/', CityDeleteViews.as_view(), name='api_city_delete'),
    #path('api/city/delete/', CityDeleteViews.as_view(), name='city-delete'),
    path('busdelete/', BusDeleteViews.as_view(), name='busdelete'),
    #path('api/busdelete/', BusDeleteViews.as_view(), name='api_busdelete'),
    path('update_ticket/', UpdateTicketViews.as_view(), name='update_ticket'),
    path('specific/', Specific.as_view(), name='specific'),
    path('subspecific/', Subspecific.as_view(), name='subspecific'),
    path('get_ticket/', GetTicketViews.as_view(), name='get_ticket'),
    path('api/get_ticket/', GetTicketViews.as_view(), name='api_get_ticket'),  # API endpoint
    path('totalballance/', Totalballance.as_view(), name='totalballance'),  # URL for the bus insert view
    path('businsert/', BusInsertView.as_view(), name='businsert'),  # URL for the bus insert view
    path('activity/', Activates.as_view(), name='activity'),  # URL for the bus insert view
    path('booker/', Books.as_view(), name='booker'),  # API endpoint
    path('Showtickets', ShowTicketsViews.as_view(), name='Showtickets'),
    #path('Showticketss', ShowTicketsViewss.as_view(), name='Showticketss'),
    path('Showticketss/', ShowTicketsViewss.as_view(), name='Showticketss'),
    path('safaripassword/', Safaricompassword.as_view(), name='safaripassword'),  # API endpoint
    path('city/', CityInsertView.as_view(), name='city'),  # For rendering the form page
    path('service_fee/', ServicInsertView.as_view(), name='service_fee'),  # For rendering the form page
    path('api/service_fee/', ServicInsertView.as_view(), name='service_fee'),  # For rendering the form page
    path('api/city/', CityInsertView.as_view(), name='api_city'),  # API endpoint
    path('route/', RoutesInsertView.as_view(), name='route'),
    path('special_route/', Special_route.as_view(), name='special_route'),
    path('api/route/', RoutesInsertView.as_view(), name='api_route'),
    path('commentdelete/', CommentDeleteViews.as_view(), name='commentdelete'),
    path('api/commentdelete/', CommentDeleteViews.as_view(), name='api-commentdelete'),
    path('admindelete/', AdminDeleteViews.as_view(), name='admindelete'),
    path('scdelete/', ScDeleteViews.as_view(), name='scdelete'),
    path('api/admindelete/', AdminDeleteViews.as_view(), name='api_admindelete'),
    path('routedelete/', RouteDeleteViews.as_view(), name='routedelete'),
    path('api/routedelete/', RouteDeleteViews.as_view(), name='route-delete'),
    #path('route-lookup/', RouteLookupView.as_view(), name='route_lookup'),
    #path('delete-tickets/', DeleteTicketsView.as_view(), name='delete_tickets'),
    #path('bus-delete/', BusDeleteView.as_view(), name='bus_delete'),
    #path('api/buschanges/', RootView.as_view(), name='buschanges'),  # Adjust the path as needed
    #path('change-buses/', ChangeBusesView.as_view(), name='change_buses'),
    #path('change-bus/', ChangeBusView.as_view(), name='change_bus'),
    #path('ticketinfo/', views.ticketinfo, name='ticketinfo'),  # URL for the HTML registration form
    path('ticketinfo/', TicketInfoView.as_view(), name='ticketinfo'),  # URL for the ticket info view
    #path('api/registor/', RegisterView.as_view(), name='registor'),
    path('', HomeViews.as_view(), name='home'),
    path('api/home', HomeViews.as_view(), name='api_home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('users/', UsersView.as_view(), name='users'),
    #path('see/', SeeView.as_view(), name='see'),
    #path('routes/', RoutesView.as_view(), name='routes'),
    path('api/routes/', Rout.as_view(), name='routes_api'),
    path('routes/', Rout.as_view(), name='routes'),
    path('api/users/', Use.as_view(), name='users_api'),
    path('users/', Use.as_view(), name='users'),
    path('sce/', Sce.as_view(), name='sce'),
    path('passenger/', Changepassenger.as_view(), name='passenger'),
    #path('register/', RegisterView.as_view(), name='register'),
    #path('updatebus/', views.updatebus, name='updatebus'),
    #path('city-delete/', CityDeleteView.as_view(), name='city_delete'),
    #path('admin-delete/', AdminDeleteView.as_view(), name='admin_delete'),
    #path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    #path('comment-delete/', CommentDeleteView.as_view(), name='comment_delete'),
    #path('worker-delete/', WorkerDeleteView.as_view(), name='worker_delete'),
    path('api/buses/', Buse.as_view(), name='buses_api'),
    path('buses/', Buse.as_view(), name='buses'),
    path('mybus/', MyBus.as_view(), name='mybus'),
    #path('drivers/', MyDriver.as_view(), name='drivers'),
    path('myroute/',  MyRoute.as_view(), name='myroute'),
    #path('route-delete/', RouteDeleteView.as_view(), name='route_delete'),
    path('select-bus/', SelectBusView.as_view(), name='select_bus'),
    #path('check-delete-ticket/', CheckDeleteTicketView.as_view(), name='check_delete_ticket'),
    #path('check-route/', RouteCheckView.as_view(), name='check_route'),
    path('delete-ticket/', DeleteTicketViews.as_view(), name='delete_ticket'),
    
    #path('city/', CityView.as_view(), name='city'),
    path('sc/', ScInsertViews.as_view(), name='sc'),    
    path('worker/', Workers.as_view(), name='worker'),
    path('api/worker/', Workers.as_view(), name='api_worker'),
    path('registor/', UrRegisterView.as_view(), name='registor'),
    path('api/registor/', UrRegisterView.as_view(), name='api_user_register'),
    #path('book-ticket/', TicketBookingView.as_view(), name='book_ticket'),
    #path('api/tickets/', get_tickets, name='get_tickets'),  # New endpoint for retrieving tickets
    path('api/comments/', Com.as_view(),  name='comments_api'),
    path('comments/', Com.as_view(), name='comments'),
    path('api/driver/', Drivers.as_view(),  name='driver_api'),
    path('driver/', Drivers.as_view(), name='driver'),
    path('login/change_password/', ChangePasswordView.as_view(), name='login_change_password'),  # Define this route  
    path('api/routes/', Rout.as_view(), name='routes_api'),  # API endpoint
    path('routes/', Rout.as_view(), name='routes'),  # HTML page endpoint
    #path('update-bus/', UpdateBusView.as_view(), name='update_bus'),
    #path('city-delete/', CityDeleteView.as_view(), name='city_delete'),
    #path('admin-delete/', AdminDeleteView.as_view(), name='admin_delete'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    #path('comment-delete/', CommentDeleteView.as_view(), name='comment_delete'),
    #path('workerdelete/', WorkerDeleteView.as_view(), name='workerdelete'),
    #path('route-delete/', RouteDeleteView.as_view(), name='route_delete'),

    path('select-bus/', SelectBusView.as_view(), name='select_bus'),
    path('api/Select/', SelectView.as_view(), name='select_bus'),
    path('payment/', ProcessPaymentView.as_view(), name='payment'),
    path('api/payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('telebirr-password/', Telebirrpassword.as_view(), name='telebirr-password'),
    #path('Selectbus/', SelectBusView.as_view(), name='Selectbus'),  # URL for the SelectBus view
    # General URL (Used by your templates)
    path('Selectbus/', SelectBusView.as_view(), name='Selectbus'),
    # API URL (Used for mobile or external apps)
    path('api/Selectbus/', SelectBusView.as_view(), name='api_selectbus'),
    #path('api/ticket/', TicketBookingViews.as_view(), name='ticket'),
    #path('book-ticket/', TicketBookingView.as_view(), name='book_ticket'),
    #path('api/tickets/', get_tickets, name='get_tickets'),  # New endpoint for retrieving tickets
    
    #path('change_password/', ChangesPasswordView.as_view(), name='change_password'),
    #path('api/change_password/', ChangesPasswordView.as_view(), name='api_change_password'),  # Adding this line
    
    path('profile/change_password/', RedirectView.as_view(url='/change_password/', permanent=True)),
    

    #path('profile/', views.profile, name='profile'),ProfileView
    path('profile/', ProfileView.as_view(), name='profile'),
    path('custom_csrf_failure_view/', views.custom_csrf_failure_view, name='custom_csrf_failure_view'),
    
    path('login/', LoginView.as_view(), name='login'),
    #path('api/login/', LoginView.as_view(), name='api_login'),

    path('ticket/', TicketBookingViews.as_view(), name='ticket'),
    path('agentbooking/', TicketBookingViews.as_view(), name='agentbooking'),
    path('active/', Activate.as_view(), name='active'),
    #path('api/ticket/', TicketBookingViews.as_view(), name='api_ticket'),
    #path('root/', views.root, name='root'),
    path('changebus/', ChangesBusView.as_view(), name='changebus'),
    path('scupdate/', Scchange.as_view(), name='scupdate'),
    path('serviceupdate/', Serviceupdate.as_view(), name='serviceupdate'),
    path('changebuses/', ChangeBusesViews.as_view(), name='changebuses'),
]
