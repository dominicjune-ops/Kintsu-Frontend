"""
Create a CareerCoach.ai logo placeholder using Python PIL
This creates a professional-looking logo placeholder that you can replace with your actual logo
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_careercoach_logo():
    """Create a professional CareerCoach.ai logo placeholder"""
    
    # Create image with professional colors
    width, height = 400, 120
    background_color = (15, 23, 42)  # Dark blue-gray
    text_color = (59, 130, 246)     # Blue
    accent_color = (34, 197, 94)    # Green for ".ai"
    
    # Create image
    img = Image.new('RGBA', (width, height), background_color + (255,))
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        # Try to load a professional font
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except:
        try:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        except:
            font_large = None
            font_small = None
    
    # Draw "CareerCoach" in blue
    career_text = "CareerCoach"
    ai_text = ".ai"
    
    # Calculate text positioning
    if font_large:
        career_bbox = draw.textbbox((0, 0), career_text, font=font_large)
        ai_bbox = draw.textbbox((0, 0), ai_text, font=font_small)
        
        career_width = career_bbox[2] - career_bbox[0]
        ai_width = ai_bbox[2] - ai_bbox[0]
        total_width = career_width + ai_width
        
        start_x = (width - total_width) // 2
        text_y = (height - career_bbox[3]) // 2
        
        # Draw "CareerCoach" in blue
        draw.text((start_x, text_y), career_text, fill=text_color, font=font_large)
        
        # Draw ".ai" in green
        draw.text((start_x + career_width, text_y + 8), ai_text, fill=accent_color, font=font_small)
    else:
        # Fallback for systems without font support
        draw.text((50, 45), "CareerCoach.ai", fill=text_color)
    
    # Add a subtle border
    draw.rectangle([2, 2, width-3, height-3], outline=text_color, width=2)
    
    # Save the logo
    static_path = "static/logo.png"
    assets_path = "assets/logo.png"
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    os.makedirs(os.path.dirname(assets_path), exist_ok=True)
    
    # Save to both locations
    img.save(static_path, "PNG")
    img.save(assets_path, "PNG")
    
    print(f" Logo placeholder created successfully!")
    print(f"📁 Saved to: {static_path}")
    print(f"📁 Saved to: {assets_path}")
    print(f"🎨 Size: {width}x{height} pixels")
    print(f"💡 Replace these files with your actual CareerCoach.ai logo")
    
    return static_path

if __name__ == "__main__":
    try:
        create_careercoach_logo()
    except ImportError:
        print(" PIL (Pillow) not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "Pillow"])
        print(" Pillow installed. Please run the script again.")
    except Exception as e:
        print(f" Error creating logo: {e}")
        print("💡 You can manually save your logo as 'static/logo.png' or 'assets/logo.png'")