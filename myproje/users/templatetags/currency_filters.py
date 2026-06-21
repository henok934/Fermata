from django import template
from num2words import num2words

register = template.Library()

@register.filter
def price_to_words_intl(value):
    try:
        amount = float(value)
        birr_val = int(amount)
        # Calculate cents/santim
        santim_val = int(round((amount - birr_val) * 100))

        # Convert numbers to English words
        birr_words = num2words(birr_val).upper()
        
        if santim_val > 0:
            santim_words = num2words(santim_val).upper()
            # This follows your requested format: [WORDS] BIRR KE [WORDS] SANTIM
            return f"{birr_words} BIRR WITH {santim_words} SANTIM"
        
        return f"{birr_words} BIRR"
    except (TypeError, ValueError):
        return value
