# VerseCanvas 🎨

> Transform your poetry into stunning visual art using cutting-edge AI technology

![VerseCanvas](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Google Cloud](https://img.shields.io/badge/Platform-Google%20Cloud-yellow)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## 🌟 Overview

VerseCanvas is an innovative AI-powered application that bridges the gap between literary art and visual expression. Simply input a poem, and watch as advanced AI models analyze its themes, emotions, and imagery to generate stunning background artwork that captures the essence of your words. **With automatic text overlay**, your poetry-art pieces are ready to share in just two clicks!

**✨ Perfect for:** Writers, Artists, Educators, Content Creators, Poetry Enthusiasts

## 🎥 Demo

> **[📺 Watch Demo Video](YOUR_DEMO_VIDEO_LINK)** *(Coming Soon)*

**Try it with these sample poems:**
- Classic poetry (Shakespeare, Frost, Dickinson)
- Modern free verse
- Haikus and short forms
- Your own original poetry

## ✨ Key Features

### 🧠 **AI-Powered Poetry Analysis**
- **Deep Semantic Understanding**: Uses Google Gemini 2.0 to analyze themes, emotions, and visual elements
- **Multi-Language Support**: English, Spanish, French, German, Italian, and Portuguese
- **Contextual Interpretation**: Goes beyond literal text to capture poetic nuance and metaphor
- **Structured Analysis**: Extracts themes, mood, visual elements, and narrative structure

### 🎨 **Advanced Image Generation**
- **High-Quality Output**: Powered by Google Imagen 3.0 on Vertex AI
- **Multiple Art Styles**: 
  - Photorealistic
  - Watercolor
  - Oil Painting
  - Digital Art
  - Abstract
  - Minimalist
- **Multiple Interpretations**: Generate 1-3 different visual interpretations per poem
- **Mood Intensity Control**: Adjust emotional expression intensity (0.1x to 2.0x)

### 🖼️ **Comprehensive Image Editing**
- **Real-time Adjustments**: Brightness, contrast, and blur controls
- **Smart Text Overlay**: Poem text automatically enabled with full customization:
  - Multiple font styles (serif, sans-serif, arial, times, helvetica)
  - Customizable font sizes (16-48px)
  - Flexible positioning (center, top, bottom, left, right)
  - Adjustable text colors and background opacity
  - Text alignment options (left, center, right)
  - Toggle on/off as needed
- **Carousel Navigation**: Seamlessly browse between multiple generated interpretations
- **Version Control**: Reset to original or apply cumulative edits

### 📱 **Intuitive User Experience**
- **Clean Interface**: Modern, responsive design with custom CSS styling
- **Progress Tracking**: Real-time feedback during AI processing
- **Sample Poems**: Pre-loaded examples for quick testing
- **One-Click Downloads**: Download individual images as high-resolution PNG files
- **Session Persistence**: Maintains state across user interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Google Cloud account with Vertex AI API enabled
- Google Cloud CLI installed and authenticated

### Installation

1. **Clone and navigate to the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/versecanvas.git
cd versecanvas
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up Google Cloud authentication**:
```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login

# Set your project (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID
```

4. **Configure environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Google Cloud project details
# PROJECT_ID=your-google-cloud-project-id
# LOCATION=us-central1
```

5. **Verify your setup**:
```bash
python setup.py
```

6. **Launch the application**:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Basic Workflow

1. **📝 Input Your Poem**
   - Type or paste your poem in the text area
   - Or select from pre-loaded sample poems
   - Supports multiple languages

2. **⚙️ Configure Settings** (Sidebar)
   - Choose poem language
   - Select art style (Photorealistic, Watercolor, etc.)
   - Adjust mood intensity (0.1x to 2.0x)
   - Set number of images to generate (1-3)

3. **🔍 Analyze & Generate**
   - Click "Analyze & Generate" button
   - Watch AI analyze your poem's themes and emotions
   - View generated visual interpretations

4. **🖼️ Browse & Edit**
   - Use carousel navigation (◀ ▶) to view different interpretations
   - Text overlay is automatically applied with smart defaults
   - Customize text styling: fonts, size, position, colors
   - Apply real-time edits: brightness, contrast, blur
   - Toggle text overlay on/off as needed
   - Reset to original anytime

5. **📥 Download & Share**
   - Download individual images as PNG files
   - Perfect for social media, presentations, or printing

### Advanced Features

#### Poetry Analysis Details
Click "View Analysis Details" to see:
- **Themes**: Core concepts and subjects identified
- **Mood**: Emotional tone and atmosphere
- **Visual Elements**: Colors, objects, settings extracted
- **Generated Prompt**: The detailed prompt used for image creation

#### Text Overlay Customization
Text overlay is enabled by default with smart positioning and styling:
- **Font Styles**: Choose from serif, sans-serif, arial, times, helvetica
- **Positioning**: Center, top, bottom, left, or right placement
- **Styling**: Adjust font size, color, and background opacity
- **Alignment**: Left, center, or right text alignment
- **Toggle Control**: Enable/disable as needed for your design

## 🏗️ Project Architecture

```
versecanvas/
├── app.py                 # Main Streamlit application
├── poem_analyzer.py       # Gemini-powered poetry analysis
├── image_generator.py     # Imagen-based image generation
├── image_editor.py        # PIL-based image editing tools
├── text_overlay.py        # Advanced text overlay functionality
├── setup.py              # Environment validation and testing
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── secrets.toml          # Streamlit secrets (for deployment)
├── README.md             # This file
└── LICENSE               # MIT License
```

## 🧪 Testing & Validation

Run the comprehensive test suite to verify your setup:

```bash
# Run full environment validation
python setup.py

# Test individual components
python poem_analyzer.py    # Test poetry analysis
python image_generator.py  # Test image generation
python image_editor.py     # Test image editing
python text_overlay.py     # Test text overlay
```

## 🚧 Troubleshooting

### Common Issues & Solutions

**❌ "PROJECT_ID environment variable not set"**
- Ensure your `.env` file is properly configured
- Run `python setup.py` to validate your environment

**❌ Authentication errors**
- Check: `gcloud auth list` (should show active account)
- Re-authenticate: `gcloud auth application-default login`
- Verify Vertex AI API is enabled in your Google Cloud project

**❌ "Failed to generate images"**
- Check your Google Cloud project quotas
- Ensure you have sufficient credits/billing enabled
- Try simpler poems first

**❌ Import errors**
- Run: `pip install -r requirements.txt`
- Ensure Python 3.9+ is being used: `python --version`

**❌ No images generated**
- Try more concrete, descriptive poetry
- Adjust art style or mood intensity
- Check the generated prompt in analysis details

### Getting Help

1. **First**: Run `python setup.py` to diagnose issues
2. **Check**: Streamlit interface error messages
3. **Verify**: Google Cloud project configuration
4. **Test**: Sample poems to understand expected format

## 🎯 Use Cases

### 🎨 **Creative & Artistic**
- **Social Media Content**: Create engaging poetry posts with matching visuals - text included automatically
- **Book Covers**: Generate artwork for poetry collections or chapbooks with integrated text
- **Art Projects**: Explore the intersection of literature and visual art
- **Personal Expression**: Visualize your emotions and thoughts through poetry with instant text overlay

### 📚 **Educational**
- **Literature Classes**: Demonstrate poetry analysis and interpretation
- **Creative Writing**: Inspire students with visual representations of their work
- **Language Learning**: Combine language practice with visual context
- **AI Education**: Show practical applications of language and vision models

### 💼 **Professional**
- **Content Creation**: Generate unique visuals for blogs, websites, presentations
- **Marketing**: Create atmospheric backgrounds for campaigns
- **Therapy & Wellness**: Use poetry and visuals for mindfulness and expression
- **Gifts**: Create personalized artwork from meaningful poems

## 🔧 Technical Details

### AI Models & APIs
- **Poetry Analysis**: Google Gemini 2.0 Flash (Vertex AI)
- **Image Generation**: Google Imagen 3.0 (Vertex AI)
- **Image Processing**: PIL (Pillow) for editing and text overlay
- **Platform**: Google Cloud Platform with Vertex AI

### Performance & Scalability
- **Serverless**: Built for Cloud Run deployment
- **Auto-scaling**: Handles variable user demand
- **Session Management**: Persistent state across interactions
- **Error Handling**: Graceful fallbacks and user-friendly messages

### Security & Privacy
- **Secure Authentication**: Google Cloud service account integration
- **Environment Variables**: Sensitive data protected via `.env` files
- **No Data Storage**: Poems and images processed in memory only
- **Streamlit Secrets**: Production deployment credential management

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment (Streamlit Community Cloud)
1. Push your code to GitHub
2. Connect to Streamlit Community Cloud
3. Add your secrets via the Streamlit dashboard
4. Deploy with one click

### Google Cloud Run (Production)
```bash
# Build and deploy container
gcloud run deploy versecanvas \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit**: `git commit -m 'Add amazing feature'`
5. **Push**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Test with multiple poem types and languages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud**: For providing Vertex AI platform and advanced AI models
- **Streamlit**: For the excellent rapid prototyping framework
- **PIL/Pillow**: For comprehensive image processing capabilities
- **Open Source Community**: For the tools and libraries that make this possible
- **Poetry Community**: For inspiring this creative intersection of technology and art

## 🔮 Roadmap & Future Enhancements

### Phase 2 Features
- [ ] **Video Generation**: Animated poetry visualizations
- [ ] **Audio Integration**: AI-generated poetry narration with Gemini's audio capabilities
- [ ] **Advanced Styles**: Integration with artistic style transfer models
- [ ] **Batch Processing**: Process multiple poems simultaneously

### Phase 3 Features
- [ ] **Community Platform**: Share and discover poetry-art creations
- [ ] **Collaborative Editing**: Real-time collaborative poem editing
- [ ] **API Access**: RESTful API for developers
- [ ] **Mobile App**: Native iOS and Android applications

### Phase 4 Features
- [ ] **Custom Models**: Fine-tuned models for specific poetry styles
- [ ] **3D Visualizations**: Three-dimensional poetry representations
- [ ] **VR/AR Integration**: Immersive poetry experiences
- [ ] **Educational Platform**: Structured courses on AI and creativity

## 📊 Project Stats

- **Languages Supported**: 6 (English, Spanish, French, German, Italian, Portuguese)
- **Art Styles Available**: 6 (Photorealistic, Watercolor, Oil Painting, Digital Art, Abstract, Minimalist)
- **Default Features**: Automatic text overlay with smart positioning
- **Image Formats**: PNG output, RGB color space
- **Max Resolution**: Limited by Imagen model capabilities
- **Response Time**: ~10-30 seconds per generation (varies by complexity)
- **Workflow**: Complete poetry-art pieces in just 2 clicks!

---

**🎨 Built with ❤️ and AI | Transform words into visual wonder in just 2 clicks**

*Made with Google Cloud Vertex AI • Powered by Gemini and Imagen • Created with Streamlit • Text overlay included automatically*

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/JannetEkka/versecanvas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JannetEkka/versecanvas/discussions)
- **Email**: jannetaekka@gmail.com

**Star ⭐ this repo if you find it helpful!**