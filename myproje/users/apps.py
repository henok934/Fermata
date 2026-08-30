"""
from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate
class YourAppConfig(AppConfig):
    name = 'users'
    def ready(self):
        # We connect the signal to run after migrations are done
        post_migrate.connect(create_default_user, sender=self)

def create_default_user(sender, **kwargs):
    from .models import CustomUser
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            # We use first_name and last_name (Django defaults)
            # instead of fname and lname
            CustomUser.objects.create_superuser(
                username='henok',
                email='henok@example.com',
                password='Super_admin@934',
                phone='0934567890',
                first_name='Henok',
                last_name='Mossie',
                city='Addis Ababa',

                # ---- ነባሪ የክፍያ አካውንት መረጃዎች ----
                cbe_account='1000123456789',        # የኢትዮጵያ ንግድ ባንክ አካውንት ቁጥር
                telebirr_account='0934567890',      # የቴሌብር ቁጥር (ብዙውን ጊዜ ከስልክ ቁጥር ጋር አንድ ነው)
                boa_account='45678912',             # የአቢሲኒያ ባንክ አካውንት ቁጥር
            )
            print("--- Default Superuser 'henok' with Payment Accounts created successfully ---")
    except Exception as e:
        print(f"--- Note: Admin auto-creation skipped: {e} ---")
"""
import uuid
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class YourAppConfig(AppConfig):
    name = 'users'

    def ready(self):
        # Connect the signal to run after migrations are done
        post_migrate.connect(initialize_default_data, sender=self)


def initialize_default_data(sender, **kwargs):
    from .models import CustomUser, City

    # 1. --- CLEAN LIST OF REQUIRED CITIES ---
    cities_list = [
        "Addisababa", "Abaala", "Autobustera", "Kality", "Asko", "Ayertena", "Lamberet", "Abiyaddi", "Abobo", "Adama", "Adet", "Addiszemen", 
        "Adigrat", "Adigudom", "Adiremets", "Adwa", "Afrera", "Agaro", "Akobo", "Axum", 
        "Alabakulito", "Alamata", "Alamahal", "Alemdegolowereilu", "Alemketema", 
        "Aletawondo", "Ambo", "Ameya", "Amibara", "Amstructural", "Amuru", "Anosire", 
        "Arbaminich", "Arere", "Arjogudetu", "Asayita", "Asella", "Asossa", "Ataye", 
        "Awash", "Awasharba", "Awbare", "Ayira", "Babillesomali", "Bahirdar", "Bako", 
        "Bambasi", "Bati", "Batu", "Bedelle", "Bega", "Berhale", "Bichena", "Birbir", 
        "Bishoftu", "Bonga", "Bulehora", "Bullene", "Bure", "Bureafar", "Buregambela", 
        "Bureoromia", "Butajira", "Chagni", "Chagnimetekel", "Chencha", "Chena", 
        "Chereti", "Chifra", "Chiro", "Dallol", "Dangila", "Dangur", "Danod", "Dansha", 
        "Debark", "Debirebirhan", "Debremarkos", "Debiresina", "Debiretabor", 
        "Debrezeitbenishangul", "Dedu", "Degehabur", "Dejen", "Dembecha", "Dembidollo", 
        "Dera", "Dessie", "Dibate", "Digotsion", "Dilla", "Dima", "Diredawa", "Ditre", 
        "Dolloado", "Dufti", "Durame", "Durbete", "Elkere", "Endabaguna", "Erebti", 
        "Erer", "Esite", "Fafan", "Feresbet", "Fiche", "Filtu", "Finchawabereha", 
        "Finchawaketema", "Finoteselam", "Galessa", "Gambela", "Gashamo", "Gawane", 
        "Geladin", "Gera", "Geregera", "Gewane", "Gidole", "Gilgelbeles", "Gimbi", 
        "Gimijabetazenayehu", "Goba", "Gode", "Goderesomali", "Gog", "Gonder", "Guba", 
        "Gulen", "Gundewoin", "Hamusit", "Harar", "Hararroadmojo", "Hargelle", 
        "Hawassa", "Hawzen", "Hosaena", "Humera", "Idagamamus", "Imey", "Inango", 
        "Injibara", "Itang", "Jaragedo", "Jiga", "Jigjiga", "Jimma", "Jinka", "Jikawo", 
        "Kake", "Kamashi", "Karati", "Kebribeyah", "Kebridahar", "Kelala", "Kelafo", 
        "Kemisie", "Kika", "Kobo", "Kobodeder", "Kombolcha", "Korem", "Kosober", 
        "Kurmuk", "Lalibela", "Lare", "Lera", "Limu", "Logiya", "Lumame", "Mankush", 
        "Maokomo", "Maychew", "Maykadra", "Mehoni", "Mekele", "Mendi", 
        "Mendibenishangul", "Merabete", "Mertolemariam", "Meskela", "Metema", 
        "Metar", "Metu", "Mille", "Mizan", "Mizanaman", "Modjo", "Mojo", "Motta", 
        "Mustahil", "Nazreth", "Negeleborena", "Nefasmewcha", "Nekemte", 
        "Odabuldigilu", "Pignudo", "Robie", "Sanja", "Sawla", "Sekota", "Selekleka", 
        "Semera", "Shambu", "Shashemene", "Sheraro", "Sherkole", "Sherkolegambela", 
        "Shewarobit", "Shilabo", "Shire", "Shishinda", "Sodo", "Tepi", "Teru", 
        "Togwajale", "Tongo", "Turmi", "Waliso", "Wardher", "Wayu", "Wegidi", 
        "Welayita", "Welayatiatercha", "Weldiya", "Wombera", "Woreta", "Woreilu", 
        "Wuchale", "Wukro", "Yabelo", "Yallo", "Yejube", "Yirgalem", "Yirgachefe"
    ]

    # 2. --- AUTO-POPULATE CITIES ---
    try:
        cities_to_create = []
        # Pull existing records to prevent crashing on duplicate runs
        existing_cities = set(City.objects.values_list('depcity', flat=True))

        for city_name in cities_list:
            if city_name not in existing_cities:
                cities_to_create.append(City(depcity=city_name))

        if cities_to_create:
            City.objects.bulk_create(cities_to_create)
            print(f"--- Successfully initialized {len(cities_to_create)} new routing cities ---")
    except Exception as e:
        print(f"--- Note: City auto-initialization skipped: {e} ---")

    # 3. --- AUTO-CREATE DEFAULT SUPERUSER ---
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            CustomUser.objects.create_superuser(
                username='henok',
                email='henok@example.com',
                password='Super_admin@934',
                phone='0934567890',
                first_name='Henok',
                last_name='Mossie',
                city='Addis Ababa',
                cbe_account='1000123456789',
                telebirr_account='0934567890',
                boa_account='45678912',
            )
            print("--- Default Superuser 'henok' with Payment Accounts created successfully ---")
    except Exception as e:
        print(f"--- Note: Admin auto-creation skipped: {e} ---")

