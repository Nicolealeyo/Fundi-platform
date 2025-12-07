# How to Find Your M-Pesa Passkey

## Where to Find the Passkey

### Step 1: Go to Your Daraja Portal
1. Visit: https://developer.safaricom.co.ke/
2. Login to your account

### Step 2: Navigate to Your App
1. Click "My Apps"
2. Click on your app (the one with Consumer Key: TDkSzl8sSwdHCCrUeJb9SxMqv727Qb71Y9mInEEOptlnC1Rs)

### Step 3: Find Lipa na M-Pesa Online Section
1. Scroll down to find "Products" or "API Products" section
2. Look for **"Lipa na M-Pesa Online"** or **"M-PESA EXPRESS"** card/tile
3. Click on it

### Step 4: Get the Passkey
In the "Lipa na M-Pesa Online" section, you should see:

**Test Credentials:**
- **Shortcode**: 174379
- **Passkey**: [A long base64 string - this is what you need!]

The passkey will look something like:
```
bfb279f9aa9bdbcf158e97dd71a001ed3f
```
or a longer base64 string.

### Step 5: Copy the Passkey
Copy the entire passkey string and share it with me so I can update your `.env` file.

## Important Notes

- The passkey is different from the password
- Password = base64(Shortcode + Passkey + Timestamp) - this is generated dynamically
- Passkey = The static key from your Daraja portal
- You need the **Passkey**, not the Password

## If You Don't See Lipa na M-Pesa Online

If you don't see "Lipa na M-Pesa Online" in your app:

1. **Enable it**: Look for an "Enable" or "Activate" button
2. **Or create new app**: Create a new app and make sure to enable "Lipa na M-Pesa Online" during setup

## What the Passkey Looks Like

The passkey is usually:
- A long alphanumeric string (32+ characters)
- Sometimes shown as base64 encoded
- Found in "Test Credentials" section of "Lipa na M-Pesa Online"

Example format:
```
bfb279f9aa9bdbcf158e97dd71a001ed3f
```
or
```
YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkx
```

