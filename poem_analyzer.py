"""
Poem Analysis Module
Uses Google Gemini to analyze poetry and extract visual elements for image generation.
"""

import os
import json
import logging
import json
import logging
from google import genai
from google.genai.types import GenerateContentConfig
from google.oauth2 import service_account
import vertexai
from google.oauth2 import service_account
import vertexai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_config_and_credentials():
    """
    Get configuration and credentials with proper scopes for Vertex AI
    Supports both JSON string format and individual TOML fields
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
            
            # Method 1: Try GOOGLE_CREDENTIALS as JSON string
            if 'GOOGLE_CREDENTIALS' in st.secrets:
                try:
                    credentials_json = st.secrets['GOOGLE_CREDENTIALS']
                    credentials_info = json.loads(credentials_json)
                    
                    # Create credentials with cloud platform scope
                    credentials = service_account.Credentials.from_service_account_info(
                        credentials_info,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    logger.info("Successfully loaded credentials from GOOGLE_CREDENTIALS JSON")
                    
                    return {
                        'project_id': project_id,
                        'location': location,
                        'credentials': credentials
                    }
                        
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logger.warning(f"Failed to parse GOOGLE_CREDENTIALS JSON: {e}")
            
            # Method 2: Try individual credential fields (google_credentials table)
            if 'google_credentials' in st.secrets:
                try:
                    cred_dict = dict(st.secrets['google_credentials'])
                    
                    # Create credentials with cloud platform scope
                    credentials = service_account.Credentials.from_service_account_info(
                        cred_dict,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    logger.info("Successfully loaded credentials from individual fields")
                    
                    return {
                        'project_id': project_id,
                        'location': location,
                        'credentials': credentials
                    }
                    
                except Exception as e:
                    logger.warning(f"Failed to load credentials from individual fields: {e}")
            
            # If we have project_id but no working credentials, continue without explicit credentials
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

class PoemAnalyzer:
    def __init__(self):
        """Initialize the poem analyzer with Gemini client."""
        try:
            config = get_config_and_credentials()
            config = get_config_and_credentials()
            project_id = config['project_id']
            location = config['location']
            credentials = config['credentials']

            # Initialize Vertex AI with explicit credentials if provided
            vertexai.init(project=project_id, location=location, credentials=credentials)
            credentials = config['credentials']

            # Initialize Vertex AI with explicit credentials if provided
            vertexai.init(project=project_id, location=location, credentials=credentials)
            
            # Initialize the Gemini client
            # Initialize the Gemini client
            self.client = genai.Client(vertexai=True, project=project_id, location=location)
            self.model_id = "gemini-2.0-flash-001"
            
            
            logger.info("PoemAnalyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PoemAnalyzer: {str(e)}")
            raise

    def analyze_poem(self, poem_text, language="English", art_style="Photorealistic", mood_intensity=1.0):
        """
        Analyze a poem and extract visual elements for image generation.
        
        Args:
            poem_text (str): The poem to analyze
            language (str): Language of the poem
            art_style (str): Preferred artistic style
            mood_intensity (float): Intensity of mood expression (0.1-2.0)
            
        Returns:
            dict: Analysis results with themes, mood, visual elements, and image prompt
        """
        try:
            # Construct analysis prompt
            analysis_prompt = self._create_analysis_prompt(poem_text, language, art_style, mood_intensity)
            
            # Get analysis from Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=analysis_prompt,
                config=GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                    response_mime_type="application/json"
                )
            )
            
            # Parse the JSON response
            if response.text is not None:
                analysis_result = json.loads(response.text)
            else:
                logger.error("Response text is None.")
                return self._fallback_analysis(poem_text, language, art_style, mood_intensity)
            if response.text is not None:
                analysis_result = json.loads(response.text)
            else:
                logger.error("Response text is None.")
                return self._fallback_analysis(poem_text, language, art_style, mood_intensity)
            
            logger.info("Poem analysis completed successfully")
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            # Fallback to text analysis if JSON parsing fails
            return self._fallback_analysis(poem_text, language, art_style, mood_intensity)
            
        except Exception as e:
            logger.error(f"Error during poem analysis: {str(e)}")
            return None

    def _create_analysis_prompt(self, poem_text, language, art_style, mood_intensity):
        """Create a detailed prompt for poem analysis."""
        
        prompt = f"""
        You are an expert poetry analyst and visual artist. Analyze the following poem and provide a comprehensive breakdown for creating a background image that captures its essence.

        **Poem** (Language: {language}):
        {poem_text}

        **Instructions:**
        1. Analyze the poem's core themes, emotions, and narrative
        2. Extract specific visual elements that could be depicted in an image
        3. Consider the requested art style: {art_style}
        4. Adjust emotional intensity by factor: {mood_intensity}
        5. Create a detailed prompt for image generation

        **Please respond in JSON format with exactly these fields:**
        {{
            "themes": "Main themes and concepts (comma-separated)",
            "mood": "Overall emotional tone and atmosphere",
            "visual_elements": "Specific objects, colors, settings, and visual details",
            "narrative": "Story or progression if present",
            "style_notes": "How the {art_style} style should be applied",
            "image_prompt": "Detailed prompt for image generation (combine all analysis into a rich, descriptive prompt suitable for AI image generation)"
        }}

        **Image Prompt Guidelines:**
        - Be specific about colors, lighting, composition
        - Include atmosphere and mood descriptors
        - Mention the art style: {art_style}
        - Incorporate key visual elements from the poem
        - Adjust emotional intensity according to mood_intensity: {mood_intensity}
        - Make it suitable for a background image that complements text
        - Avoid including text or people's faces directly
        - Focus on environment, atmosphere, and symbolic elements
        """
        
        return prompt

    def _fallback_analysis(self, poem_text, language, art_style, mood_intensity):
        """Fallback analysis method if JSON parsing fails."""
        try:
            # Simplified prompt for fallback
            simple_prompt = f"""
            Analyze this poem and create a visual description for image generation:
            
            Poem: {poem_text}
            
            Focus on:
            - Main themes and emotions
            - Visual elements (colors, objects, settings)
            - Atmosphere and mood
            - Art style: {art_style}
            
            Create a detailed prompt for generating a background image.
            """
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=simple_prompt,
                config=GenerateContentConfig(temperature=0.7)
            )
            
            # Create structured response from text
            result = {
                "themes": "Nature, emotion, beauty",
                "mood": "Contemplative and serene",
                "visual_elements": "Natural landscapes, soft colors",
                "narrative": "A journey of reflection",
                "style_notes": f"Rendered in {art_style} style",
                "image_prompt": response.text
            }
            
            logger.info("Fallback analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {str(e)}")
            return self._default_analysis(art_style)

    def _default_analysis(self, art_style):
        """Default analysis as last resort."""
        return {
            "themes": "Poetry, creativity, expression",
            "mood": "Artistic and inspiring",
            "visual_elements": "Abstract forms, flowing lines, gentle colors",
            "narrative": "A creative expression",
            "style_notes": f"Artistic representation in {art_style} style",
            "image_prompt": f"A beautiful, abstract artistic composition in {art_style} style, with flowing forms and gentle colors, representing creativity and poetic expression, suitable as a background image"
        }

# Convenience function for the main app
def analyze_poem(poem_text, language="English", art_style="Photorealistic", mood_intensity=1.0):
    """
    Convenience function to analyze a poem.
    
    Args:
        poem_text (str): The poem to analyze
        language (str): Language of the poem
        art_style (str): Preferred artistic style
        mood_intensity (float): Intensity of mood expression
        
    Returns:
        dict: Analysis results
    """
    try:
        analyzer = PoemAnalyzer()
        return analyzer.analyze_poem(poem_text, language, art_style, mood_intensity)
    except Exception as e:
        logger.error(f"Error in analyze_poem function: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Test the analyzer
    test_poem = """
    Two roads diverged in a yellow wood,
    And sorry I could not travel both
    And be one traveler, long I stood
    And looked down one as far as I could
    To where it bent in the undergrowth;
    """
    
    result = analyze_poem(test_poem, "English", "Watercolor", 1.2)
    if result:
        print("Analysis successful!")
        print(json.dumps(result, indent=2))
    else:
        print("Analysis failed!")