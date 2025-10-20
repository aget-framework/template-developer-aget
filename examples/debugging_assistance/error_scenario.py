#!/usr/bin/env python3
"""Sample code that triggers an AttributeError.

This demonstrates a common bug pattern: accessing an attribute on None.
"""


def get_user_email(user_id):
    """Fetch user and return email."""
    # Simulated database query
    # In real code, this might return None if user not found
    if user_id == 123:
        return {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com"
        }
    else:
        # User not found - returns None
        return None


def process_email(user_id):
    """Process user email - contains bug."""
    user = get_user_email(user_id)

    # BUG: No null check before accessing attribute
    # This will fail if user is None
    email_parts = user['email'].split('@')

    username = email_parts[0]
    domain = email_parts[1]

    print(f"Username: {username}")
    print(f"Domain: {domain}")


if __name__ == "__main__":
    # This will work
    print("Processing user 123:")
    process_email(123)

    print()

    # This will trigger AttributeError
    print("Processing user 999 (not found):")
    try:
        process_email(999)
    except (AttributeError, TypeError) as e:
        print(f"Error occurred: {type(e).__name__}: {e}")
