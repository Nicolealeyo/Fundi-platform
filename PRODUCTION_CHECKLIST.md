# M-Pesa Production Checklist

## Before Going Live

### 1. Credentials & Configuration
- [ ] Production Consumer Key obtained
- [ ] Production Consumer Secret obtained
- [ ] Production Shortcode (business Paybill/Till number) obtained
- [ ] Production Passkey obtained
- [ ] .env file updated with production credentials
- [ ] MPESA_ENVIRONMENT set to 'production' in .env
- [ ] MPESA_API_URL set to 'https://api.safaricom.co.ke'
- [ ] MPESA_CALLBACK_URL uses HTTPS and real domain

### 2. Infrastructure
- [ ] Website deployed to production server
- [ ] HTTPS certificate installed and valid
- [ ] Domain name configured
- [ ] Callback URL is publicly accessible
- [ ] Server can handle production traffic
- [ ] Database backups configured

### 3. Security
- [ ] All credentials in .env (not in code)
- [ ] .env file not committed to git
- [ ] Webhook signature validation implemented
- [ ] Error handling for all payment scenarios
- [ ] Transaction logging in place
- [ ] Rate limiting implemented

### 4. Testing
- [ ] Tested with real M-Pesa accounts
- [ ] Tested successful payment flow
- [ ] Tested failed payment scenarios
- [ ] Tested callback/webhook reception
- [ ] Tested payment status updates
- [ ] Tested refund process (if applicable)

### 5. Legal & Compliance
- [ ] Terms of Service updated
- [ ] Privacy Policy updated
- [ ] Payment terms clearly stated
- [ ] Refund policy documented
- [ ] Data protection measures in place
- [ ] Tax compliance verified

### 6. Support & Monitoring
- [ ] Customer support process ready
- [ ] Payment issue escalation process
- [ ] Transaction monitoring dashboard
- [ ] Error alerting configured
- [ ] Support contact information available

### 7. Documentation
- [ ] Production setup documented
- [ ] Troubleshooting guide created
- [ ] Support team trained
- [ ] Rollback plan prepared

## Production .env Example

```env
# Production M-Pesa Settings
MPESA_ENVIRONMENT=production
MPESA_CONSUMER_KEY=your_production_consumer_key
MPESA_CONSUMER_SECRET=your_production_consumer_secret
MPESA_SHORTCODE=your_business_shortcode
MPESA_PASSKEY=your_production_passkey
MPESA_API_URL=https://api.safaricom.co.ke
MPESA_CALLBACK_URL=https://yourdomain.com/mpesa/callback/

# Django Settings
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your_production_secret_key
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Important Reminders

⚠️ **Real Money**: Production involves real money transactions
⚠️ **Test First**: Always test with small amounts first
⚠️ **Monitor**: Watch transactions closely in first days
⚠️ **Support**: Have customer support ready
⚠️ **Backup**: Keep backups of all transaction data

