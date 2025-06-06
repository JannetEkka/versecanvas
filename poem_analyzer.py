"""
Poem Analysis Module
Uses Google Gemini to analyze poetry and extract visual elements for image generation.
"""

import os
from google import genai
from google.genai.types import GenerateContentConfig
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_config():
    """Get configuration from either Streamlit secrets or environment variables."""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        import streamlit as st
        if hasattr(st, 'secrets') and 'PROJECT_ID' in st.secrets:
            config = {
                'project_id': st.secrets['PROJECT_ID'],
                'location': st.secrets.get('LOCATION', 'us-central1')
            }
            
            # Handle Google Cloud authentication for Streamlit Cloud
            if 'GOOGLE_CREDENTIALS' in st.secrets:
                import json
                from google.oauth2 import service_account
                
                # Parse the service account credentials
                credentials_info = json.loads(st.secrets['GOOGLE_CREDENTIALS'])
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                
                # Set the credentials for Google Cloud libraries
                import os
                # This is a bit hacky but works for most Google Cloud libraries
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'temp_creds.json'
                with open('temp_creds.json', 'w') as f:
                    json.dump(credentials_info, f)
            
            return config
    except (ImportError, AttributeError, KeyError):
        pass
    
    # Fallback to environment variables (for local development)
    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION', 'us-central1')
    
    if not project_id:
        raise ValueError("PROJECT_ID not found in secrets or environment variables")
    
    return {
        'project_id': project_id,
        'location': location
    }

class PoemAnalyzer:
    def __init__(self):
        """Initialize the poem analyzer with Gemini client."""
        try:
            config = get_config()
            project_id = config['project_id']
            location = config['location']
            
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
            analysis_result = json.loads(response.text) # type: ignore
            
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