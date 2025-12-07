"""
M-Pesa Webhook/Callback Views
"""
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json
from .models import Payment
from django.utils import timezone


@csrf_exempt
def mpesa_callback(request):
    """
    Handle M-Pesa STK Push callback/webhook
    This endpoint receives payment results from M-Pesa
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Parse the callback data
        callback_data = json.loads(request.body)
        
        # Extract relevant information
        body = callback_data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        merchant_request_id = stk_callback.get('MerchantRequestID', '')
        checkout_request_id = stk_callback.get('CheckoutRequestID', '')
        result_code = stk_callback.get('ResultCode', '')
        result_description = stk_callback.get('ResultDesc', '')
        
        # Find the payment by checkout_request_id
        try:
            payment = Payment.objects.get(checkout_request_id=checkout_request_id)
            print(f"M-Pesa Callback - Found payment: ID={payment.id}, Current Status={payment.status}, Booking ID={payment.booking.id}")
        except Payment.DoesNotExist:
            # Try to find by merchant_request_id as fallback
            try:
                payment = Payment.objects.get(merchant_request_id=merchant_request_id)
                print(f"M-Pesa Callback - Found payment by merchant_request_id: ID={payment.id}")
            except Payment.DoesNotExist:
                print(f"M-Pesa Callback - Payment not found. CheckoutRequestID: {checkout_request_id}, MerchantRequestID: {merchant_request_id}")
                return JsonResponse({
                    'ResultCode': 1,
                    'ResultDesc': 'Payment not found'
                })
        
        # Check result code
        # ResultCode 0 = Success
        print(f"M-Pesa Callback - ResultCode: {result_code}, ResultDesc: {result_description}")
        
        if result_code == 0:
            # Payment successful
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            
            # Extract transaction details
            transaction_id = None
            amount = None
            
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    transaction_id = item.get('Value')
                elif item.get('Name') == 'Amount':
                    amount = item.get('Value')
            
            print(f"M-Pesa Callback - Payment successful. Transaction ID: {transaction_id}, Amount: {amount}")
            
            # Update payment
            payment.status = 'completed'
            payment.transaction_id = transaction_id or checkout_request_id
            payment.completed_at = timezone.now()
            payment.save()
            
            print(f"M-Pesa Callback - Payment #{payment.id} updated to completed. Booking ID: {payment.booking.id}")
            
            # Automatically update booking status to completed when payment is completed
            booking = payment.booking
            if booking.status != 'completed':
                booking.status = 'completed'
                booking.save()
                print(f"M-Pesa Callback - Booking #{booking.id} updated to completed")
            
            return JsonResponse({
                'ResultCode': 0,
                'ResultDesc': 'Payment processed successfully'
            })
        else:
            # Payment failed
            payment.status = 'failed'
            payment.save()
            
            return JsonResponse({
                'ResultCode': 0,  # Acknowledge receipt
                'ResultDesc': 'Payment failed - ' + result_description
            })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'ResultCode': 1,
            'ResultDesc': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        # Log the error
        print(f"M-Pesa callback error: {str(e)}")
        return JsonResponse({
            'ResultCode': 1,
            'ResultDesc': 'Error processing callback'
        }, status=500)






