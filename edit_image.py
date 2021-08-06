from PIL import Image, ImageFont, ImageDraw 

def makeimage(author):
    my_image = Image.open("canvas.png")
    title_font = ImageFont.truetype('OpenSans-Bold.ttf', 40)
    title_text = str(author)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((150,-10), title_text, (82, 16, 16), font=title_font)
    my_image.save("result.png")
