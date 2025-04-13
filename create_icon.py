"""
Script to generate a simple application icon for Whisper Transcribe.
This creates a blue circle with a white "W" in the center.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_app_icon():
    """Generate a simple icon for the application."""
    try:
        # Create directory if it doesn't exist
        os.makedirs("resources/icons", exist_ok=True)
        
        # Set up icon parameters
        icon_size = 256
        background_color = (74, 134, 232)  # Blue color
        text_color = (255, 255, 255)  # White color
        
        # Create a new image with a blue background
        icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Calculate circle dimensions to center it
        padding = 10  # Add some padding from the edges
        circle_size = icon_size - (2 * padding)
        circle_pos = (padding, padding)
        circle_end = (padding + circle_size, padding + circle_size)
        
        # Draw a filled circle
        draw.ellipse([circle_pos, circle_end], fill=background_color)
        
        # Add the letter "W" in the center
        # Try to use a built-in font or fall back to default
        try:
            # Try to use a common font available on most systems
            if os.name == 'nt':  # Windows
                font = ImageFont.truetype("arial.ttf", int(circle_size * 0.6))
            else:  # macOS/Linux
                font = ImageFont.truetype("Arial.ttf", int(circle_size * 0.6))
        except IOError:
            # Fall back to default font
            font = ImageFont.load_default()
        
        # Get text size to center it properly
        text = "W"
        try:
            # For newer Pillow versions
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # For older Pillow versions
            text_width, text_height = draw.textsize(text, font=font)
        
        # Calculate text position to center it within the circle
        text_x = padding + (circle_size - text_width) // 2
        text_y = padding + (circle_size - text_height) // 2
        
        # Draw the text centered
        draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        # Save icons in different formats
        icon_path = "resources/icons/app_icon.png"
        icon.save(icon_path)
        print(f"Icon saved to {icon_path}")
        
        # Convert to ICO format for Windows
        icon_path_ico = "resources/icons/app_icon.ico"
        icon.save(icon_path_ico, format="ICO")
        print(f"Icon saved to {icon_path_ico}")
        
        return True
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    print("Creating application icon...")
    success = create_app_icon()
    if success:
        print("Icon creation completed successfully!")
    else:
        print("Failed to create icon.")