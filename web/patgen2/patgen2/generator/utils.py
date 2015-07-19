from PIL import Image, ImageDraw, ImageFont
from scipy.cluster.vq import kmeans2, vq, whiten, kmeans
from numpy import array
import argparse
from io import StringIO
from operator import itemgetter

class PatternMaker():

    img = None
    pat = None
    args = None
    blocks = []
    palette = None
    w = 0
    h = 0

    def saveImage(self, filename):
        if self.pat is not None:
            filename = filename.replace("jpeg", "png")
            self.pat.save(filename)

    def setArgs(self, shapes='squares', colours=20, size=20):
        self.args = {}
        self.args['shapes'] = shapes
        self.args['colours'] = colours
        self.args['size'] = size

    def parseArgs(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('--squares', dest='squares', action='store_true')
        parser.add_argument('--triangles', dest='triangles', action='store_true')
        parser.add_argument('images', nargs='*', help='Images to process')

        parser.set_defaults(triangles=False, squares=False)

        if args is not None:
            self.args = parser.parse_args(args)
        else:
            self.args = parser.parse_args()

        return self.args.images

    def drawAxes(self):
        pass

    def drawGrid(self):
        for x in range(0, self.w-15, 20):
            self.pat.paste((255, 255, 255), (x, 0, x+1, self.h))

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

        self.pat = Image.new("RGB", (int(self.w/20)*20, int(self.h/20)*20))

        dpat = ImageDraw.Draw(self.pat)

        block_num = 0
        for x in range(0, self.w-20, 20):
            for y in range(0, self.h-20, 20):

                if self.args.triangles is True:
#                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                       dpat.polygon([(x, y), (x+20, y), (x, y+20)], fill=tuple([int(x) for x in self.palette[self.qblocks[block_num]]]))
                    else:
                       dpat.polygon([(x, y), (x+20, y), (x, y+20)], fill=tuple([int(x) for x in self.blocks[block_num]]))
                    block_num += 1
#                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                        dpat.polygon([(x, y+20), (x+20, y+20), (x+20, y)], fill=tuple([int(x) for x in self.palette[self.qblocks[block_num]]]))
                    else:
                        dpat.polygon([(x, y+20), (x+20, y+20), (x+20, y)], fill=tuple([int(x) for x in self.blocks[block_num]]))

                if self.args.squares is True:
                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                        self.pat.paste(tuple([int(x) for x in self.palette[self.qblocks[block_num]]]), box=(x, y, x+20, y+20))
                    else:
                        self.pat.paste(tuple([int(x) for x in self.blocks[block_num]]), box=(x, y, x+20, y+20))

# Check if upper/lower are the same after drawing for lettering

                block_num += 1

    def reducePalette(self, size=8):
        self.palette, self.qblocks = kmeans2(array(self.blocks), size, minit="random")
#        self.qblocks, distortion = vq(array(self.blocks), self.palette)
        print("Reduced palette to: ", self.palette)
#        print("Palette Distortion : ", distortion)

    def scanImage(self, img_filename=None, img_buffer=None):
        palette = []

        if img_buffer is not None:
            self.image = Image.open(StringIO(img_buffer))
        else:
            self.image = Image.open(img_filename)

        self.image = self.image.convert('RGBA')

        self.w, self.h = self.image.size
#        print("Width: %d Height: %d" % (w, h))

        self.pixels = self.image.load()

        self.pat = Image.new("RGB", (int(self.w/20)*20, int(self.h/20)*20), "white")

        for x in range(0, self.w-20, 20):
            for y in range(0, self.h-20, 20):
                print("X: %d Y: %d" % (x, y))

#        subim = im_rgb.crop((x, y, 20, 20))

                r = g = b = count = 0
                avg_r = avg_g = avg_b = 0
                right_r = right_g = right_b = 0
                left_r = left_g = left_b = 0
                right_avg_r = right_avg_g = right_avg_b = 0
                left_avg_r = left_avg_g = left_avg_b = 0

                tri_line = 20
                for y_p in range(y, y+20, 1):
                    tri_pos = 0
# print("R:%d G:%d B:%d" % pixel)
                    for x_p in range(x, x+20, 1):
                        if self.args.triangles is True:
                            if tri_pos >= tri_line:
                                right_r += self.pixels[x_p, y_p][0]
                                right_g += self.pixels[x_p, y_p][1]
                                right_b += self.pixels[x_p, y_p][2]
                            else:
                                left_r += self.pixels[x_p, y_p][0]
                                left_g += self.pixels[x_p, y_p][1]
                                left_b += self.pixels[x_p, y_p][2]

                            tri_pos += 1

                        if self.args.squares is True:
                            r += self.pixels[x_p, y_p][0]
                            g += self.pixels[x_p, y_p][1]
                            b += self.pixels[x_p, y_p][2]

                        count += 1

                    tri_line -= 1

                if self.args.squares is True:
                    if r > 0:
                        avg_r = r/count
                    if g > 0:
                        avg_g = g/count
                    if b > 0:
                        avg_b = b/count

                    self.blocks.append([avg_r, avg_g, avg_b])

                if self.args.triangles is True:

                    tri_count = count / 2
                    if left_r > 0:
                        left_avg_r = left_r/tri_count
                    if left_g > 0:
                        left_avg_g = left_g/tri_count
                    if left_b > 0:
                        left_avg_b = left_b/tri_count

                    self.blocks.append([left_avg_r, left_avg_g, left_avg_b])

                    if right_r > 0:
                        right_avg_r = right_r/tri_count
                    if right_g > 0:
                        right_avg_g = right_g/tri_count
                    if right_b > 0:
                        right_avg_b = right_b/tri_count

                    self.blocks.append([right_avg_r, right_avg_g, right_avg_b])

def handle_uploaded_file(f, shapes):

    pg = PatternMaker()
    if shapes == 'squares':
        pg.parseArgs(['--squares'])
    else:
        pg.parseArgs(['--triangles'])

    pg.scanImage(img_filename=f)

    pg.drawPattern()
    pg.drawGrid()

    return pg.pat


if __name__ == "__main__":

    pg = PatternMaker()
    filenames = pg.parseArgs()

    for img_filename in filenames:
        pg.scanImage(img_filename)

#        print(pg.blocks)

        pg.drawPattern()
        pg.drawGrid()
        pg.saveImage("triangles-" + img_filename)

        pg.reducePalette()
        pg.drawPattern()

#    pg.drawGrid()
#    pg.drawLetters()
#    pg.drawAxes()

        pg.drawGrid()
        pg.saveImage("reduced-" + img_filename)

# Save image


