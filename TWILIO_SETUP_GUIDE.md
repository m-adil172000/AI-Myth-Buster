# 🚀 Complete Twilio WhatsApp Integration Guide

## Step-by-Step Setup for AI Myth-Buster WhatsApp Bot

### Prerequisites

- ✅ Your FastAPI bot is running (which it is!)
- ✅ You have a phone number for testing
- ✅ Internet connection

---

## 📱 **STEP 1: Create Twilio Account**

1. **Go to Twilio**: Visit [https://www.twilio.com](https://www.twilio.com)
2. **Sign Up**: Click "Sign up" and create a free account
3. **Verify Phone**: Verify your phone number
4. **Complete Setup**: Answer the questionnaire (select "Products & APIs" → "Messaging")

---

## 🔑 **STEP 2: Get Your Twilio Credentials**

1. **Go to Console**: After login, go to [Twilio Console](https://console.twilio.com)
2. **Find Credentials**: On the main dashboard, you'll see:

   - **Account SID**: Starts with `AC...` (copy this)
   - **Auth Token**: Click "Show" to reveal it (copy this)

3. **Save Credentials**: You'll need these for your `.env` file

---

## 📞 **STEP 3: Set Up WhatsApp Sandbox**

1. **Navigate to WhatsApp**:

   - Go to Console → Messaging → Try it out → Send a WhatsApp message
   - Or direct link: [https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)

2. **Get Sandbox Number**: You'll see a number like `+1 415 523 8886`

3. **Join Sandbox**:
   - Send the join code (like `join <code>`) to the Twilio WhatsApp number
   - You'll get a confirmation message

---

## 🌐 **STEP 4: Set Up ngrok (Expose Your Local Server)**

1. **Install ngrok**:

   ```bash
   # On macOS with Homebrew
   brew install ngrok

   # Or download from https://ngrok.com/download
   ```

2. **Start ngrok** (in a new terminal):

   ```bash
   ngrok http 8000
   ```

3. **Copy the URL**: You'll see something like:
   ```
   Forwarding    https://abc123.ngrok.io -> http://localhost:8000
   ```
   **Copy the `https://abc123.ngrok.io` URL**

---

## ⚙️ **STEP 5: Configure Twilio Webhook**

1. **Go to WhatsApp Sandbox Settings**:

   - Console → Messaging → Settings → WhatsApp sandbox settings
   - Or: [https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox](https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox)

2. **Set Webhook URL**:
   - **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook/whatsapp`
   - **HTTP Method**: POST
   - Click **Save Configuration**

---

## 🔧 **STEP 6: Update Your Environment Variables**

1. **Edit your `.env` file**:

   ```bash
   nano .env
   ```

2. **Replace with your real credentials**:

   ```env
   # Replace these with your actual Twilio credentials
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_actual_auth_token_here
   TWILIO_PHONE_NUMBER=whatsapp:+14155238886

   # Your ngrok URL
   WEBHOOK_URL=https://your-ngrok-url.ngrok.io

   # Application settings
   DEBUG=true
   LOG_LEVEL=INFO
   ```

3. **Save the file** (Ctrl+X, then Y, then Enter)

---

## 🧪 **STEP 7: Test Your Bot**

1. **Restart your FastAPI server** (if needed):

   ```bash
   # Your server should already be running, but if not:
   uvicorn app.main:app --reload
   ```

2. **Send a test message**:

   - Open WhatsApp on your phone
   - Send any message to the Twilio WhatsApp number
   - Example: "Hello, can you fact-check this claim?"

3. **Expected Response**:

   ```
   Received your message: Hello, can you fact-check this claim?

   Fact-checking feature coming soon! 🔍
   ```

---

## 🔍 **STEP 8: Monitor and Debug**

1. **Check your terminal**: You should see logs like:

   ```
   INFO:app.routes.webhook:Received webhook from whatsapp:+1234567890: Hello, can you fact-check this claim?
   INFO:app.services.message_service:Processing message from +1234567890: Hello, can you fact-check this claim?
   INFO:app.services.message_service:Generated response for +1234567890
   ```

2. **Check Twilio Console**:

   - Go to Console → Monitor → Logs → Messaging
   - You should see successful message logs

3. **Test webhook directly**:
   ```bash
   curl -X GET https://your-ngrok-url.ngrok.io/webhook/status
   ```

---

## 🚨 **Troubleshooting Common Issues**

### Issue 1: "Authentication Error"

- **Problem**: Wrong Twilio credentials
- **Solution**: Double-check Account SID and Auth Token in `.env`

### Issue 2: "Webhook not receiving messages"

- **Problem**: Wrong webhook URL or ngrok not running
- **Solution**:
  1. Ensure ngrok is running: `ngrok http 8000`
  2. Update webhook URL in Twilio console
  3. Make sure URL ends with `/webhook/whatsapp`

### Issue 3: "Connection refused"

- **Problem**: FastAPI server not running
- **Solution**: Start server: `uvicorn app.main:app --reload`

### Issue 4: "ngrok tunnel not found"

- **Problem**: ngrok session expired
- **Solution**: Restart ngrok and update webhook URL in Twilio

---

## 📋 **Quick Checklist**

- [ ] Twilio account created
- [ ] Account SID and Auth Token copied
- [ ] WhatsApp sandbox joined
- [ ] ngrok installed and running
- [ ] Webhook URL configured in Twilio
- [ ] `.env` file updated with real credentials
- [ ] FastAPI server running
- [ ] Test message sent and received

---

## 🎯 **What Happens Next**

Once everything is working:

1. **Your bot receives WhatsApp messages**
2. **Processes them through the webhook**
3. **Sends back placeholder responses**
4. **Ready for LLM integration** (OpenAI/Groq for actual fact-checking)

---

## 💡 **Pro Tips**

1. **Keep ngrok running**: If ngrok stops, you need to update the webhook URL
2. **Use ngrok auth**: Sign up for ngrok to get persistent URLs
3. **Monitor logs**: Watch your terminal for debugging
4. **Test thoroughly**: Send different types of messages to test

---

## 🔗 **Useful Links**

- [Twilio Console](https://console.twilio.com)
- [Twilio WhatsApp Docs](https://www.twilio.com/docs/whatsapp)
- [ngrok Download](https://ngrok.com/download)
- [Your Bot API Docs](http://localhost:8000/docs)

---

**🎉 You're all set! Your WhatsApp AI Myth-Buster bot is ready to receive and respond to messages!**
