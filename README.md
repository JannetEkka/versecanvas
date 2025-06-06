# VerseCanvas 🎨

Transform your poetry into stunning visual art using cutting-edge AI technology.

![VerseCanvas](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Google Cloud](https://img.shields.io/badge/Platform-Google%20Cloud-yellow)

## ✨ Features

### 🧠 AI-Powered Poetry Analysis
- **Deep Understanding**: Uses Google Gemini to analyze themes, emotions, and visual elements
- **Multi-language Support**: Supports English, Spanish, French, German, Italian, and Portuguese
- **Contextual Interpretation**: Goes beyond literal text to capture poetic nuance and metaphor

### 🎨 Advanced Image Generation
- **High-Quality Output**: Powered by Google Imagen on Vertex AI
- **Multiple Art Styles**: Choose from Photorealistic, Watercolor, Oil Painting, Digital Art, Abstract, and Minimalist
- **Multiple Interpretations**: Generate 1-3 different visual interpretations per poem
- **Mood Intensity Control**: Adjust emotional expression intensity (0.1x to 2.0x)

### 🖼️ Comprehensive Image Editing
- **Real-time Adjustments**: Brightness, contrast, and blur controls
- **Advanced Filters**: Multiple artistic filters and effects
- **Text Overlay**: Add poem text directly to images with customizable styling
- **Font Options**: Multiple font styles, sizes, and positioning options
- **Background Control**: Adjustable text background opacity and colors

### 📱 Intuitive User Interface
- **Carousel Navigation**: Seamlessly browse between multiple generated interpretations
- **Responsive Design**: Clean, modern interface with custom CSS styling
- **Progress Tracking**: Real-time feedback during AI processing
- **Sample Poems**: Pre-loaded examples for quick testing
- **One-Click Downloads**: Download individual images or entire collections

### 🔧 Technical Excellence
- **Robust Error Handling**: Graceful fallbacks and user-friendly error messages
- **Environment Validation**: Built-in setup verification and testing tools
- **Modular Architecture**: Clean separation of concerns across multiple modules
- **Session Management**: Persistent state management across user interactions

## 🚀 Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI Models**: 
  - Google Gemini 2.0 Flash (Poetry Analysis)
  - Google Imagen 3.0 (Image Generation)
- **Platform**: Google Cloud Vertex AI
- **Image Processing**: PIL (Pillow) for editing and text overlay
- **Language**: Python 3.9+
- **Configuration**: Environment variables with `.env` support

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Google Cloud account with Vertex AI API enabled
- Google Cloud CLI installed and authenticated

### Quick Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/versecanvas.git
cd versecanvas
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Google Cloud project details
PROJECT_ID=your-google-cloud-project-id
LOCATION=us-central1
```

4. **Authenticate with Google Cloud**:
```bash
gcloud auth login
gcloud auth application-default login
```

5. **Verify setup**:
```bash
python setup.py
```

6. **Run the application**:
```bash
streamlit run app.py
```

## 📖 Usage Guide

### Basic Workflow

1. **Enter Your Poem**: Type or paste your poem in the text area, or select from sample poems
2. **Configure Settings**: Choose language, art style, and mood intensity from the sidebar
3. **Generate Art**: Click "Analyze & Generate" to create your visual interpretations
4. **Browse Results**: Use the carousel navigation to view different interpretations
5. **Edit & Customize**: Adjust brightness, contrast, blur, or add text overlays
6. **Download**: Save your favorite creations as high-resolution PNG files

### Advanced Features

#### Poetry Analysis
- View detailed analysis including themes, mood, visual elements, and narrative structure
- See the AI-generated prompt used for image creation
- Understand how your poem was interpreted visually

#### Image Editing
- **Basic Adjustments**: Fine-tune brightness (0.1-2.0x), contrast (0.1-2.0x), and blur (0-5 levels)
- **Text Overlay**: Add your poem text with customizable:
  - Font styles (serif, sans-serif, arial, times, helvetica)
  - Font sizes (16-48px)
  - Colors (white, black, gray variations)
  - Positions (center, top, bottom, left, right)
  - Background opacity (0-100%)
  - Text alignment (left, center, right)

#### Multi-Image Management
- Generate up to 3 interpretations per poem
- Navigate between interpretations with intuitive carousel controls
- Apply different edits to each interpretation
- Download individual images or browse the entire collection

## 🏗️ Project Structure

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
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## 🧪 Testing & Validation

The project includes a comprehensive testing suite:

```bash
# Run full environment validation
python setup.py

# Test individual components
python poem_analyzer.py    # Test poetry analysis
python image_generator.py  # Test image generation
python image_editor.py     # Test image editing
python text_overlay.py     # Test text overlay
```

## 🎯 Sample Use Cases

### Creative Writing
- Visualize your poetry for social media
- Create book covers or promotional materials
- Generate inspiration for further creative work

### Education
- Teaching poetry analysis and interpretation
- Demonstrating AI capabilities in creative domains
- Exploring the intersection of literature and visual art

### Personal Projects
- Create personalized gifts with meaningful poems
- Build visual poetry collections
- Experiment with different artistic interpretations

## 🚧 Troubleshooting

### Common Issues

**"PROJECT_ID environment variable not set"**
- Ensure your `.env` file is properly configured
- Run `python setup.py` to validate your environment

**"Failed to generate images"**
- Check your Google Cloud authentication: `gcloud auth list`
- Verify Vertex AI API is enabled in your project
- Ensure sufficient API quotas

**"No images generated"**
- Try simpler, more concrete poetry
- Adjust the art style or mood intensity
- Check the generated prompt in the analysis details

**Import errors**
- Run `pip install -r requirements.txt`
- Ensure Python 3.9+ is being used

### Getting Help

1. Run the setup validation: `python setup.py`
2. Check the error logs in the Streamlit interface
3. Verify your Google Cloud project configuration
4. Review the sample poems to understand expected input format

## 🤝 Contributing

This project was created as a demonstration of AI integration capabilities. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud**: For providing the Vertex AI platform and AI models
- **Streamlit**: For the excellent rapid prototyping framework
- **PIL/Pillow**: For comprehensive image processing capabilities
- **Poetry Community**: For inspiring this creative intersection of technology and art

## 🔮 Future Enhancements

- **Video Generation**: Animated poetry visualizations
- **Audio Integration**: AI-generated poetry narration
- **Community Features**: Share and discover poetry-art creations
- **Advanced Editing**: More sophisticated image manipulation tools
- **Style Transfer**: Apply artistic styles from reference images
- **Batch Processing**: Process multiple poems simultaneously

---

**Built with ❤️ and AI | Transform words into visual wonder**