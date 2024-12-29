from PIL import ImageDraw, Image

img = Image.new('RGB', (1000, 1000), 'pink')
draw = ImageDraw.Draw(img)

draw.rectangle([000, 100, 300, 300], fill='green')

img.save('rectangle.png')

frames = []

# Create frames with rectangles of different colors
colors = ['red', 'blue', 'yellow', 'purple', 'orange']
for color in colors:
    frame = Image.new('RGB', (1000, 1000), 'pink')
    draw = ImageDraw.Draw(frame)
    draw.rectangle([0, 100, 300, 300], fill=color)
    frames.append(frame)

# Save frames as a GIF
frames[0].save('rectangle.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)
