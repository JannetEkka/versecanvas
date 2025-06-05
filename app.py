import streamlit as st
import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv
from PIL import Image
import io
import base64

# Import our custom modules
from poem_analyzer import analyze_poem
from image_generator import generate_poem_image
from image_editor import basic_edit_image

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="VerseCanvas - Poetry to Visual Art",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'images' not in st.session_state:
    st.session_state.images = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'current_poem' not in st.session_state:
    st.session_state.current_poem = ""
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
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
</style>
""", unsafe_allow_html=True)

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
        <div style='text-align: center; padding: 3rem 0; color: #6c757d;'>
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
                st.session_state.generation_complete = True
                
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

def display_generated_artwork():
    """Display the generated artwork with editing controls"""
    
    # Add visual separation
    st.markdown('<div class="artwork-section">', unsafe_allow_html=True)
    st.header("🎨 Generated Artwork")
    
    images = st.session_state.images
    
    if not images:
        return
    
    # Display analysis if available
    if st.session_state.analysis_result:
        with st.expander("📋 View Analysis Details"):
            analysis = st.session_state.analysis_result
            st.markdown("**Themes:** " + analysis.get('themes', 'N/A'))
            st.markdown("**Mood:** " + analysis.get('mood', 'N/A'))
            st.markdown("**Visual Elements:** " + analysis.get('visual_elements', 'N/A'))
            st.markdown("**Generated Prompt:** " + analysis.get('image_prompt', 'N/A'))
    
    st.subheader("Generated Images")
    
    # Use columns for better layout when multiple images
    if len(images) > 1:
        cols = st.columns(min(len(images), 2))
        for i, img in enumerate(images):
            with cols[i % 2]:
                st.image(img, caption=f"Interpretation {i+1}", use_container_width=True)
                
                # Add editing controls for each image
                with st.expander(f"✏️ Edit Image {i+1}"):
                    edited_img = add_editing_controls(img, i)

                    # Always show the result (edited or original)
                    if edited_img:
                        st.image(edited_img, caption=f"Edited Image {i+1}", use_container_width=True)
                        
                        # Download button
                        img_bytes = get_image_download_link(edited_img, f"versecanvas_poem_{i+1}.png")
                        st.download_button(
                            label=f"📥 Download Image {i+1}",
                            data=img_bytes,
                            file_name=f"versecanvas_poem_{i+1}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error("Could not process image for editing")
    else:
        # Single image - full width
        img = images[0]
        st.image(img, caption="Generated Interpretation", use_container_width=True)
        
        # Add editing controls
        with st.expander("✏️ Edit Image"):
            edited_img = add_editing_controls(img, 0)

            if edited_img:
                st.image(edited_img, caption="Edited Image", use_container_width=True)
                
                # Download button
                img_bytes = get_image_download_link(edited_img, "versecanvas_poem.png")
                st.download_button(
                    label="📥 Download Image",
                    data=img_bytes,
                    file_name="versecanvas_poem.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.error("Could not process image for editing")

def add_editing_controls(image, image_index):
    """Add basic editing controls for an image"""
    st.markdown("**Adjust Image Properties:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        brightness = st.slider(
            "Brightness", 
            0.1, 2.0, 1.0, 0.1, 
            key=f"brightness_{image_index}"
        )

    with col2:
        contrast = st.slider(
            "Contrast", 
            0.1, 2.0, 1.0, 0.1, 
            key=f"contrast_{image_index}"
        )

    with col3:
        blur = st.slider(
            "Blur", 
            0, 5, 0, 1, 
            key=f"blur_{image_index}"
        )

    # Always return an image - either edited or original
    try:
        # Apply edits (even if values are default, it will return the original)
        edited_image = basic_edit_image(image, brightness, contrast, blur)
        return edited_image
    except Exception as e:
        st.error(f"Error editing image: {str(e)}")
        return image  # Return original image if editing fails
    
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
            st.session_state.analysis_result = None
            st.session_state.current_poem = ""
            st.session_state.generation_complete = False
            st.rerun()

if __name__ == "__main__":
    show_info()
    main()