from PIL import Image, ImageDraw

# Create a new image with a white background
size = (256, 256)
image = Image.new('RGBA', size, (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# Draw a simple SD logo
margin = 20
draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], 
             fill=(70, 130, 180, 255))
draw.ellipse([margin+30, margin+30, size[0]-margin-30, size[1]-margin-30], 
             fill=(135, 206, 235, 255))

# Save as ICO
image.save('../webui.ico', format='ICO', sizes=[(256, 256)])
