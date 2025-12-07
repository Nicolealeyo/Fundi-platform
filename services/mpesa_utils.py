"""
M-Pesa Daraja API Integration Utilities
"""
import requests
import base64
from datetime import datetime
from django.conf import settings
import json


def get_access_token():
    """
    Get M-Pesa OAuth access token
    """
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_base_url = settings.MPESA_API_URL
    
    # Safety check: Warn if using production API
    if 'api.safaricom.co.ke' in api_base_url and 'sandbox' not in api_base_url.lower():
        print("⚠️ WARNING: Using PRODUCTION M-Pesa API! Real money will be charged!")
        print("⚠️ To use sandbox (no real money), set MPESA_API_URL=https://sandbox.safaricom.co.ke")
    else:
        print(f"✓ Using M-Pesa Sandbox API (no real money): {api_base_url}")
    
    # M-Pesa API endpoint for OAuth
    api_url = api_base_url + "/oauth/v1/generate?grant_type=client_credentials"
    
    # Create base64 encoded string
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"M-Pesa Access Token Error - HTTP {response.status_code}: {response.text}")
            return None
        
        json_response = response.json()
        access_token = json_response.get('access_token')
        
        if access_token:
            print(f"M-Pesa Access Token obtained successfully")
        else:
            error_description = json_response.get('error_description', 'Unknown error')
            print(f"M-Pesa Access Token Error: {error_description}")
            print(f"Full response: {json_response}")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token (Network): {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        return None


def format_phone_number(phone_number):
    """
    Format phone number to M-Pesa format (254XXXXXXXXX)
    Accepts various formats: 0712345678, +254712345678, 254712345678, etc.
    """
    if not phone_number:
        return None
    
    # Remove any spaces, dashes, or plus signs
    phone = str(phone_number).strip().replace(" ", "").replace("-", "").replace("+", "")
    
    # Remove any non-digit characters (except for safety)
    phone = ''.join(filter(str.isdigit, phone))
    
    # If starts with 0, replace with 254 (Kenyan format: 0712345678 -> 254712345678)
    if phone.startswith("0") and len(phone) == 10:
        phone = "254" + phone[1:]
    
    # If doesn't start with 254, add it (for 9-digit numbers after removing 0)
    if not phone.startswith("254"):
        # If it's a 9-digit number, add 254
        if len(phone) == 9:
            phone = "254" + phone
        # If it's a 10-digit number starting with 7, add 254
        elif len(phone) == 10 and phone.startswith("7"):
            phone = "254" + phone
        # Otherwise, assume it needs 254 prefix
        elif len(phone) < 12:
            phone = "254" + phone
    
    # Validate final format (should be 254 followed by 9 digits = 12 digits total)
    if len(phone) == 12 and phone.startswith("254"):
        return phone
    else:
        # Return as-is if validation fails (let M-Pesa API handle validation)
        return phone


def initiate_stk_push(phone_number, amount, account_reference, transaction_desc, callback_url):
    """
    Initiate M-Pesa STK Push (Lipa na M-Pesa Online)
    
    Args:
        phone_number: Customer phone number
        amount: Amount to charge
        account_reference: Account reference (e.g., booking ID)
        transaction_desc: Transaction description
        callback_url: URL for M-Pesa to send payment result
    
    Returns:
        dict: Response from M-Pesa API
    """
    access_token = get_access_token()
    
    if not access_token:
        return {
            'success': False,
            'error': 'Failed to get access token'
        }
    
    # Format phone number
    formatted_phone = format_phone_number(phone_number)
    
    # Verify we're using sandbox API
    api_base_url = settings.MPESA_API_URL
    if 'api.safaricom.co.ke' in api_base_url and 'sandbox' not in api_base_url.lower():
        return {
            'success': False,
            'error': 'PRODUCTION API detected! Real money will be charged. Please use sandbox credentials. Set MPESA_API_URL=https://sandbox.safaricom.co.ke',
            'error_code': 'production_api_detected',
        }
    
    # M-Pesa API endpoint for STK push
    api_url = api_base_url + "/mpesa/stkpush/v1/processrequest"
    
    # Get timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Create password (base64 encoded)
    # Password = base64(Shortcode + Passkey + Timestamp)
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    password_string = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(password_string.encode()).decode()
    
    # Convert shortcode to integer if it's a string
    try:
        business_shortcode = int(shortcode) if isinstance(shortcode, str) else shortcode
    except (ValueError, TypeError):
        business_shortcode = shortcode
    
    # Request payload
    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": formatted_phone,
        "PartyB": business_shortcode,
        "PhoneNumber": formatted_phone,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    
    # Debug logging
    print(f"M-Pesa STK Push Request:")
    print(f"  URL: {api_url}")
    print(f"  Phone: {formatted_phone}")
    print(f"  Amount: {amount}")
    print(f"  Shortcode: {business_shortcode}")
    print(f"  Callback: {callback_url}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        # Log the response for debugging
        print(f"M-Pesa API Response Status: {response.status_code}")
        print(f"M-Pesa API Response: {response.text}")
        
        # Check HTTP status
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'HTTP Error {response.status_code}: {response.text}',
                'status_code': response.status_code
            }
        
        json_response = response.json()
        
        # Check if request was successful
        response_code = json_response.get('ResponseCode')
        if response_code == '0':
            return {
                'success': True,
                'merchant_request_id': json_response.get('MerchantRequestID'),
                'checkout_request_id': json_response.get('CheckoutRequestID'),
                'response_description': json_response.get('ResponseDescription'),
                'customer_message': json_response.get('CustomerMessage'),
                'raw_response': json_response
            }
        else:
            error_msg = json_response.get('ResponseDescription', 'Unknown error')
            error_code = json_response.get('ResponseCode', 'Unknown')
            print(f"M-Pesa Error - Code: {error_code}, Message: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'error_code': error_code,
                'raw_response': json_response
            }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout - M-Pesa API did not respond in time'
        }
    except requests.exceptions.RequestException as e:
        error_msg = f'Network error: {str(e)}'
        print(f"M-Pesa Network Error: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
    except json.JSONDecodeError as e:
        error_msg = f'Invalid JSON response: {str(e)}'
        print(f"M-Pesa JSON Error: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f'Error initiating STK push: {str(e)}'
        print(f"M-Pesa General Error: {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }


def query_stk_status(checkout_request_id):
    """
    Query the status of an STK push transaction
    
    Args:
        checkout_request_id: The checkout request ID from STK push
    
    Returns:
        dict: Status response from M-Pesa API
    """
    access_token = get_access_token()
    
    if not access_token:
        return {
            'success': False,
            'error': 'Failed to get access token'
        }
    
    api_url = settings.MPESA_API_URL + "/mpesa/stkpushquery/v1/query"
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    password_string = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(password_string.encode()).decode()
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        json_response = response.json()
        
        return {
            'success': True,
            'response_code': json_response.get('ResponseCode'),
            'response_description': json_response.get('ResponseDescription'),
            'merchant_request_id': json_response.get('MerchantRequestID'),
            'checkout_request_id': json_response.get('CheckoutRequestID'),
            'result_code': json_response.get('ResultCode'),
            'result_description': json_response.get('ResultDesc')
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error querying STK status: {str(e)}'
        }






