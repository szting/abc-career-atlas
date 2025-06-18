"""
Icon Generator for PWA
Creates placeholder icons for the Career Atlas PWA
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the Career Atlas compass emoji"""
    # Create a new image with a blue gradient background
    img = Image.new('RGB', (size, size), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    
    # Add a lighter blue circle in the center
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#3b82f6')
    
    # Add compass emoji or text
    try:
        # Try to use a large font
        font_size = size // 3
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw compass symbol (using text as fallback)
    text = "🧭"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw white text
    draw.text((x, y), text, fill='white', font=font)
    
    # Add "CA" text below for smaller icons
    if size >= 192:
        ca_font_size = size // 8
        try:
            ca_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", ca_font_size)
        except:
            ca_font = font
        
        ca_text = "Career Atlas"
        ca_bbox = draw.textbbox((0, 0), ca_text, font=ca_font)
        ca_width = ca_bbox[2] - ca_bbox[0]
        ca_x = (size - ca_width) // 2
        ca_y = size - margin - ca_font_size
        
        draw.text((ca_x, ca_y), ca_text, fill='white', font=ca_font)
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created {filename}")

# Create icons
if not os.path.exists('static'):
    os.makedirs('static')

# Generate different sized icons
create_icon(192, 'static/icon-192.png')
create_icon(512, 'static/icon-512.png')
create_icon(96, 'static/icon-96.png')

# Create a simple screenshot placeholder
screenshot = Image.new('RGB', (1280, 720), color='#f3f4f6')
draw = ImageDraw.Draw(screenshot)

# Add some text to the screenshot
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

draw.text((640, 300), "Career Atlas", fill='#1e3a8a', font=title_font, anchor="mm")
draw.text((640, 380), "AI-Powered Career Guidance Platform", fill='#6b7280', font=subtitle_font, anchor="mm")

screenshot.save('static/screenshot-1.png', 'PNG')
print("Created screenshot-1.png")

print("\nIcon generation complete!")
print("Note: These are placeholder icons. For production, create proper branded icons.")
