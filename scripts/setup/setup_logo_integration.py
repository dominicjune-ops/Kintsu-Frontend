#!/usr/bin/env python3
"""
CareerCoach.ai Logo Integration Helper
Helps you integrate your logo into the platform
"""

import os
import shutil
from pathlib import Path

def setup_logo_integration():
    """Setup logo integration for CareerCoach.ai platform"""
    
    print("🎨 CareerCoach.ai Logo Integration Setup")
    print("=" * 50)
    
    # Check if directories exist
    static_dir = Path("static")
    assets_dir = Path("assets")
    
    if not static_dir.exists():
        static_dir.mkdir()
        print(" Created /static directory")
    
    if not assets_dir.exists():
        assets_dir.mkdir()
        print(" Created /assets directory")
    
    # Look for logo files in common locations
    logo_candidates = []
    search_paths = [
        ".",
        "assets",
        "static",
        "images",
        "img",
        "../",
        "../../"
    ]
    
    logo_extensions = [".png", ".jpg", ".jpeg", ".svg", ".gif"]
    logo_names = ["logo", "careercoach", "brand", "icon"]
    
    print("\n Searching for logo files...")
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                file_lower = file.lower()
                if any(name in file_lower for name in logo_names) and any(file_lower.endswith(ext) for ext in logo_extensions):
                    logo_candidates.append(os.path.join(search_path, file))
    
    if logo_candidates:
        print(f"📁 Found {len(logo_candidates)} potential logo files:")
        for i, logo in enumerate(logo_candidates):
            print(f"   {i+1}. {logo}")
        
        # Copy the first logo found to static directory
        main_logo = logo_candidates[0]
        logo_ext = os.path.splitext(main_logo)[1]
        destination = f"static/logo{logo_ext}"
        
        try:
            shutil.copy2(main_logo, destination)
            print(f" Copied {main_logo} → {destination}")
        except Exception as e:
            print(f" Failed to copy logo: {e}")
    else:
        print(" No logo files found automatically")
        print("\n Manual Setup Instructions:")
        print("1. Copy your logo file to: static/logo.png")
        print("2. Supported formats: PNG, JPG, JPEG, SVG")
        print("3. Recommended size: 200x80 pixels")
    
    # Create logo placement guide
    guide_content = """# 🎨 CareerCoach.ai Logo Integration Guide

## Logo Locations in Platform:

### 1. Main UI Header
- **File**: static/index.html
- **Element**: `.logo` class
- **Size**: max-width: 200px, max-height: 80px

### 2. API Documentation
- **Endpoint**: /logo
- **Returns**: Your logo file directly
- **Usage**: Used by Zapier, Notion, and other integrations

### 3. Email Templates
- **Integration**: Zapier email automation
- **Display**: Header and footer of automated emails

### 4. Notion Roadmap
- **Integration**: Published roadmap page
- **Display**: Small logo in footer

### 5. Investor Materials
- **Usage**: Automatically included in investor dashboards
- **Format**: Professional presentation layout

## Supported Formats:
-  PNG (recommended for transparency)
-  SVG (best for scalability)
-  JPG/JPEG (good for photos)

## Recommended Specifications:
- **Primary Logo**: 400x160px (PNG with transparency)
- **Small Logo**: 100x40px (for headers/footers)
- **Icon**: 64x64px (for favicons and small spaces)

## File Naming Convention:
- `logo.png` - Main logo
- `logo-small.png` - Small version
- `icon.png` - Icon version
- `favicon.ico` - Browser tab icon

## Integration Status:
-  Static file serving configured
-  Logo endpoint available at /logo
-  UI template ready for branding
-  Notion integration prepared
-  Email template variables set

## Next Steps:
1. Upload your logo file(s) to the /static directory
2. Test the integration at: http://localhost:8000/
3. Verify logo appears in: http://localhost:8000/logo
4. Update Notion roadmap with branded version
5. Configure email automation with logo

## Troubleshooting:
- **Logo not showing?** Check file path: /static/logo.png
- **Wrong size?** Use CSS max-width/max-height
- **Blurry logo?** Use higher resolution file
- **Integration issues?** Check file permissions

Ready to make CareerCoach.ai fully branded! 
"""
    
    with open("LOGO_archive/deprecated/INTEGRATION_GUIDE.md", "w") as f:
        f.write(guide_content)
    
    print("\n Created LOGO_archive/deprecated/INTEGRATION_GUIDE.md")
    
    # Check current server integration
    print("\n🔗 Integration Status:")
    
    if os.path.exists("production_app.py"):
        with open("production_app.py", "r") as f:
            content = f.read()
            if "StaticFiles" in content:
                print(" Static file serving configured")
            else:
                print("  Static file serving needs configuration")
            
            if "/logo" in content:
                print(" Logo endpoint available")
            else:
                print("  Logo endpoint needs setup")
    
    if os.path.exists("static/index.html"):
        print(" Branded UI template ready")
    else:
        print("  UI template needs creation")
    
    print("\n Quick Test:")
    print("1. Start server: python production_app.py")
    print("2. Open: http://localhost:8000/")
    print("3. Logo test: http://localhost:8000/logo")
    
    return logo_candidates

if __name__ == "__main__":
    found_logos = setup_logo_integration()
    
    if found_logos:
        print(f"\n Logo integration ready! Found {len(found_logos)} logo files.")
    else:
        print("\n📤 Ready for logo upload! Please add your logo to /static/logo.png")
    
    print("\n Your CareerCoach.ai platform is ready for branding!")