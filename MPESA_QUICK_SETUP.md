# Quick M-Pesa Setup Guide

## The Error You're Seeing
"M-Pesa payment failed: Authentication failed. Please check your M-Pesa credentials."

This means your M-Pesa credentials are not configured in the `.env` file.

## Quick Fix Steps

### Step 1: Get Your M-Pesa Credentials

1. **Go to**: https://developer.safaricom.co.ke/
2. **Sign up** or **Login** to your account
3. **Navigate to**: "My Apps" → Click on your app (or create a new one)
4. **Copy these values**:
   - **Consumer Key** (looks like: `abc123def456...`)
   - **Consumer Secret** (looks like: `xyz789uvw012...`)
   - **Shortcode** (usually `174379` for sandbox STK Push)
   - **Passkey** (long base64 string, found in "Lipa na M-Pesa Online" section)

### Step 2: Update Your .env File

Open your `.env` file and replace the placeholder values:

```env
MPESA_CONSUMER_KEY=your_actual_consumer_key_here
MPESA_CONSUMER_SECRET=your_actual_consumer_secret_here
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_actual_passkey_here
MPESA_API_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=http://localhost:8000/mpesa/callback/
```

**Important Notes:**
- Replace `your_actual_consumer_key_here` with your real Consumer Key
- Replace `your_actual_consumer_secret_here` with your real Consumer Secret
- Replace `your_actual_passkey_here` with your real Passkey
- **NO QUOTES** around the values
- **NO SPACES** before or after the `=` sign

### Step 3: For Local Testing with ngrok

If you're testing locally, you need to use ngrok for the callback URL:

1. **Start ngrok**: `ngrok http 8000`
2. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
3. **Update .env**:
   ```env
   MPESA_CALLBACK_URL=https://abc123.ngrok.io/mpesa/callback/
   ```

### Step 4: Restart Django Server

After updating `.env`, **restart your Django server**:

```bash
# Stop server (Ctrl+C)
python manage.py runserver
```

## Example .env File

```env
# Stripe (if needed)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# M-Pesa
MPESA_CONSUMER_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
MPESA_CONSUMER_SECRET=xyz789uvw012rst345def678ghi901jkl234mno567pqr890
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_API_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok.io/mpesa/callback/
```

## Common Issues

### Issue 1: "Invalid credentials"
- **Solution**: Double-check you copied the Consumer Key and Secret correctly
- Make sure there are no extra spaces or quotes

### Issue 2: "Merchant does not exist"
- **Solution**: Use shortcode `174379` for sandbox STK Push
- Make sure you're using the Passkey from "Lipa na M-Pesa Online" section, not C2B

### Issue 3: "Callback URL not accessible"
- **Solution**: Use ngrok for local testing
- Make sure the callback URL in `.env` matches your ngrok URL

## Test Numbers

For sandbox testing, you can use these test numbers:
- `254708374149`
- `254712345678`
- `254700000000`

## Still Having Issues?

1. Check your `.env` file format (no quotes, no spaces)
2. Verify credentials in M-Pesa Developer Portal
3. Make sure you restarted Django server after updating `.env`
4. Check Django server logs for detailed error messages

