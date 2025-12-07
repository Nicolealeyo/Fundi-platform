# How to Ensure M-Pesa is in Sandbox Mode (No Real Money)

## ⚠️ IMPORTANT: If Real Money is Being Deducted

If M-Pesa is deducting **real money** from your account, you're likely using **PRODUCTION credentials** instead of **SANDBOX/TEST credentials**.

## Quick Fix

### Step 1: Verify Your .env File

Make sure your `.env` file has:

```env
MPESA_API_URL=https://sandbox.safaricom.co.ke
```

**NOT:**
```env
MPESA_API_URL=https://api.safaricom.co.ke  # ❌ This is PRODUCTION!
```

### Step 2: Get Sandbox/Test Credentials

1. **Go to**: https://developer.safaricom.co.ke/
2. **Login** to your account
3. **Navigate to**: "My Apps" → Select your app
4. **Look for**: "Sandbox" or "Test" section
5. **Get these credentials**:
   - Consumer Key (from Sandbox/Test section)
   - Consumer Secret (from Sandbox/Test section)
   - Shortcode: `174379` (standard sandbox shortcode)
   - Passkey (from "Lipa na M-Pesa Online" → Test Credentials)

### Step 3: Update Your .env File

Replace your current credentials with **SANDBOX credentials**:

```env
MPESA_CONSUMER_KEY=your_sandbox_consumer_key
MPESA_CONSUMER_SECRET=your_sandbox_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_sandbox_passkey
MPESA_API_URL=https://sandbox.safaricom.co.ke
```

### Step 4: Restart Django Server

After updating `.env`:
```bash
# Stop server (Ctrl+C)
python manage.py runserver
```

## How to Identify Sandbox vs Production

### Sandbox Credentials:
- ✅ API URL: `https://sandbox.safaricom.co.ke`
- ✅ Shortcode: Usually `174379` for STK Push
- ✅ No real money deducted
- ✅ Test phone numbers work
- ✅ Consumer Key/Secret from "Sandbox" or "Test" section

### Production Credentials:
- ❌ API URL: `https://api.safaricom.co.ke`
- ❌ Shortcode: Your business Paybill/Till number
- ❌ **REAL MONEY WILL BE DEDUCTED**
- ❌ Requires production approval
- ❌ Consumer Key/Secret from "Production" section

## Test Phone Numbers (Sandbox Only)

In sandbox mode, you can use these test numbers:
- `254708374149`
- `254712345678`
- `254700000000`
- `254711111111`

**Note**: These only work in sandbox mode. In production, you must use real M-Pesa registered numbers.

## Safety Features Added

The system now:
1. ✅ Checks if you're using production API and warns you
2. ✅ Shows warning in payment form
3. ✅ Logs sandbox mode status in server logs
4. ✅ Blocks production API if accidentally configured

## Verify You're in Sandbox

After restarting your server, check the Django terminal logs. You should see:
```
✓ Using M-Pesa Sandbox API (no real money): https://sandbox.safaricom.co.ke
```

If you see:
```
⚠️ WARNING: Using PRODUCTION M-Pesa API! Real money will be charged!
```

**STOP** and switch to sandbox credentials immediately!

## Still Having Issues?

1. **Double-check** your M-Pesa Developer Portal - make sure you're copying credentials from the **Sandbox/Test** section, not Production
2. **Verify** your `.env` file has `MPESA_API_URL=https://sandbox.safaricom.co.ke`
3. **Restart** your Django server after making changes
4. **Check** Django server logs for sandbox confirmation

## Contact M-Pesa Support

If you've been charged real money and need help:
- Contact Safaricom M-Pesa Support
- Check your M-Pesa statement
- Review transactions in your M-Pesa Developer Portal

