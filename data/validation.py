"""
Validation patterns for user input.

This module contains regular expression patterns used to validate
phone numbers and email addresses throughout the application.
"""

phone_number_pattern = r"^[0-9]{10}$"
email_address_pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"
