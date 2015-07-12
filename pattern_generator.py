from PIL import Image, ImageDraw, ImageFont
from scipy.cluster.vq import kmeans, vq, whiten
import argparse
from operator import itemgetter

class PatternGenerator():

    img = None
    pat = None
    args = None
    blocks = []
    palette = ()
    w = 0
    h = 0

    def saveImage(self):
        if self.pat is not None:
            self.pat.save("dog-new.jpeg")

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--squares', dest='squares', action='store_true')
        parser.add_argument('--triangles', dest='triangles', action='store_true')
        parser.add_argument('images', nargs='+', help='Images to process')

        parser.set_defaults(triangles=False, squares=False)
        self.args = parser.parse_args()

        return self.args.images

    def drawAxes(self):
        pass

    def drawGrid(self):
        for x in range(0, self.w-15, 20):
#            self.pat.paste((255, 255, 255), (x, 0, x+1, self.h))
            self.pat.paste((0, 0, 0), (x, 0, x+1, self.h))

        for y in range(0, self.h-15, 20):
            self.pat.paste((255, 255, 255), (0, y, self.w, y+1))

    def drawLetters(self):
#        pixels = im.load()

        rgb_used = {}
        rgb_count = 0
        rgb_counts = {}

        font = ImageFont.truetype("LiberationMono-Regular.ttf")

        d_rgb = ImageDraw.Draw(pat)

        if self.args.squares:
            rgb = '#%02x%02x%02x' % (avg_r, avg_g, avg_b)
            if rgb not in rgb_used:
                rgb_used[rgb] = rgb_count
                rgb_counts[rgb] = 1
                self.pat.paste((avg_r, avg_g, avg_b), (x, y, x+20, y+20))
                d_rgb.text((x+8, y+8), chr(ord("A")+rgb_count), font=font)
                rgb_count += 1
            else:
                rgb_counts[rgb] += 1


    def drawPattern(self):

# loop through orig_image, drawing into new image with reduced pallete

        pat = Image.new("P", (int(self.w/20)*20, int(self.h/20)*20))

        pat.putpalette(self.palette * 13)

        dpat = ImageDraw.Draw(pat)

        block_num = 0
        for x in range(0, self.w-15, 20):
            for y in range(0, self.h-15, 20):

                if 'triangle' in self.args:
                    dpat.polygon([(x, y), (x+20, y), (x, y+20)], fill=self.blocks[block_num])
                    block_num += 1
                    dpat.polygon([(x, y+20), (x+20, y+20), (x+20, y)], fill=self.blocks[block_num])

                if 'square' in self.args:
                    dpat.paste((x, y, x+20, y+20), self.blocks[block_num])

# Check if upper/lower are the same after drawing for lettering

                block_num += 1

    def reducePalette(self, size=20):
        whitened = whiten(self.blocks)
        self.palette, distortion = kmeans(whitened, size)
        print("Reduced palette to: ", self.palette)

    def scanImage(self, img_filename):
        palette = []

        self.image = Image.open(img_filename)
        self.image = self.image.convert('RGBA')

        self.w, self.h = self.image.size
#        print("Width: %d Height: %d" % (w, h))

        self.pixels = self.image.load()

        self.pat = Image.new("RGB", (int(self.w/20)*20, int(self.h/20)*20), "white")

        for x in range(0, self.w-15, 20):
            for y in range(0, self.h-15, 20):
                print("X: %d Y: %d" % (x, y))

#        subim = im_rgb.crop((x, y, 20, 20))

                r = g = b = count = 0
                avg_r = avg_g = avg_b = 0
                right_r = right_g = right_b = 0
                left_r = left_g = left_b = 0
                right_avg_r = right_avg_g = right_avg_b = 0
                left_avg_r = left_avg_g = left_avg_b = 0

                tri_line = 20
                for x_p in range(x, x+20, 1):
                    tri_pos = 0
# print("R:%d G:%d B:%d" % pixel)
                    for y_p in range(y, y+20, 1):
                        if self.args.triangles:
                            if tri_pos > tri_line:
                                right_r += self.pixels[x_p, y_p][0]
                                right_g += self.pixels[x_p, y_p][1]
                                right_b += self.pixels[x_p, y_p][2]
                            else:
                                left_r += self.pixels[x_p, y_p][0]
                                left_g += self.pixels[x_p, y_p][1]
                                left_b += self.pixels[x_p, y_p][2]

                            tri_pos += 1

                        if self.args.squares:
                            r += self.pixels[x_p, y_p][0]
                            g += self.pixels[x_p, y_p][1]
                            b += self.pixels[x_p, y_p][2]

                        count += 1

                tri_line -= 1

                if 'squares' in self.args:
                    if r > 0:
                        avg_r = int(r/count)
                    if g > 0:
                        avg_g = int(g/count)
                    if b > 0:
                        avg_b = int(b/count)

                    self.blocks.append([avg_r, avg_g, avg_b])

                if 'triangles' in self.args:

                    tri_count = count / 2
                    if left_r > 0:
                        left_avg_r = int(left_r/tri_count)
                    if left_g > 0:
                        left_avg_g = int(left_g/tri_count)
                    if left_b > 0:
                        left_avg_b = int(left_b/tri_count)

                    self.blocks.append([left_avg_r, left_avg_g, left_avg_b])

                    if right_r > 0:
                        right_avg_r = int(right_r/tri_count)
                    if right_g > 0:
                        right_avg_g = int(right_g/tri_count)
                    if right_b > 0:
                        right_avg_b = int(right_b/tri_count)

                    self.blocks.append([right_avg_r, right_avg_g, right_avg_b])


if __name__ == "__main__":

    pg = PatternGenerator()
    filenames = pg.parseArgs()

    for img_filename in filenames:
        pg.scanImage(img_filename)
        pg.reducePalette()
        pg.drawPattern()

#    pg.drawGrid()
#    pg.drawLetters()
#    pg.drawAxes()

        pg.drawGrid()
        pg.saveImage()

# Save image

