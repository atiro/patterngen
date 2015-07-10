from PIL import Image, ImageDraw, ImageFont
import argparse
from operator import itemgetter

parser = argparse.ArgumentParser()
parser.add_argument('--squares', dest='squares', action='store_true')
parser.add_argument('--triangles', dest='triangles', action='store_true')
parser.set_defaults(triangles=False, squares=False)
args = parser.parse_args()

def reducePalette(size = 20):


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

        r = g = b = count = 0
        avg_r = avg_g = avg_b = 0
        right_r = right_g = right_b = 0
        left_r = left_g = left_b = 0

        tri_line = 20
        for x_p in range(x, x+20, 1):
            tri_pos = 0
            for y_p in range(y, y+20, 1):
# print("R:%d G:%d B:%d" % pixel)
                    if args.triangles:
                        if tri_pos > tri_line:
                            right_r += pixels[x_p, y_p][0]
                            right_g += pixels[x_p, y_p][1]
                            right_b += pixels[x_p, y_p][2]
                        else:
                            left_r += pixels[x_p, y_p][0]
                            left_g += pixels[x_p, y_p][1]
                            left_b += pixels[x_p, y_p][2]

                        tri_pos += 1

                    if args.squares:
                        r += pixels[x_p, y_p][0]
                        g += pixels[x_p, y_p][1]
                        b += pixels[x_p, y_p][2]

                    count += 1

            tri_line -= 1

        if args.squares:
            if r > 0:
                avg_r = int(r/count)
            if g > 0:
                avg_g = int(g/count)
            if b > 0:
                avg_b = int(b/count)

            print("Avg R: %d G: %d B: %d" % (avg_r, avg_g, avg_b))

            pat.paste((avg_r, avg_g, avg_b), (x, y, x+20, y+20))

        if args.triangles:
            if left_r > 0:
                left_avg_r = int(left_r/count)
            if left_g > 0:
                left_avg_g = int(left_g/count)
            if left_b > 0:
                left_avg_b = int(left_b/count)

            d_rgb.polygon([(x, y), (x+20, y), (x, y+20)], fill=(left_avg_r, left_avg_g, left_avg_b))

            print("Left Avg R: %d G: %d B: %d" % (left_avg_r, left_avg_g, left_avg_b))
            if right_r > 0:
                right_avg_r = int(right_r/count)
            if right_g > 0:
                right_avg_g = int(right_g/count)
            if right_b > 0:
                right_avg_b = int(right_b/count)

            if ((left_avg_r == right_avg_r) and
                (left_avg_g == right_avg_g) and 
                (left_avg_b == right_avg_b)):

                pat.paste((avg_r, avg_g, avg_b), (x, y, x+20, y+20))
            else:
                d_rgb.polygon([(x, y), (x+20, y), (x, y+20)], fill=(left_avg_r, left_avg_g, left_avg_b))
                d_rgb.polygon([(x, y+20), (x+20, y+20), (x+20, y)], fill=(right_avg_r, right_avg_g, right_avg_b))
                print("Right Avg R: %d G: %d B: %d" % (right_avg_r, right_avg_g, right_avg_b))

        if args.squares:

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
