# AI Myth-Buster WhatsApp Bot

A WhatsApp AI fact-checker bot built with FastAPI and Twilio that receives messages and replies with LLM-generated fact-checks.

## 🚀 Features

- **FastAPI Backend**: Modern, fast web framework for building APIs
- **Twilio WhatsApp Integration**: Seamless WhatsApp messaging via Twilio API
- **Modular Architecture**: Clean separation of routes, services, and models
- **Docker Support**: Easy deployment with containerization
- **Webhook Handling**: Secure webhook endpoint for receiving WhatsApp messages
- **Placeholder Responses**: Currently replies with placeholder text (LLM integration coming soon)
- **Safety Filtering**: Basic filtering to avoid processing personal chats

## 📋 Prerequisites

- Python 3.11+
- Twilio Account with WhatsApp API access
- ngrok (for local testing)
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/m-adil172000/AI-Myth-Buster.git
cd AI-Myth-Buster
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

Required environment variables:

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp number (e.g., `whatsapp:+14155238886`)

### 4. Set Up Twilio WhatsApp

1. **Create a Twilio Account**: Sign up at [twilio.com](https://www.twilio.com)
2. **Get WhatsApp Sandbox**: Go to Console → Messaging → Try it out → Send a WhatsApp message
3. **Get Credentials**: Find your Account SID and Auth Token in the Twilio Console
4. **Note Your WhatsApp Number**: Use the provided Twilio WhatsApp sandbox number

## 🚀 Running the Application

### Local Development

```bash
# Run with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m app.main
```

The API will be available at:

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Webhook Status**: http://localhost:8000/webhook/status

### Using Docker

```bash
# Build the Docker image
docker build -t ai-myth-buster .

# Run the container
docker run -p 8000:8000 --env-file .env ai-myth-buster
```

## 🌐 Setting Up ngrok for Local Testing

To test webhooks locally, you need to expose your local server to the internet:

```bash
# Install ngrok (if not already installed)
# On macOS with Homebrew:
brew install ngrok

# On other systems, download from https://ngrok.com/download

# Start your FastAPI app
uvicorn app.main:app --reload --port 8000

# In another terminal, expose the local server
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and use it to configure your Twilio webhook.

## ⚙️ Configuring Twilio Webhook

1. **Go to Twilio Console** → Messaging → Settings → WhatsApp sandbox settings
2. **Set Webhook URL**: `https://your-ngrok-url.ngrok.io/webhook/whatsapp`
3. **Set HTTP Method**: POST
4. **Save Configuration**

## 🧪 Testing the Bot

1. **Join WhatsApp Sandbox**: Send the join code to your Twilio WhatsApp number
2. **Send a Test Message**: Send any message to the bot
3. **Check Response**: You should receive a placeholder response like:

   ```
   Received your message: [your message]

   Fact-checking feature coming soon! 🔍
   ```

## 📁 Project Structure

```
AI-Myth-Buster/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── models.py            # Pydantic models for data validation
│   ├── routes/
│   │   ├── __init__.py
│   │   └── webhook.py       # Webhook routes for WhatsApp
│   └── services/
│       ├── __init__.py
│       ├── twilio_service.py    # Twilio WhatsApp integration
│       └── message_service.py   # Message processing logic
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 API Endpoints

- `GET /` - Health check and welcome message
- `GET /health` - Health check for monitoring
- `POST /webhook/whatsapp` - Main webhook for receiving WhatsApp messages
- `GET /webhook/whatsapp` - Webhook verification endpoint
- `GET /webhook/status` - Webhook service status

## 🔮 Future Enhancements

- **LLM Integration**: Add OpenAI or Groq API for actual fact-checking
- **Advanced Safety Filtering**: ML-based detection of personal vs. fact-checkable content
- **Media Processing**: Handle images and documents
- **Database Integration**: Store conversation history and fact-check results
- **Rate Limiting**: Prevent abuse and manage API costs
- **Analytics Dashboard**: Monitor bot usage and performance

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to initialize Twilio client"**

   - Check your Twilio credentials in `.env`
   - Ensure Account SID and Auth Token are correct

2. **"Webhook not receiving messages"**

   - Verify ngrok is running and URL is correct
   - Check Twilio webhook configuration
   - Ensure your local server is running on the correct port

3. **"Module not found" errors**
   - Activate your virtual environment
   - Install dependencies: `pip install -r requirements.txt`

### Logs and Debugging

- Check application logs for detailed error messages
- Set `DEBUG=true` in `.env` for verbose logging
- Use `LOG_LEVEL=DEBUG` for maximum detail

## 📝 Environment Variables Reference

| Variable              | Description                            | Example                           |
| --------------------- | -------------------------------------- | --------------------------------- |
| `TWILIO_ACCOUNT_SID`  | Your Twilio Account SID                | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN`   | Your Twilio Auth Token                 | `your_auth_token_here`            |
| `TWILIO_PHONE_NUMBER` | Your Twilio WhatsApp number            | `whatsapp:+14155238886`           |
| `WEBHOOK_URL`         | Your webhook URL (ngrok or production) | `https://abc123.ngrok.io`         |
| `OPENAI_API_KEY`      | OpenAI API key (future use)            | `sk-...`                          |
| `GROQ_API_KEY`        | Groq API key (future use)              | `gsk_...`                         |
| `DEBUG`               | Enable debug mode                      | `false`                           |
| `LOG_LEVEL`           | Logging level                          | `INFO`                            |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [Twilio WhatsApp documentation](https://www.twilio.com/docs/whatsapp)
3. Open an issue on GitHub

---

**Note**: This is the first milestone of the AI Myth-Buster project. The fact-checking functionality using LLMs will be added in subsequent updates.
