from PIL import Image, ImageDraw, ImageFont
import argparse
from operator import itemgetter

im = Image.open("dog.jpeg")
w, h = im.size
print("Width: %d Height: %d" % (w, h))
pat = Image.new("RGB", (int(w/20)*20, int(h/20)*20), "white")

im_rgb = im.convert('RGBA')

w, h = im.size
print("Width: %d Height: %d" % (w, h))
pixels = im.load()

rgb_used = {}
rgb_count = 0
rgb_counts = {}

font = ImageFont.truetype("LiberationMono-Regular.ttf")

d_rgb = ImageDraw.Draw(pat)

for x in range(0, w-15, 20):
    for y in range(0, h-15, 20):
        print("X: %d Y: %d" % (x, y))

#        subim = im_rgb.crop((x, y, 20, 20))

        r = g = b = count =0
        avg_r = avg_g = avg_b = 0

        for x_p in range(x, x+20, 1):
            for y_p in range(y, y+20, 1):
#print("R:%d G:%d B:%d" % pixel)
                    r += pixels[x_p, y_p][0]
                    g += pixels[x_p, y_p][1]
                    b += pixels[x_p, y_p][2]

                    count += 1

        if r > 0:
            avg_r = int(r/count)
        if g > 0:
            avg_g = int(g/count)
        if b > 0:
            avg_b = int(b/count)

        print("Avg R: %d G: %d B: %d" % (avg_r, avg_g, avg_b))

        pat.paste((avg_r, avg_g, avg_b), (x, y, x+20, y+20))

        rgb = '#%02x%02x%02x' % (avg_r, avg_g, avg_b)

        if rgb not in rgb_used:
            rgb_used[rgb] = rgb_count
            rgb_counts[rgb] = 1
            pat.paste((avg_r, avg_g, avg_b), (x, y, x+20, y+20))
            d_rgb.text((x+8, y+8), chr(ord("A")+rgb_count), font=font)
            rgb_count += 1
        else:
            rgb_counts[rgb] += 1

for x in range(0, w-15, 20):
    pat.paste((255, 255, 255), (x, 0, x+1, h))

for y in range(0, h-15, 20):
    pat.paste((255, 255, 255), (0, y, w, y+1))

pat.save("new_dog.jpg")
