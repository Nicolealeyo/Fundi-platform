# M-Pesa Production Integration Guide

## Moving from Sandbox to Production

This guide will help you integrate M-Pesa for **real money payments** in production.

## Prerequisites

1. **Business Registration**: You must have a registered business in Kenya
2. **M-Pesa Business Account**: Apply for M-Pesa Business services
3. **Daraja API Access**: Apply for production API access
4. **Production Credentials**: Get approved production credentials from Safaricom

## Step 1: Apply for Production Access

### 1.1 Business Requirements
- Registered business in Kenya
- Valid business registration documents
- Business bank account
- Tax compliance (KRA PIN)

### 1.2 Apply Through Safaricom
1. Go to: https://developer.safaricom.co.ke/
2. Login to your account
3. Navigate to "My Apps"
4. Click "Request Production Access" or "Apply for Production"
5. Fill out the application form with:
   - Business details
   - Business registration documents
   - Bank account information
   - Use case description
6. Submit and wait for approval (usually 1-2 weeks)

## Step 2: Get Production Credentials

Once approved, you'll receive:

1. **Production Consumer Key**
2. **Production Consumer Secret**
3. **Production Shortcode** (your business Paybill/Till number)
4. **Production Passkey** (from "Lipa na M-Pesa Online" in production)
5. **Initiator Name** (if using B2C/B2B)
6. **Initiator Password** (if using B2C/B2B)

## Step 3: Update Your Settings

### 3.1 Update .env File

```env
# Production M-Pesa Settings
MPESA_CONSUMER_KEY=your_production_consumer_key
MPESA_CONSUMER_SECRET=your_production_consumer_secret
MPESA_SHORTCODE=your_production_shortcode
MPESA_PASSKEY=your_production_passkey
MPESA_API_URL=https://api.safaricom.co.ke
MPESA_CALLBACK_URL=https://yourdomain.com/mpesa/callback/
```

### 3.2 Important Changes
- **API URL**: Change from `sandbox.safaricom.co.ke` to `api.safaricom.co.ke`
- **Shortcode**: Use your production business shortcode
- **Passkey**: Use production passkey (different from sandbox)
- **Callback URL**: Must be HTTPS and publicly accessible
- **Domain**: Must be a real domain (not localhost/ngrok)

## Step 4: Production Requirements

### 4.1 HTTPS Certificate
- Your website MUST use HTTPS
- Valid SSL certificate required
- No self-signed certificates

### 4.2 Callback URL
- Must be publicly accessible
- Must use HTTPS
- Must be from a real domain
- Example: `https://fundiplatform.com/mpesa/callback/`

### 4.3 Security
- Never expose credentials in code
- Use environment variables
- Implement proper error handling
- Log all transactions
- Implement webhook signature validation

## Step 5: Testing Production

### 5.1 Test with Real M-Pesa Accounts
- Use real M-Pesa registered phone numbers
- Test with small amounts first
- Verify callbacks are received
- Test payment completion flow

### 5.2 Test Scenarios
1. Successful payment
2. Failed payment (insufficient funds)
3. Cancelled payment (user cancels)
4. Timeout scenarios
5. Duplicate payment prevention

## Step 6: Go Live Checklist

- [ ] Production credentials obtained
- [ ] .env file updated with production credentials
- [ ] API URL changed to production
- [ ] HTTPS certificate installed
- [ ] Callback URL is publicly accessible
- [ ] Webhook endpoint tested
- [ ] Error handling implemented
- [ ] Transaction logging in place
- [ ] Customer support process ready
- [ ] Terms of service updated
- [ ] Privacy policy updated

## Step 7: Monitoring & Support

### 7.1 Monitor Transactions
- Check payment status regularly
- Monitor callback logs
- Track failed transactions
- Review customer complaints

### 7.2 Support Contacts
- Safaricom Developer Support: developer@safaricom.co.ke
- M-Pesa Business Support: Call 234

## Important Notes

⚠️ **WARNING**: 
- Production payments involve REAL MONEY
- Test thoroughly before going live
- Start with small amounts
- Monitor closely in first days
- Have refund process ready

## Cost Considerations

- M-Pesa charges transaction fees
- Fees vary by transaction type
- Check current M-Pesa pricing
- Factor fees into your pricing

## Legal & Compliance

- Ensure compliance with Kenyan payment regulations
- Have proper terms of service
- Implement data protection (GDPR/Data Protection Act)
- Keep transaction records
- Tax compliance

