"""
Image Generation Module
Uses Google Imagen on Vertex AI to generate images from poem analysis.
"""

import os
import json
import json
import logging
import tempfile
from typing import List, Optional
from PIL import Image
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from PIL import Image
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_config_and_credentials():
    """
    Get configuration and credentials with proper scopes for Vertex AI
    """
    project_id = None
    location = None
    credentials = None

    try:
        # Attempt to load from Streamlit secrets (for cloud deployment)
        import streamlit as st
        if hasattr(st, 'secrets') and 'PROJECT_ID' in st.secrets:
            project_id = st.secrets['PROJECT_ID']
            location = st.secrets.get('LOCATION', 'us-central1')
            
            logger.info("Using Streamlit secrets for configuration")
            
            if 'GOOGLE_CREDENTIALS' in st.secrets:
                try:
                    credentials_json = st.secrets['GOOGLE_CREDENTIALS']
                    credentials_info = json.loads(credentials_json)
                    
                    # Create credentials with cloud platform scope (sufficient for Vertex AI)
                    credentials = service_account.Credentials.from_service_account_info(
                        credentials_info,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    logger.info("Successfully loaded credentials with cloud platform scope")
                    
                    return {
                        'project_id': project_id,
                        'location': location,
                        'credentials': credentials
                    }
                        
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logger.warning(f"Failed to parse GOOGLE_CREDENTIALS JSON: {e}")
            
            # Fallback without explicit credentials
            logger.warning("Using project config without explicit credentials")
            return {
                'project_id': project_id,
                'location': location,
                'credentials': None
            }
            
    except (ImportError, AttributeError, KeyError) as e:
        logger.info(f"Streamlit secrets not available: {e}")

    # Fallback to environment variables (for local development)
    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION', 'us-central1')
    
    if not project_id:
        raise ValueError(
            "PROJECT_ID not found. Please set it in:\n"
            "1. Streamlit secrets (for cloud deployment), or\n"
            "2. Environment variables (for local development)"
        )
    
    # For local development, try explicit service account file
    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if service_account_path and os.path.exists(service_account_path):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            logger.info(f"Using service account file with cloud platform scope: {service_account_path}")
        except Exception as e:
            logger.warning(f"Failed to load service account file: {e}")
            credentials = None
    else:
        logger.info("Using default Google Cloud authentication")
        credentials = None
    
    return {
        'project_id': project_id,
        'location': location,
        'credentials': credentials
    }

class ImageGenerator:
    def __init__(self):
        """Initialize the image generator with Vertex AI."""
        try:
            config = get_config_and_credentials()
            config = get_config_and_credentials()
            self.project_id = config['project_id']
            self.location = config['location']
            credentials = config['credentials']
            credentials = config['credentials']
            
            # Initialize Vertex AI with explicit credentials if provided
            vertexai.init(project=self.project_id, location=self.location, credentials=credentials)
            # Initialize Vertex AI with explicit credentials if provided
            vertexai.init(project=self.project_id, location=self.location, credentials=credentials)
            
            # Load the Imagen model
            self.model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
            
            logger.info("ImageGenerator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ImageGenerator: {str(e)}")
            raise

    def generate_images(self, prompt: str, num_images: int = 2) -> List[Image.Image]:
        """
        Generate images based on a text prompt.
        
        Args:
            prompt (str): The text prompt for image generation
            num_images (int): Number of images to generate (1-4)
            
        Returns:
            List[Image.Image]: List of generated PIL Images
        """
        try:
            # Ensure num_images is within bounds
            num_images = max(1, min(num_images, 4))
            
            logger.info(f"Generating {num_images} images with prompt: {prompt[:100]}...")
            
            # Generate images using Imagen
            response = self.model.generate_images(
                prompt=prompt,
                number_of_images=num_images,
                seed=None,  # Random seed for variety
                add_watermark=False,
                safety_filter_level="block_few",
                person_generation="allow_adult"
            )
            
            # Convert to PIL Images
            pil_images = []
            for i, image in enumerate(response.images):
                try:
                    # Convert to PIL Image
                    pil_image = self._vertex_image_to_pil(image)
                    pil_images.append(pil_image)
                    logger.info(f"Successfully converted image {i+1} to PIL format")
                except Exception as e:
                    logger.error(f"Failed to convert image {i+1}: {str(e)}")
            
            logger.info(f"Successfully generated {len(pil_images)} images")
            return pil_images
            
        except Exception as e:
            logger.error(f"Error generating images: {str(e)}")
            return []

    def _vertex_image_to_pil(self, vertex_image) -> Image.Image:
        """
        Convert a Vertex AI Image to PIL Image.
        
        Args:
            vertex_image: Vertex AI Image object
            
        Returns:
            Image.Image: PIL Image object
        """
        try:
            # Save to temporary file and reload as PIL
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                vertex_image.save(temp_file.name)
                pil_image = Image.open(temp_file.name)
                # Convert to RGB if necessary
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                # Make a copy to avoid file handle issues
                result_image = pil_image.copy()
                pil_image.close()
                
                # Clean up temp file
                try:
                    os.unlink(temp_file.name)
                except:
                    pass  # Ignore cleanup errors
                    
                return result_image
                # Make a copy to avoid file handle issues
                result_image = pil_image.copy()
                pil_image.close()
                
                # Clean up temp file
                try:
                    os.unlink(temp_file.name)
                except:
                    pass  # Ignore cleanup errors
                    
                return result_image
                
        except Exception as e:
            logger.error(f"Error converting Vertex AI image to PIL: {str(e)}")
            raise

    def enhance_prompt(self, base_prompt: str, style_modifiers: Optional[str] = None) -> str:
        """
        Enhance the base prompt with additional style and quality modifiers.
        
        Args:
            base_prompt (str): The base prompt from poem analysis
            style_modifiers (str): Additional style modifications
            
        Returns:
            str: Enhanced prompt
        """
        enhancements = [
            "high quality",
            "detailed",
            "artistic composition",
            "beautiful lighting",
            "cinematic",
            "masterpiece"
        ]
        
        # Add style modifiers if provided
        if style_modifiers:
            enhancements.append(style_modifiers)
        
        # Combine base prompt with enhancements
        enhanced_prompt = f"{base_prompt}, {', '.join(enhancements)}"
        
        return enhanced_prompt

    def generate_with_variations(self, prompt: str, num_images: int = 2) -> List[Image.Image]:
        """
        Generate images with slight prompt variations for diversity.
        
        Args:
            prompt (str): The base prompt
            num_images (int): Number of images to generate
            
        Returns:
            List[Image.Image]: List of generated images
        """
        try:
            # Create prompt variations
            variations = self._create_prompt_variations(prompt, num_images)
            
            all_images = []
            for i, variation in enumerate(variations):
                try:
                    logger.info(f"Generating image {i+1} with variation...")
                    images = self.generate_images(variation, 1)
                    if images:
                        all_images.extend(images)
                except Exception as e:
                    logger.error(f"Failed to generate variation {i+1}: {str(e)}")
            
            return all_images
            
        except Exception as e:
            logger.error(f"Error generating variations: {str(e)}")
            return self.generate_images(prompt, num_images)  # Fallback to regular generation

    def _create_prompt_variations(self, base_prompt: str, num_variations: int) -> List[str]:
        """Create slight variations of the base prompt."""
        
        style_variations = [
            "atmospheric",
            "dreamy",
            "ethereal",
            "mysterious",
            "serene",
            "dramatic",
            "peaceful",
            "enchanting"
        ]
        
        lighting_variations = [
            "golden hour lighting",
            "soft natural light",
            "misty atmosphere",
            "warm glow",
            "cool blue tones",
            "sunset colors"
        ]
        
        variations = []
        for i in range(num_variations):
            # Add different modifiers for each variation
            style_mod = style_variations[i % len(style_variations)]
            lighting_mod = lighting_variations[i % len(lighting_variations)]
            
            variation = f"{base_prompt}, {style_mod}, {lighting_mod}"
            variations.append(variation)
        
        return variations

# Convenience function for the main app
def generate_poem_image(prompt: str, num_images: int = 2) -> List[Image.Image]:
    """
    Convenience function to generate images from a poem analysis prompt.
    
    Args:
        prompt (str): The image generation prompt
        num_images (int): Number of images to generate
        
    Returns:
        List[Image.Image]: List of generated PIL Images
    """
    try:
        generator = ImageGenerator()
        
        # Enhance the prompt for better results
        enhanced_prompt = generator.enhance_prompt(prompt)
        
        # Generate images
        images = generator.generate_images(enhanced_prompt, num_images)
        
        if not images:
            logger.warning("No images generated, trying with original prompt...")
            images = generator.generate_images(prompt, num_images)
        
        return images
        
    except Exception as e:
        logger.error(f"Error in generate_poem_image function: {str(e)}")
        return []

# Example usage and testing
if __name__ == "__main__":
    # Test the image generator
    test_prompt = """
    A peaceful forest path in watercolor style, with golden sunlight filtering through 
    autumn leaves, creating a dreamy atmosphere of contemplation and choice, 
    two paths diverging in a yellow wood, soft natural colors, artistic composition
    """
    
    try:
        images = generate_poem_image(test_prompt, 2)
        if images:
            print(f"Successfully generated {len(images)} images!")
            for i, img in enumerate(images):
                print(f"Image {i+1}: {img.size} pixels")
        else:
            print("No images were generated")
    except Exception as e:
        print(f"Test failed: {str(e)}")