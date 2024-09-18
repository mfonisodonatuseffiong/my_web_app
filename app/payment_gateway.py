import random

def process_payment(amount):
    """
    Simulates payment processing.
    For now, it randomly returns a success or failure response.
    :param amount: The total amount to process.
    :return: A dictionary containing success status and message.
    """
    # Simulate a random outcome (success or failure)
    success = random.choice([True, False])
    
    if success:
        return {
            'success': True,
            'message': 'Payment processed successfully.'
        }
    else:
        return {
            'success': False,
            'message': 'Payment failed. Please try again.'
        }
