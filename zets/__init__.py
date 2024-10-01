# models/__init__.py
from .customer import Customer
from .campaign import Campaign
from .sms import SMS
# Add other models as needed

# Optionally export these models in __all__ for easier imports elsewhere
__all__ = ["Customer", "Campaign", "SMS"]
