"""
Image Editing Module
Basic image editing capabilities using PIL for the VerseCanvas application.
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageEditor:
    """Basic image editing class with PIL operations."""
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image brightness.
        
        Args:
            image (Image.Image): PIL Image to adjust
            factor (float): Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
            
        Returns:
            Image.Image: Adjusted image
        """
        try:
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(factor)
        except Exception as e:
            logger.error(f"Error adjusting brightness: {str(e)}")
            return image

    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image contrast.
        
        Args:
            image (Image.Image): PIL Image to adjust
            factor (float): Contrast factor (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)
            
        Returns:
            Image.Image: Adjusted image
        """
        try:
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(factor)
        except Exception as e:
            logger.error(f"Error adjusting contrast: {str(e)}")
            return image

    @staticmethod
    def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
        """
        Adjust image saturation.
        
        Args:
            image (Image.Image): PIL Image to adjust
            factor (float): Saturation factor (1.0 = no change, >1.0 = more saturated, <1.0 = less saturated)
            
        Returns:
            Image.Image: Adjusted image
        """
        try:
            enhancer = ImageEnhance.Color(image)
            return enhancer.enhance(factor)
        except Exception as e:
            logger.error(f"Error adjusting saturation: {str(e)}")
            return image

    @staticmethod
    def apply_blur(image: Image.Image, radius: int) -> Image.Image:
        """
        Apply Gaussian blur to image.
        
        Args:
            image (Image.Image): PIL Image to blur
            radius (int): Blur radius (0 = no blur, higher = more blur)
            
        Returns:
            Image.Image: Blurred image
        """
        try:
            if radius <= 0:
                return image
            return image.filter(ImageFilter.GaussianBlur(radius=radius))
        except Exception as e:
            logger.error(f"Error applying blur: {str(e)}")
            return image

    @staticmethod
    def apply_sharpen(image: Image.Image, factor: float = 1.0) -> Image.Image:
        """
        Apply sharpening to image.
        
        Args:
            image (Image.Image): PIL Image to sharpen
            factor (float): Sharpening factor (1.0 = no change, >1.0 = sharper)
            
        Returns:
            Image.Image: Sharpened image
        """
        try:
            if factor <= 0:
                return image
            enhancer = ImageEnhance.Sharpness(image)
            return enhancer.enhance(factor)
        except Exception as e:
            logger.error(f"Error applying sharpen: {str(e)}")
            return image

    @staticmethod
    def resize_image(image: Image.Image, size: Tuple[int, int], maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image to specified dimensions.
        
        Args:
            image (Image.Image): PIL Image to resize
            size (Tuple[int, int]): Target size (width, height)
            maintain_aspect (bool): Whether to maintain aspect ratio
            
        Returns:
            Image.Image: Resized image
        """
        try:
            if maintain_aspect:
                # Calculate size maintaining aspect ratio
                image.thumbnail(size, Image.Resampling.LANCZOS)
                return image
            else:
                return image.resize(size, Image.Resampling.LANCZOS)
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            return image

    @staticmethod
    def crop_center(image: Image.Image, crop_size: Tuple[int, int]) -> Image.Image:
        """
        Crop image from center.
        
        Args:
            image (Image.Image): PIL Image to crop
            crop_size (Tuple[int, int]): Crop size (width, height)
            
        Returns:
            Image.Image: Cropped image
        """
        try:
            width, height = image.size
            crop_width, crop_height = crop_size
            
            # Calculate crop box
            left = (width - crop_width) // 2
            top = (height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height
            
            return image.crop((left, top, right, bottom))
        except Exception as e:
            logger.error(f"Error cropping image: {str(e)}")
            return image

    @staticmethod
    def apply_filter(image: Image.Image, filter_type: str) -> Image.Image:
        """
        Apply various filters to image.
        
        Args:
            image (Image.Image): PIL Image to filter
            filter_type (str): Type of filter to apply
            
        Returns:
            Image.Image: Filtered image
        """
        try:
            filter_map = {
                'blur': ImageFilter.BLUR,
                'contour': ImageFilter.CONTOUR,
                'detail': ImageFilter.DETAIL,
                'edge_enhance': ImageFilter.EDGE_ENHANCE,
                'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
                'emboss': ImageFilter.EMBOSS,
                'find_edges': ImageFilter.FIND_EDGES,
                'smooth': ImageFilter.SMOOTH,
                'smooth_more': ImageFilter.SMOOTH_MORE,
                'sharpen': ImageFilter.SHARPEN
            }
            
            if filter_type in filter_map:
                return image.filter(filter_map[filter_type])
            else:
                logger.warning(f"Unknown filter type: {filter_type}")
                return image
                
        except Exception as e:
            logger.error(f"Error applying filter {filter_type}: {str(e)}")
            return image

    @staticmethod
    def adjust_gamma(image: Image.Image, gamma: float) -> Image.Image:
        """
        Adjust image gamma.
        
        Args:
            image (Image.Image): PIL Image to adjust
            gamma (float): Gamma value (1.0 = no change, <1.0 = brighter, >1.0 = darker)
            
        Returns:
            Image.Image: Gamma-adjusted image
        """
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Apply gamma correction
            gamma_corrected = np.power(img_array / 255.0, gamma) * 255.0
            gamma_corrected = np.clip(gamma_corrected, 0, 255).astype(np.uint8)
            
            # Convert back to PIL Image
            return Image.fromarray(gamma_corrected)
            
        except Exception as e:
            logger.error(f"Error adjusting gamma: {str(e)}")
            return image

    @staticmethod
    def create_vignette(image: Image.Image, intensity: float = 0.5) -> Image.Image:
        """
        Apply vignette effect to image.
        
        Args:
            image (Image.Image): PIL Image to apply vignette to
            intensity (float): Vignette intensity (0.0 = no effect, 1.0 = strong effect)
            
        Returns:
            Image.Image: Image with vignette effect
        """
        try:
            width, height = image.size
            
            # Create vignette mask
            vignette = Image.new('L', (width, height), 0)
            
            # Calculate center and radius
            center_x, center_y = width // 2, height // 2
            max_radius = min(width, height) // 2
            
            # Create gradient from center
            for y in range(height):
                for x in range(width):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    if distance <= max_radius:
                        # Linear gradient
                        value = int(255 * (1 - (distance / max_radius) * intensity))
                        vignette.putpixel((x, y), value)
                    else:
                        vignette.putpixel((x, y), int(255 * (1 - intensity)))
            
            # Apply vignette
            result = Image.composite(image, Image.new('RGB', image.size, (0, 0, 0)), vignette)
            return result
            
        except Exception as e:
            logger.error(f"Error creating vignette: {str(e)}")
            return image

# Convenience function for basic editing (used by main app)
def basic_edit_image(image: Image.Image, brightness: float = 1.0, contrast: float = 1.0, blur: int = 0) -> Image.Image:
    """
    Apply basic edits to an image.
    
    Args:
        image (Image.Image): PIL Image to edit
        brightness (float): Brightness adjustment factor
        contrast (float): Contrast adjustment factor
        blur (int): Blur radius
        
    Returns:
        Image.Image: Edited image
    """
    try:
        editor = ImageEditor()
        
        # Apply edits in sequence
        edited_image = image.copy()
        
        if brightness != 1.0:
            edited_image = editor.adjust_brightness(edited_image, brightness)
        
        if contrast != 1.0:
            edited_image = editor.adjust_contrast(edited_image, contrast)
        
        if blur > 0:
            edited_image = editor.apply_blur(edited_image, blur)
        
        return edited_image
        
    except Exception as e:
        logger.error(f"Error in basic_edit_image: {str(e)}")
        return image

# Advanced editing function
def advanced_edit_image(
    image: Image.Image,
    brightness: float = 1.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    blur: int = 0,
    sharpen: float = 1.0,
    gamma: float = 1.0,
    filter_type: Optional[str] = None,
    vignette_intensity: float = 0.0
) -> Image.Image:
    """
    Apply advanced edits to an image.
    
    Args:
        image (Image.Image): PIL Image to edit
        brightness (float): Brightness adjustment factor
        contrast (float): Contrast adjustment factor
        saturation (float): Saturation adjustment factor
        blur (int): Blur radius
        sharpen (float): Sharpening factor
        gamma (float): Gamma adjustment factor
        filter_type (str): Filter type to apply
        vignette_intensity (float): Vignette effect intensity
        
    Returns:
        Image.Image: Edited image
    """
    try:
        editor = ImageEditor()
        
        # Apply edits in sequence
        edited_image = image.copy()
        
        # Basic adjustments
        if brightness != 1.0:
            edited_image = editor.adjust_brightness(edited_image, brightness)
        
        if contrast != 1.0:
            edited_image = editor.adjust_contrast(edited_image, contrast)
        
        if saturation != 1.0:
            edited_image = editor.adjust_saturation(edited_image, saturation)
        
        # Gamma adjustment
        if gamma != 1.0:
            edited_image = editor.adjust_gamma(edited_image, gamma)
        
        # Sharpening
        if sharpen != 1.0:
            edited_image = editor.apply_sharpen(edited_image, sharpen)
        
        # Blur
        if blur > 0:
            edited_image = editor.apply_blur(edited_image, blur)
        
        # Filters
        if filter_type:
            edited_image = editor.apply_filter(edited_image, filter_type)
        
        # Vignette
        if vignette_intensity > 0:
            edited_image = editor.create_vignette(edited_image, vignette_intensity)
        
        return edited_image
        
    except Exception as e:
        logger.error(f"Error in advanced_edit_image: {str(e)}")
        return image

# Example usage and testing
if __name__ == "__main__":
    # Test with a sample image
    try:
        # Create a test image
        test_image = Image.new('RGB', (400, 300), color=(100, 150, 200))
        
        # Apply basic edits
        edited = basic_edit_image(test_image, brightness=1.2, contrast=1.1, blur=1)
        print("Basic editing test successful!")
        
        # Apply advanced edits
        advanced = advanced_edit_image(
            test_image,
            brightness=1.1,
            contrast=1.2,
            saturation=1.3,
            sharpen=1.1,
            vignette_intensity=0.3
        )
        print("Advanced editing test successful!")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")