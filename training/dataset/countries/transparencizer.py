from PIL import Image

img = Image.open("mlt.png").convert("RGBA")
arr = img.getdata()

newArr = []
for r, g, b, _ in arr:
    if r == 255 and b == 255 and g == 255:
        newArr.append((r, g, b, 0))
    else:
        newArr.append((r, g, b, 255))

img.putdata(newArr)
img.save("mlt2.png", "PNG")
