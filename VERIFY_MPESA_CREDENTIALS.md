# Fix "Wrong Credentials" Error

## Problem
Error: "Wrong credentials" (500.001.1001)

This means your Consumer Key, Consumer Secret, Shortcode, and Passkey don't match.

## Solution: Verify All Credentials Match

### Step 1: Check Your Daraja Portal

1. **Go to**: https://developer.safaricom.co.ke/
2. **Login** to your account
3. **Navigate to**: "My Apps" → Click on your app
4. **Important**: Make sure you're looking at the **"Lipa na M-Pesa Online"** or **"M-PESA EXPRESS"** section

### Step 2: Get ALL Credentials from the Same Section

In the **"Lipa na M-Pesa Online"** section, you should see:

1. **Consumer Key**: (from the app overview)
2. **Consumer Secret**: (from the app overview)
3. **Shortcode**: Should be `174379` for sandbox
4. **Passkey**: (from "Lipa na M-Pesa Online" → "Test Credentials")

**CRITICAL**: All these credentials must be from the SAME app and SAME product (Lipa na M-Pesa Online).

### Step 3: Common Issues

#### Issue 1: Consumer Key/Secret from Different App
- If you created a new app for shortcode 600000, those credentials won't work with shortcode 174379
- **Solution**: Use the Consumer Key/Secret from the app that has "Lipa na M-Pesa Online" enabled

#### Issue 2: Wrong Passkey
- The passkey for shortcode 174379 is different from shortcode 600000
- **Solution**: Get the passkey specifically from "Lipa na M-Pesa Online" section

#### Issue 3: App Not Configured for STK Push
- Make sure your app has "Lipa na M-Pesa Online" product enabled
- **Solution**: Enable "Lipa na M-Pesa Online" in your app settings

### Step 4: Update Your .env File

Once you have all the correct credentials from the same section:

```env
MPESA_CONSUMER_KEY=your_consumer_key_from_lipa_na_mpesa_online_app
MPESA_CONSUMER_SECRET=your_consumer_secret_from_lipa_na_mpesa_online_app
MPESA_SHORTCODE=174379
MPESA_PASSKEY=passkey_from_lipa_na_mpesa_online_test_credentials
MPESA_API_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://volitional-maximus-prewillingly.ngrok-free.dev/mpesa/callback/
```

### Step 5: Alternative - Use Standard Sandbox Credentials

If you're having trouble, you can test with the standard sandbox credentials:

1. Create a NEW app in Daraja portal
2. Select "Lipa na M-Pesa Online" product
3. Use the default test credentials provided
4. The shortcode should automatically be 174379

### Step 6: Verify Credentials Match

All credentials must be from:
- ✅ Same app
- ✅ Same product (Lipa na M-Pesa Online)
- ✅ Same environment (Sandbox)

## Quick Checklist

- [ ] Consumer Key from app with "Lipa na M-Pesa Online"
- [ ] Consumer Secret from same app
- [ ] Shortcode = 174379 (from Lipa na M-Pesa Online section)
- [ ] Passkey from "Lipa na M-Pesa Online" → "Test Credentials"
- [ ] All credentials are from Sandbox (not Production)

