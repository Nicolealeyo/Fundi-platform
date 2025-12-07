# Fix M-Pesa Shortcode Error

## Problem
Error: "Merchant does not exist" (500.001.1001)

This means the shortcode `600000` is not valid for STK Push in the sandbox.

## Solution: Get the Correct Shortcode

### Step 1: Check Your Daraja Portal

1. **Go to**: https://developer.safaricom.co.ke/
2. **Login** to your account
3. **Navigate to**: "My Apps" → Click on your app
4. **Find**: "Lipa na M-Pesa Online" or "M-PESA EXPRESS" section
5. **Look for**: "Test Credentials" or "Sandbox" section
6. **You should see**:
   - **Shortcode**: Usually `174379` for sandbox STK Push
   - **Passkey**: Your passkey (the long base64 string)

### Step 2: Update Your .env File

The shortcode for **Lipa na M-Pesa Online (STK Push)** is usually:
- **174379** (standard sandbox shortcode)

Update your `.env` file:

```env
MPESA_SHORTCODE=174379
```

**Important**: 
- `600000` is for C2B (Paybill) payments, NOT for STK Push
- `174379` is the standard sandbox shortcode for STK Push
- Make sure you're using the shortcode from the "Lipa na M-Pesa Online" section, not C2B

### Step 3: Verify Passkey

Make sure your passkey matches the one from "Lipa na M-Pesa Online" section, not C2B.

### Step 4: Restart Django Server

After updating `.env`:
```cmd
# Stop server (Ctrl+C)
python manage.py runserver
```

### Step 5: Test Again

Try the payment again - it should work now!

## Common Shortcodes

- **174379**: Standard sandbox shortcode for STK Push (Lipa na M-Pesa Online)
- **600000**: Usually for C2B (Paybill) payments, NOT for STK Push
- **Your custom shortcode**: If you have a reserved shortcode, use that

## Still Having Issues?

If you still get errors:
1. Double-check the shortcode in your Daraja portal
2. Make sure you're looking at "Lipa na M-Pesa Online" section, not C2B
3. Verify the passkey matches the shortcode
4. Check that your app has "Lipa na M-Pesa Online" product enabled

