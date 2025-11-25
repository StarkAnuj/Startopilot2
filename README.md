# Gemini AI Assistant

A professional full-stack voice and vision-enabled AI assistant powered by Google Gemini Pro Vision API. The application combines real-time camera feed, voice recording, speech-to-text, and text-to-speech capabilities for natural AI interactions.

## 🚀 Features

- **Voice Interaction**: Record voice messages with real-time speech-to-text using VOSK
- **Vision Analysis**: Capture camera snapshots for visual analysis by Gemini Pro Vision
- **Natural Conversations**: Combined voice and vision input for contextual AI responses
- **Audio Responses**: Text-to-speech playback of AI responses using gTTS
- **Real-time Interface**: Live camera feed with responsive web interface
- **Professional UI**: Modern, responsive design with dark mode support
- **Production Ready**: Optimized for Vercel deployment

## 🛠️ Technology Stack

**Backend (Python):**
- FastAPI - Modern, fast web framework
- Google Gemini Pro Vision API - AI vision and text analysis
- VOSK - Offline speech recognition
- gTTS - Text-to-speech synthesis
- Pydub - Audio processing
- Pillow - Image processing

**Frontend (TypeScript/React):**
- Next.js 15 - React framework with App Router
- Tailwind CSS - Utility-first styling
- Lucide React - Modern icon library
- MediaDevices API - Camera and microphone access

## 📦 Installation

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd gemini-ai-assistant

# Create virtual environment
python -m venv .venv_gemini_demo

# Activate virtual environment
# Windows:
.venv_gemini_demo\Scripts\activate
# Linux/Mac:
source .venv_gemini_demo/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "https://your-vercel-domain.vercel.app"]
```

**Get your Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Add it to your `.env` file

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Run Setup Script

```bash
python setup.py
```

This script will:
- Verify your API key configuration
- Test Gemini API connectivity
- Download the VOSK speech recognition model
- Create necessary directories

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
# Activate virtual environment first
.venv_gemini_demo\Scripts\activate

# Start FastAPI server
python -m uvicorn api.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Build

```bash
cd frontend
npm run build
npm start
```

## 📁 Project Structure

```
gemini-ai-assistant/
├── api/                          # Python FastAPI backend
│   ├── services/                 # Core services
│   │   ├── gemini_service.py     # Gemini API integration
│   │   ├── speech_service.py     # VOSK STT & gTTS
│   │   └── vision_service.py     # Image processing
│   ├── utils/                    # Utility modules
│   │   ├── audio_utils.py        # Audio processing
│   │   └── image_utils.py        # Image utilities
│   └── main.py                   # FastAPI application
├── frontend/                     # Next.js frontend
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   │   └── AIAssistant.tsx       # Main AI interface
│   └── public/                   # Static assets
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── setup.py                     # Setup and configuration script
├── vercel.json                  # Vercel deployment config
└── README.md                    # This file
```

## 🔧 API Endpoints

### Main Interaction
- `POST /api/interact` - Process voice/text + image for AI response
  - `audio`: Audio file (optional)
  - `image`: Image file (required)
  - `text_prompt`: Text input (optional)

### Utility Endpoints
- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /api/transcribe` - Audio-to-text only
- `POST /api/tts` - Text-to-speech only

## 🌐 Deployment on Vercel

### 1. Prepare for Deployment

The project is pre-configured for Vercel deployment with:
- `vercel.json` configuration
- Serverless function setup
- Environment variable configuration

### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### 3. Configure Environment Variables

In your Vercel dashboard, add:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `ENVIRONMENT`: `production`

### 4. Domain Configuration

Update your `.env` and `next.config.ts` with your Vercel domain.

## 🎮 Usage Guide

### Basic Interaction
1. **Enable Permissions**: Allow camera and microphone access when prompted
2. **Voice Input**: Click the microphone button to start recording
3. **Text Input**: Type messages in the text input field
4. **Visual Context**: The camera captures context for your questions
5. **AI Response**: Receive both text and audio responses

### Example Interactions
- "What do you see in front of me?"
- "Describe the objects on my desk"
- "What color is my shirt?"
- "Read any text visible in the image"
- "What's the weather like based on what you can see?"

### Tips for Best Results
- Ensure good lighting for camera
- Speak clearly into microphone
- Position objects clearly in camera view
- Use specific questions for better responses

## 🔍 Troubleshooting

### Common Issues

**VOSK Model Missing:**
```bash
# Download manually if setup.py fails
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
mv vosk-model-en-us-0.22 vosk-model
```

**Media Access Denied:**
- Check browser permissions
- Ensure HTTPS in production
- Try different browser

**API Connection Issues:**
- Verify Gemini API key
- Check network connectivity
- Review CORS settings

**Audio Processing Errors:**
- Check microphone permissions
- Verify audio format support
- Try different browser

### Development Debugging

```bash
# Backend logs
python -m uvicorn api.main:app --reload --log-level debug

# Frontend with detailed errors
cd frontend
npm run dev -- --debug

# Test individual services
python -c "from api.services.gemini_service import GeminiService; import asyncio; print(asyncio.run(GeminiService().test_connection()))"
```

## 📋 Requirements

### System Requirements
- Python 3.9+
- Node.js 18+
- Modern web browser with MediaDevices API support
- Camera and microphone access

### Browser Compatibility
- Chrome 80+
- Firefox 76+
- Safari 13+
- Edge 80+

## 🔒 Security Considerations

- API keys stored in environment variables
- CORS properly configured
- File upload validation
- Temporary file cleanup
- No sensitive data logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini Pro Vision API
- VOSK Speech Recognition
- Next.js and React teams
- FastAPI framework
- Open source community

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the troubleshooting section
- Review API documentation at `/docs`

---

**Built with ❤️ using Google Gemini Pro Vision**