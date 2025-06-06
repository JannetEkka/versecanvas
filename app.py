import streamlit as st

# Page configuration MUST be the very first Streamlit command
st.set_page_config(
    page_title="VerseCanvas - Poetry to Visual Art",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import everything else
import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv
from PIL import Image
import io
import base64
import json
from google.oauth2 import service_account

# Import our custom modules
from poem_analyzer import analyze_poem
from image_generator import generate_poem_image
from image_editor import basic_edit_image
from text_overlay import add_poem_to_image

# Load environment variables
load_dotenv()

# Initialize session state
if 'images' not in st.session_state:
    st.session_state.images = []
if 'edited_images' not in st.session_state:
    st.session_state.edited_images = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'current_poem' not in st.session_state:
    st.session_state.current_poem = ""
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False
if 'text_overlay_enabled' not in st.session_state:
    st.session_state.text_overlay_enabled = {}
if 'text_overlay_default' not in st.session_state:
    st.session_state.text_overlay_default = False
if 'current_image_index' not in st.session_state:
    st.session_state.current_image_index = 0

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);        
    }
    .poem-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .artwork-section {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 2px solid #e9ecef;
    }
    .generated-image {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .carousel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0 1rem;
    }
    .carousel-navigation {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .nav-button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .nav-button:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .nav-button:disabled {
        background: #ccc;
        cursor: not-allowed;
        transform: none;
    }
    .image-container {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .image-container:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .controls-header {
        color: #667eea;
        font-weight: bold;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    .stMainBlockContainer {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    .stVerticalBlock {
        gap: 0.5rem !important;
    }
    
    .stElementContainer {
        margin-bottom: 0.5rem !important;
    }
    
    /* Alternative: target the specific emotion-cache class if the above doesn't work */
    .st-emotion-cache-zy6yx3 {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    .st-emotion-cache-vlxhtx {
        gap: 0.5rem !important;
    }
    
    /* Reduce overall app padding */
    section[data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

def debug_credentials():
    """Debug function to test credentials loading - only show in debug mode"""
    # Only show debug info if explicitly requested via URL parameter
    try:
        if st.query_params.get('debug', [False])[0]:
            st.write("🔍 **Debug: Credentials Loading**")
            
            try:
                # Check if secrets are available
                if hasattr(st, 'secrets'):
                    st.write("✅ Streamlit secrets available")
                    
                    # Check PROJECT_ID
                    if 'PROJECT_ID' in st.secrets:
                        st.write(f"✅ PROJECT_ID: {st.secrets['PROJECT_ID']}")
                    else:
                        st.error("❌ PROJECT_ID not found in secrets")
                        return
                    
                    # Check GOOGLE_CREDENTIALS
                    if 'GOOGLE_CREDENTIALS' in st.secrets:
                        st.write("✅ GOOGLE_CREDENTIALS found in secrets")
                        
                        # Try to parse JSON
                        try:
                            credentials_json = st.secrets['GOOGLE_CREDENTIALS']
                            st.write(f"📏 Credentials string length: {len(credentials_json)}")
                            
                            # Parse JSON
                            credentials_info = json.loads(credentials_json)
                            st.write("✅ JSON parsing successful")
                            
                            # Check required fields
                            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
                            for field in required_fields:
                                if field in credentials_info:
                                    if field == 'private_key':
                                        st.write(f"✅ {field}: {len(credentials_info[field])} characters")
                                        # Check private key format
                                        pk = credentials_info[field]
                                        if pk.startswith('-----BEGIN PRIVATE KEY-----'):
                                            st.write("✅ Private key has correct header")
                                        else:
                                            st.error("❌ Private key missing header")
                                        
                                        if pk.endswith('-----END PRIVATE KEY-----'):
                                            st.write("✅ Private key has correct footer")
                                        else:
                                            st.error("❌ Private key missing footer")
                                        
                                        # Check for proper newlines
                                        if '\\n' in pk:
                                            st.write("✅ Private key contains newline escapes")
                                        else:
                                            st.error("❌ Private key missing newline escapes")
                                            
                                    else:
                                        st.write(f"✅ {field}: {credentials_info[field][:50]}...")
                                else:
                                    st.error(f"❌ Missing field: {field}")
                            
                            # Try to create credentials object
                            try:
                                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                                st.write("✅ Service account credentials created successfully")
                                
                                # Test if credentials are valid
                                try:
                                    # Try to refresh (this will validate the credentials)
                                    import google.auth.transport.requests
                                    request = google.auth.transport.requests.Request()
                                    credentials.refresh(request)
                                    st.write("✅ Credentials are valid and refreshed successfully")
                                except Exception as e:
                                    st.error(f"❌ Credentials validation failed: {str(e)}")
                                
                            except Exception as e:
                                st.error(f"❌ Failed to create credentials: {str(e)}")
                                
                        except json.JSONDecodeError as e:
                            st.error(f"❌ JSON parsing failed: {str(e)}")
                            st.write("Raw credentials preview:")
                            st.code(credentials_json[:500] + "..." if len(credentials_json) > 500 else credentials_json)
                            
                    else:
                        st.error("❌ GOOGLE_CREDENTIALS not found in secrets")
                else:
                    st.error("❌ Streamlit secrets not available")
                    
            except Exception as e:
                st.error(f"❌ Debug failed: {str(e)}")
    except:
        # If query_params is not available, skip debug
        pass

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 VerseCanvas</h1>
        <p>Transform your poetry into stunning visual art using AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language selection
        language = st.selectbox(
            "Poem Language",
            ["English", "Spanish", "French", "German", "Italian", "Portuguese"],
            index=0
        )
        
        # Style preferences
        st.subheader("🎨 Style Preferences")
        art_style = st.selectbox(
            "Art Style",
            ["Photorealistic", "Watercolor", "Oil Painting", "Digital Art", "Abstract", "Minimalist"],
            index=0
        )
        
        mood_intensity = st.slider("Mood Intensity", 0.1, 2.0, 1.0, 0.1)
        
        # Number of images to generate
        num_images = st.slider("Number of Images", 1, 3, 2)

    # Main content area - Vertical layout
    st.header("📝 Enter Your Poem")
    
    # Sample poems for demo
    sample_poems = {
        "Original Poem": "",
        "The Road Not Taken (Frost)": """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;""",
        "Haiku - Cherry Blossom": """Petals fall gently,
Pink clouds drift on spring breezes—
Nature's soft whisper.""",
        "Ocean Waves": """Endless waves crash upon the shore,
Whispering secrets of the deep,
As moonlight dances on the foam,
And ancient tides eternal sweep."""
    }
    
    selected_sample = st.selectbox("Choose a sample poem or write your own:", list(sample_poems.keys()))
    
    poem_text = st.text_area(
        "Poem Text",
        value=sample_poems[selected_sample],
        height=200,
        placeholder="Enter your poem here...",
        help="Write or paste your poem. The AI will analyze its themes, emotions, and visual elements."
    )
    
    # Analysis button
    if st.button("🔍 Analyze & Generate", type="primary", use_container_width=True):
        if poem_text.strip():
            # Clear previous results if poem changed
            if st.session_state.current_poem != poem_text:
                st.session_state.images = []
                st.session_state.edited_images = []
                st.session_state.analysis_result = None
                st.session_state.generation_complete = False
            
            st.session_state.current_poem = poem_text
            # Add some visual separation before results
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_and_generate(poem_text, language, art_style, mood_intensity, num_images)
        else:
            st.error("Please enter a poem first!")
    
    # Display generated artwork if available
    if st.session_state.generation_complete and st.session_state.images:
        display_generated_artwork()
    elif not st.session_state.generation_complete:
        # Show placeholder when no poem is being processed
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; color: #6c757d;'>
            <h3>🎨 Your Generated Artwork Will Appear Here</h3>
            <p>Enter a poem above and click "Analyze & Generate" to create beautiful AI-powered visual art!</p>
        </div>
        """, unsafe_allow_html=True)

def analyze_and_generate(poem_text, language, art_style, mood_intensity, num_images):
    """Main processing pipeline"""
    
    # Add visual separation
    st.markdown('<div class="artwork-section">', unsafe_allow_html=True)
    st.header("🎨 Generated Artwork")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Analyze poem
        status_text.text("🧠 Analyzing poem with AI...")
        progress_bar.progress(20)
        
        analysis_result = analyze_poem(poem_text, language, art_style, mood_intensity)
        
        if analysis_result:
            st.session_state.analysis_result = analysis_result
            st.success("✅ Poem analysis complete!")
            
            # Display analysis
            with st.expander("📋 View Analysis Details"):
                st.markdown("**Themes:** " + analysis_result.get('themes', 'N/A'))
                st.markdown("**Mood:** " + analysis_result.get('mood', 'N/A'))
                st.markdown("**Visual Elements:** " + analysis_result.get('visual_elements', 'N/A'))
                st.markdown("**Generated Prompt:** " + analysis_result.get('image_prompt', 'N/A'))
            
            # Step 2: Generate images
            status_text.text("🎨 Generating images...")
            progress_bar.progress(60)
            
            images = generate_poem_image(analysis_result['image_prompt'], num_images)
            
            if images:
                st.session_state.images = images
                st.session_state.edited_images = images.copy()  # Initialize edited images as copies
                st.session_state.generation_complete = True
                reset_carousel()  # Reset to first image
                
                progress_bar.progress(100)
                status_text.text("✨ Complete! Your artwork is ready.")
                
                # Display will be handled by display_generated_artwork()
                st.rerun()  # Refresh to show the artwork section
                
            else:
                st.error("Failed to generate images. Please try again.")
                
        else:
            st.error("Failed to analyze poem. Please check your input and try again.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your Google Cloud configuration and try again.")

def navigate_carousel(direction):
    """Navigate the image carousel"""
    if not st.session_state.images:
        return
    
    current = st.session_state.current_image_index
    total = len(st.session_state.images)
    
    if direction == "next":
        st.session_state.current_image_index = (current + 1) % total
    elif direction == "prev":
        st.session_state.current_image_index = (current - 1) % total
    
    st.rerun()

def reset_carousel():
    """Reset carousel to first image"""
    st.session_state.current_image_index = 0

def display_generated_artwork():
    """Display the generated artwork with carousel navigation and editing controls"""
    
    # Initialize edited images in session state if not present
    if 'edited_images' not in st.session_state:
        st.session_state.edited_images = st.session_state.images.copy()
    
    # Add visual separation
    st.markdown('<div class="artwork-section">', unsafe_allow_html=True)
    st.header("🎨 Generated Artwork")
    
    images = st.session_state.edited_images  # Use edited versions
    
    if not images:
        return
    
    # Ensure current_image_index is within bounds
    if st.session_state.current_image_index >= len(images):
        st.session_state.current_image_index = 0
    
    # Display analysis if available
    if st.session_state.analysis_result:
        with st.expander("📋 View Analysis Details"):
            analysis = st.session_state.analysis_result
            st.markdown("**Themes:** " + analysis.get('themes', 'N/A'))
            st.markdown("**Mood:** " + analysis.get('mood', 'N/A'))
            st.markdown("**Visual Elements:** " + analysis.get('visual_elements', 'N/A'))
            st.markdown("**Generated Prompt:** " + analysis.get('image_prompt', 'N/A'))
    
    # Carousel Container
    st.markdown('<div class="carousel-container">', unsafe_allow_html=True)
    
    # Carousel Header with Navigation
    if len(images) > 1:
        col_nav_left, col_nav_right = st.columns([1, 1])
        
        with col_nav_left:
            if st.button("◀", key="nav_prev", help="Previous image", use_container_width=True):
                navigate_carousel("prev")
        
        with col_nav_right:
            if st.button("▶", key="nav_next", help="Next image", use_container_width=True):
                navigate_carousel("next")
    else:
        # Single image indicator
        st.markdown(f"""
        <div class="carousel-indicator">
            🎨 Generated Interpretation
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Current Image Display with Side-by-Side Layout
    current_index = st.session_state.current_image_index
    current_image = images[current_index]
    
    # Two columns: Image on left, Controls on right
    col_image, col_controls = st.columns([2, 1])
    
    with col_image:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(
            current_image, 
            caption=f"Interpretation {current_index + 1}" if len(images) > 1 else "Generated Interpretation",
            use_container_width=False
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button below image
        img_bytes = get_image_download_link(
            current_image, 
            f"versecanvas_poem_{current_index + 1}.png"
        )
        st.download_button(
            label="📥 Download Current Image",
            data=img_bytes,
            file_name=f"versecanvas_poem_{current_index + 1}.png",
            mime="image/png",
            use_container_width=True,
            key=f"download_current_{current_index}"
        )
        
        # Navigation hints for multiple images
        if len(images) > 1:
            st.markdown("""
            <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                💡 Use ◀ ▶ buttons above to view other interpretations
            </div>
            """, unsafe_allow_html=True)
    
    with col_controls:
        st.markdown('<div class="controls-container">', unsafe_allow_html=True)
        st.markdown('<div class="controls-header"> Edit Current Image</div>', unsafe_allow_html=True)
        add_editing_controls(current_index)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download All button for multiple images
    if len(images) > 1:
        st.markdown("---")
        col_download_all, col_info = st.columns([1, 2])
        
        with col_download_all:
            # Create a simple download all option
            if st.button("📦 Download All Images", use_container_width=True):
                st.info("💡 Use the navigation arrows above to view each image and download them individually.")
        
        with col_info:
            st.markdown(f"""
            <div style='padding: 0.5rem; background: #e8f4f8; border-radius: 5px; font-size: 0.9rem;'>
                📊 <strong>Your Collection:</strong> {len(images)} interpretations generated<br>
                🎯 <strong>Currently Viewing:</strong> Interpretation {current_index + 1}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def add_editing_controls(image_index):
    """Add editing controls for an image with apply button"""
    
    # Get original image
    original_image = st.session_state.images[image_index]
    
    # Initialize reset counter for this image if not exists
    reset_key = f"reset_counter_{image_index}"
    if reset_key not in st.session_state:
        st.session_state[reset_key] = 0
    
    # Use reset counter in widget keys to force reset
    reset_suffix = st.session_state[reset_key]
    
    # Create tabs for different editing options
    tab1, tab2 = st.tabs(["🎨 Image Adjustments", "📝 Add Poem Text"])
    
    with tab1:
        st.markdown("**Adjust Image Properties:**")

        col1, col2, col3 = st.columns(3)

        with col1:
            brightness = st.slider(
                "Brightness", 
                0.1, 2.0, 1.0, 0.1, 
                key=f"brightness_{image_index}_{reset_suffix}",
                help="Adjust image brightness"
            )

        with col2:
            contrast = st.slider(
                "Contrast", 
                0.1, 2.0, 1.0, 0.1, 
                key=f"contrast_{image_index}_{reset_suffix}",
                help="Adjust image contrast"
            )

        with col3:
            blur = st.slider(
                "Blur", 
                0, 5, 0, 1, 
                key=f"blur_{image_index}_{reset_suffix}",
                help="Apply blur effect"
            )
        
        # Show current settings
        if brightness != 1.0 or contrast != 1.0 or blur != 0:
            st.info(f"🎨 Preview: Brightness {brightness:.1f}, Contrast {contrast:.1f}, Blur {blur}")
    
    with tab2:
        st.markdown("**Add Poem Text to Image:**")
        
        # Toggle for text overlay
        enable_text = st.checkbox(
            "Add poem text to image", 
            value=st.session_state.text_overlay_default,
            key=f"enable_text_{image_index}_{reset_suffix}",
            help="Overlay the poem text on the image"
        )

        # Update the default state when user changes it
        if enable_text != st.session_state.text_overlay_default:
            st.session_state.text_overlay_default = enable_text
        
        if enable_text:
            # Text overlay options
            col1, col2 = st.columns(2)
            
            with col1:
                font_size = st.slider("Font Size", 16, 48, 24, 2, key=f"font_size_{image_index}_{reset_suffix}")
                text_position = st.selectbox(
                    "Text Position", 
                    ["center", "top", "bottom", "left", "right"],
                    key=f"position_{image_index}_{reset_suffix}"
                )
                font_style = st.selectbox(
                    "Font Style",
                    ["serif", "sans-serif", "arial", "times", "helvetica"],
                    key=f"font_style_{image_index}_{reset_suffix}"
                )
            
            with col2:
                text_color = st.selectbox(
                    "Text Color",
                    ["White", "Black", "Light Gray", "Dark Gray"],
                    key=f"text_color_{image_index}_{reset_suffix}"
                )
                
                background_opacity = st.slider(
                    "Background Opacity", 
                    0.0, 1.0, 0.7, 0.1,
                    key=f"bg_opacity_{image_index}_{reset_suffix}",
                    help="Opacity of text background"
                )
                
                text_alignment = st.selectbox(
                    "Text Alignment",
                    ["center", "left", "right"],
                    key=f"text_align_{image_index}_{reset_suffix}"
                )
            
            # Color mapping
            color_map = {
                "White": (255, 255, 255),
                "Black": (0, 0, 0),
                "Light Gray": (200, 200, 200),
                "Dark Gray": (80, 80, 80)
            }
            
            selected_color = color_map[text_color]
            
            st.info(f"📝 Text will be added with: {font_style} font, size {font_size}, {text_position} position")
    
    # Apply and Reset buttons
    col_apply, col_reset = st.columns(2)
    
    with col_apply:
        if st.button(f"✨ Apply Changes", key=f"apply_{image_index}_{reset_suffix}", use_container_width=True):
            try:
                # Start with original image
                edited_image = original_image.copy()
                
                # Apply basic edits if any
                if brightness != 1.0 or contrast != 1.0 or blur != 0:
                    edited_image = basic_edit_image(edited_image, brightness, contrast, blur)
                
                # Apply text overlay if enabled
                if enable_text and st.session_state.current_poem:
                    edited_image = add_poem_to_image(
                        image=edited_image,
                        poem_text=st.session_state.current_poem,
                        font_size=font_size,
                        font_color=selected_color,
                        position=text_position,
                        background_opacity=background_opacity,
                        font_style=font_style,
                        text_alignment=text_alignment
                    )
                
                # Update the session state with edited image
                st.session_state.edited_images[image_index] = edited_image
                st.success("✅ Changes applied!")
                st.rerun()  # Refresh to show updated image
            except Exception as e:
                st.error(f"Error applying changes: {str(e)}")
    
    with col_reset:
        if st.button(f"🔄 Reset to Original", key=f"reset_{image_index}_{reset_suffix}", use_container_width=True):
            try:
                # Reset to original image
                st.session_state.edited_images[image_index] = original_image.copy()
                # Increment reset counter to create new widget keys (this resets sliders)
                st.session_state[reset_key] += 1
                st.success("✅ Reset to original!")
                st.rerun()  # Refresh to show original image and reset sliders
            except Exception as e:
                st.error(f"Error resetting image: {str(e)}")
    
def get_image_download_link(image, filename):
    """Convert PIL image to bytes for download"""
    img_buffer = io.BytesIO()
    image.save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    return img_bytes

# Information sidebar
def show_info():
    with st.sidebar:
        st.markdown("---")
        st.subheader("ℹ️ How it works")
        st.markdown("""
        1. **Enter your poem** in any supported language
        2. **AI analyzes** themes, emotions, and visual elements
        3. **Images are generated** based on the analysis
        4. **Edit and customize** your artwork
        5. **Download** your creation
        """)
        
        st.subheader("🔧 Technical Details")
        st.markdown("""
        - **AI Models**: Google Gemini, Imagen
        - **Platform**: Vertex AI
        - **Languages**: Multi-language support
        - **Editing**: Real-time image processing
        """)
        
        # Add a button to clear the session
        if st.button("🗑️ Clear All"):
            st.session_state.images = []
            st.session_state.edited_images = []
            st.session_state.analysis_result = None
            st.session_state.current_poem = ""
            st.session_state.generation_complete = False
            st.session_state.text_overlay_enabled = {}
            reset_carousel()
            # Note: Keep text_overlay_default to remember user preference
            st.rerun()

if __name__ == "__main__":
    # Only show debug if explicitly requested
    debug_credentials()  # This is now safe since it checks for debug parameter
    show_info()
    main()