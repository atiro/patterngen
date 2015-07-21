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
    qblocks = []
    palette = None
    w = 0
    h = 0

    def reset(self):

        self.blocks = []
        self.qblocks = []
        self.palette = None
        self.w = self.h = 0

    def saveImage(self, filename):
        if self.pat is not None:
            filename = filename.replace("jpeg", "png")
            self.pat.save(filename)

    def setArgs(self, shapes='squares', colours=20, size=20):

        self.args = {}

        if shapes == 'squares':
            self.args['squares'] = 1
        else:
            self.args['triangles'] = 1

        self.args['colours'] = colours
        self.args['size'] = size

    def parseArgs(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('--squares', dest='squares', action='store_true')
        parser.add_argument('--triangles', dest='triangles', action='store_true')
        parser.add_argument('images', nargs='*', help='Images to process')

        parser.set_defaults(triangles=False, squares=False)

        if args is not None:
            pargs = parser.parse_args(args)
        else:
            pargs = parser.parse_args()

        self.args = vars(pargs)

        return self.args['images']

    def drawAxes(self):
        pass

    def drawGrid(self):

        block_size = self.args['size']

        for x in range(0, self.w, block_size):
            self.pat.paste((255, 255, 255), (x, 0, x+1, self.h))

        for y in range(0, self.h, block_size):
            self.pat.paste((255, 255, 255), (0, y, self.w, y+1))

    def drawLetters(self):
#        pixels = im.load()

        rgb_used = {}
        rgb_count = 0
        rgb_counts = {}

        font = ImageFont.truetype("LiberationMono-Regular.ttf")

        d_rgb = ImageDraw.Draw(pat)

        if 'squares' in self.args:
            rgb = '#%02x%02x%02x' % (avg_r, avg_g, avg_b)
            if rgb not in rgb_used:
                rgb_used[rgb] = rgb_count
                rgb_counts[rgb] = 1
                self.pat.paste((avg_r, avg_g, avg_b), (x, y, x+block_size, y+block_size))
                d_rgb.text((x+8, y+8), chr(ord("A")+rgb_count), font=font)
                rgb_count += 1
            else:
                rgb_counts[rgb] += 1


    def drawPattern(self):

# loop through orig_image, drawing into new image with reduced pallete

        block_size = self.args['size']

        self.pat = Image.new("RGB", (int(self.w/block_size)*block_size, int(self.h/block_size)*block_size))

        dpat = ImageDraw.Draw(self.pat)

        block_num = 0
        for x in range(0, self.w - block_size, block_size):
            for y in range(0, self.h - block_size, block_size):

                if 'triangles' in self.args:
#                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                       dpat.polygon([(x, y), (x+block_size, y), (x, y+block_size)], fill=tuple([int(x) for x in self.palette[self.qblocks[block_num]]]))
                    else:
                       dpat.polygon([(x, y), (x+block_size, y), (x, y+block_size)], fill=tuple([int(x) for x in self.blocks[block_num]]))
                    block_num += 1
#                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                        dpat.polygon([(x, y+block_size), (x+block_size, y+block_size), (x+block_size, y)], fill=tuple([int(x) for x in self.palette[self.qblocks[block_num]]]))
                    else:
                        dpat.polygon([(x, y+block_size), (x+block_size, y+block_size), (x+block_size, y)], fill=tuple([int(x) for x in self.blocks[block_num]]))

                if 'squares' in self.args:
#                    print("Block Colour: ", self.palette[self.qblocks[block_num]])
                    if self.palette is not None:
                        self.pat.paste(tuple([int(x) for x in self.palette[self.qblocks[block_num]]]), box=(x, y, x+block_size, y+block_size))
                    else:
                        self.pat.paste(tuple([int(x) for x in self.blocks[block_num]]), box=(x, y, x+block_size, y+block_size))

# Check if upper/lower are the same after drawing for lettering

                block_num += 1

    def reducePalette(self):
        self.palette, self.qblocks = kmeans2(array(self.blocks), self.args['colours'], minit="random")
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

        block_size = self.args['size']

        self.pat = Image.new("RGB", (int(self.w/block_size)*block_size, int(self.h/block_size)*block_size), "white")

        # Arrg - not being cleared between requests for some reason. 
        self.blocks = []

        for x in range(0, self.w - block_size, block_size):
            for y in range(0, self.h - block_size, block_size):
#                print("X: %d Y: %d" % (x, y))

#        subim = im_rgb.crop((x, y, 20, 20))

                r = g = b = count = 0
                avg_r = avg_g = avg_b = 0
                right_r = right_g = right_b = 0
                left_r = left_g = left_b = 0
                right_avg_r = right_avg_g = right_avg_b = 0
                left_avg_r = left_avg_g = left_avg_b = 0

                tri_line = block_size
                for y_p in range(y, y + block_size, 1):
                    tri_pos = 0
# print("R:%d G:%d B:%d" % pixel)
                    for x_p in range(x, x + block_size, 1):
                        if 'triangles' in self.args:
                            if tri_pos >= tri_line:
                                right_r += self.pixels[x_p, y_p][0]
                                right_g += self.pixels[x_p, y_p][1]
                                right_b += self.pixels[x_p, y_p][2]
                            else:
                                left_r += self.pixels[x_p, y_p][0]
                                left_g += self.pixels[x_p, y_p][1]
                                left_b += self.pixels[x_p, y_p][2]

                            tri_pos += 1

                        if 'squares' in self.args:
                            r += self.pixels[x_p, y_p][0]
                            g += self.pixels[x_p, y_p][1]
                            b += self.pixels[x_p, y_p][2]

                        count += 1

                    tri_line -= 1

                if 'squares' in self.args:
                    if r > 0:
                        avg_r = r/count
                    if g > 0:
                        avg_g = g/count
                    if b > 0:
                        avg_b = b/count

                    self.blocks.append([avg_r, avg_g, avg_b])

                if 'triangles' in self.args:

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

def handle_uploaded_file(f, shapes, colours, size):

    pg = PatternMaker()

    pg.setArgs(shapes=shapes, colours=int(colours), size=int(size))

    pg.scanImage(img_filename=f)

    pg.reducePalette()

    pg.drawPattern()
    pg.drawGrid()

    pat_img = pg.pat

    pg.reset()

    return pat_img


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


