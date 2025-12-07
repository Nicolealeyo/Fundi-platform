"""
Quick test script to verify M-Pesa credentials and STK push
Run this from Django shell: python manage.py shell
Then: from services.mpesa_test import test_mpesa_connection
"""
from services.mpesa_utils import get_access_token, initiate_stk_push
from django.conf import settings


def test_mpesa_connection():
    """Test M-Pesa API connection"""
    print("=" * 50)
    print("Testing M-Pesa Connection")
    print("=" * 50)
    
    # Check settings
    print(f"\n1. Checking Settings:")
    print(f"   Consumer Key: {settings.MPESA_CONSUMER_KEY[:10]}...")
    print(f"   Consumer Secret: {settings.MPESA_CONSUMER_SECRET[:10]}...")
    print(f"   Shortcode: {settings.MPESA_SHORTCODE}")
    print(f"   Passkey: {settings.MPESA_PASSKEY[:20]}...")
    print(f"   API URL: {settings.MPESA_API_URL}")
    
    # Test access token
    print(f"\n2. Testing Access Token:")
    token = get_access_token()
    if token:
        print(f"   ✓ Access token obtained: {token[:20]}...")
    else:
        print(f"   ✗ Failed to get access token")
        return False
    
    # Test STK push (use test phone number)
    print(f"\n3. Testing STK Push:")
    test_phone = "254708374149"  # M-Pesa test number
    test_amount = 1
    callback_url = "https://example.com/callback"
    
    result = initiate_stk_push(
        phone_number=test_phone,
        amount=test_amount,
        account_reference="TEST123",
        transaction_desc="Test payment",
        callback_url=callback_url
    )
    
    if result.get('success'):
        print(f"   ✓ STK push initiated successfully!")
        print(f"   Merchant Request ID: {result.get('merchant_request_id')}")
        print(f"   Customer Message: {result.get('customer_message')}")
    else:
        print(f"   ✗ STK push failed: {result.get('error')}")
        print(f"   Error Code: {result.get('error_code', 'N/A')}")
    
    print("\n" + "=" * 50)
    return result.get('success', False)

