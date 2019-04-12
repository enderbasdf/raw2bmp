''' write by kim kyung hun'''

from struct import pack

size = 512
''' raw to bitmap file class'''
class Bitmap():

    def __init__(s, width, height):
        s._bfType = 19778  # Bitmap signature
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26 + s._bcWidth * 3 * s._bcHeight
        s.clear()

    def clear(s):
        s._graphics = [(0, 0, 0)] * s._bcWidth * s._bcHeight

    def setPixel(s, x, y, color):
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > s._bcWidth - 1 or y > s._bcHeight - 1:
                raise ValueError('Coords out of range')
            # if len(color) != 3:
            #   raise ValueError('Color must be a tuple of 3 elems')
            s._graphics[y * s._bcWidth + x] = color
        # s._graphics[y * s._bcWidth + x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elems')

    def write(s, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         s._bfType,
                         s._bfSize,
                         s._bfReserved1,
                         s._bfReserved2,
                         s._bfOffBits))  # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                         s._bcSize,
                         s._bcWidth,
                         s._bcHeight,
                         s._bcPlanes,
                         s._bcBitCount))  # Writing BITMAPINFO

            '''write raw data'''
            img = raw('raw.raw', size)
            for i in range(size):
                for j in range(size):
                    f.write(pack('<BBB', *img[i][j]))


'''create raw file'''
def raw(file, size):
    img = [[(0, 0, 0)] * size for i in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            if i < 100:
                temp = 120
                img[i][j] = (temp, temp, temp)
            elif i < 200:
                temp = round(0.15 * i + 105)
                img[i][j] = (temp, temp, temp)
            elif i < 280:
                temp = round(9 / 8 * i) - 90
                img[i][j] = (temp, temp, temp)
            elif i < 300:
                temp = round(3 / 4 * i + 15)
                img[i][j] = (temp, temp, temp)
            else:
                temp = 240
                img[i][j] = (temp, temp, temp)
    with open(file, 'wb') as f:
        for i in range(size):
            for j in range(size):
                f.write(pack('<BBB', *img[i][j]))
    return img

''' rotate image'''
def rotate():
    import cv2 as cv
    import numpy as np

    img = cv.imread('raw2bmp.bmp', 0)
    h, w = img.shape

    h = h - 1
    w = w - 1

    new_img = np.zeros([h, w, 3], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            new_img[i, j] = img[j, i] #rotate right 90 : img[h-j][w-i]
            new_img = new_img[0:h, 0:w]

    cv.imwrite("rotate_left.bmp", new_img)
def main():
    # just create raw file
    raw('raw.raw',size)

    # raw to bmp
    b = Bitmap(size, size)
    b.write('raw2bmp.bmp')

    # ratate bmp file default left 90 rotation
    rotate()


if __name__ == '__main__':
    main()