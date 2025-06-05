#!/usr/bin/env python3
"""
Setup and Testing Script for VerseCanvas
Helps verify your environment and test core functionality
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set."""
    print("🔍 Checking environment configuration...")
    
    required_vars = ['PROJECT_ID', 'LOCATION']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\n📝 Please create a .env file with:")
        print("PROJECT_ID=your-google-cloud-project-id")
        print("LOCATION=us-central1")
        return False
    
    print("✅ Environment variables configured")
    print(f"   PROJECT_ID: {os.getenv('PROJECT_ID')}")
    print(f"   LOCATION: {os.getenv('LOCATION')}")
    return True

def check_dependencies():
    """Check if all required Python packages are installed."""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        'streamlit',
        'google-genai',
        'google-cloud-aiplatform',
        'vertexai',
        'python-dotenv',
        'Pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_gcloud_auth():
    """Check if gcloud is authenticated."""
    print("\n🔍 Checking Google Cloud authentication...")
    
    try:
        result = subprocess.run(['gcloud', 'auth', 'list'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'ACTIVE' in result.stdout:
            print("✅ Google Cloud authentication active")
            return True
        else:
            print("❌ Google Cloud not authenticated")
            print("Run: gcloud auth login")
            print("Then: gcloud auth application-default login")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ gcloud CLI not found or not responding")
        print("Please install Google Cloud CLI: https://cloud.google.com/sdk/docs/install")
        return False

def test_poem_analyzer():
    """Test the poem analyzer module."""
    print("\n🔍 Testing poem analyzer...")
    
    try:
        from poem_analyzer import analyze_poem
        
        test_poem = "Roses are red, violets are blue, AI is amazing, and so are you!"
        
        result = analyze_poem(test_poem, "English", "Watercolor", 1.0)
        
        if result and isinstance(result, dict):
            print("✅ Poem analyzer working")
            print(f"   Detected themes: {result.get('themes', 'N/A')[:50]}...")
            return True
        else:
            print("❌ Poem analyzer failed")
            return False
            
    except Exception as e:
        print(f"❌ Poem analyzer error: {str(e)}")
        return False

def test_image_generator():
    """Test the image generator module."""
    print("\n🔍 Testing image generator...")
    
    try:
        from image_generator import generate_poem_image
        
        test_prompt = "A beautiful watercolor painting of roses and violets"
        
        # Try to generate just one small test image
        images = generate_poem_image(test_prompt, 1)
        
        if images and len(images) > 0:
            print("✅ Image generator working")
            print(f"   Generated {len(images)} image(s)")
            return True
        else:
            print("❌ Image generator failed - no images returned")
            return False
            
    except Exception as e:
        print(f"❌ Image generator error: {str(e)}")
        print("   This might be due to API quotas or permissions")
        return False

def test_image_editor():
    """Test the image editor module."""
    print("\n🔍 Testing image editor...")
    
    try:
        from image_editor import basic_edit_image
        from PIL import Image
        
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        
        # Apply basic edits
        edited = basic_edit_image(test_image, brightness=1.2, contrast=1.1)
        
        if edited and edited.size == (100, 100):
            print("✅ Image editor working")
            return True
        else:
            print("❌ Image editor failed")
            return False
            
    except Exception as e:
        print(f"❌ Image editor error: {str(e)}")
        return False

def create_sample_env():
    """Create a sample .env file if it doesn't exist."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("\n📝 Creating sample .env file...")
        
        sample_content = """# VerseCanvas Environment Configuration
PROJECT_ID=your-google-cloud-project-id
LOCATION=us-central1

# Note: Replace 'your-google-cloud-project-id' with your actual Google Cloud project ID
# You can find this in the Google Cloud Console
"""
        
        env_file.write_text(sample_content)
        print("✅ Created .env file template")
        print("   Please edit .env with your actual project ID")
    else:
        print("✅ .env file already exists")

def run_streamlit_check():
    """Check if Streamlit can run."""
    print("\n🔍 Testing Streamlit...")
    
    try:
        import streamlit
        print("✅ Streamlit can be imported")
        print(f"   Version: {streamlit.__version__}")
        
        print("\n🚀 To start the app, run:")
        print("   streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit error: {str(e)}")
        return False

def main():
    """Run all setup checks."""
    print("🎨 VerseCanvas Setup Check")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    checks = [
        ("Environment Variables", check_environment),
        ("Python Dependencies", check_dependencies),
        ("Google Cloud Auth", check_gcloud_auth),
        ("Poem Analyzer", test_poem_analyzer),
        ("Image Editor", test_image_editor),
        ("Streamlit", run_streamlit_check),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} check failed: {str(e)}")
            results[check_name] = False
    
    # Test image generator separately (might fail due to quotas)
    print("\n🔍 Testing image generator (might fail due to API quotas)...")
    try:
        results["Image Generator"] = test_image_generator()
    except Exception as e:
        print(f"⚠️ Image generator test skipped: {str(e)}")
        results["Image Generator"] = None
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Setup Check Summary:")
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for check_name, result in results.items():
        if result is True:
            print(f"   ✅ {check_name}")
        elif result is False:
            print(f"   ❌ {check_name}")
        else:
            print(f"   ⚠️ {check_name} (skipped)")
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All checks passed! You're ready to run VerseCanvas!")
        print("\nTo start the application:")
        print("   streamlit run app.py")
    else:
        print("\n🔧 Please fix the failed checks before running the application.")
        
        if not os.getenv('PROJECT_ID'):
            create_sample_env()

if __name__ == "__main__":
    main()