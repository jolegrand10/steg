import logging
import sys
from io import BytesIO

import cv2 as cv
import numpy as np

logger = logging.getLogger(__name__)


class Stegano:
    """ encode/decode a byte-msg in/from an image without visible difference"""

    INPICFILES = (('image files', '.jpg .png .bmp'),)
    OUTPICFILES = (('image files', '.jpg .png .bmp'),)
    TXTFILES = (('text files', '*.txt'),)

    def __init__(self):
        """ image is an np.ndarray as used in cv2 """
        self.image = None
        self.data = ""
        self.n = 0
        self.p = 0

    def bs2image(self, bs):
        """ Byte string to image """
        logger.info(f"Read image from bytestring")
        nparr = np.frombuffer(bs, np.uint8)
        self.image = cv.imdecode(nparr, cv.IMREAD_COLOR)
        self.n, self.p, _ = self.image.shape

    def image2bs(self, dot_ext):
        """ image to byte string """
        image_encoded = cv.imencode(dot_ext, self.image)[1]
        nparr = np.array(image_encoded)
        return nparr.tobytes()

    def read_image(self, path):
        logger.info(f"Read image from {path}")
        try:
            self.image = cv.imread(path)
        except Exception as e:
            logger.error(f"Failed to read cv2 image. Reason: {e}")
        if self.image is None:
            raise Exception("Failed to read cv2 image")
        else:
            logger.debug(f"Successfully read image from {path}")
            self.n, self.p, _ = self.image.shape

    def read_data(self, path):
        """ reads a text file as bytes """
        with open(path, "rb") as f:
            self.data = f.read()
        logger.info(f"{len(self.data)} bytes read from {path}")

    def input_data(self):
        """ collect text data as bytes from stdin """
        self.data = sys.stdin.read()
        self.data = bytearray(self.data, 'utf-8')
        logger.info(f"{len(self.data)} bytes read from stdin")

    def write_image(self, path):
        """ save image to file """
        logger.info(f"Write image to {path}")
        cv.imwrite(path, self.image)

    def write_data(self, path):
        """ save text to file """
        with open(path, "wb") as f:
            f.write(self.data)
            logger.info(f"{len(self.data)} bytes written")

    def output_data(self):
        """ send text to stdout """
        sys.stdout.write(self.data)
        logger.info(f"{len(self.data)} bytes written")

    def output_image(self, dot_ext):
        """ send image to stdout """
        # TODO check imencode return code
        sys.stdout.buffer.write(cv.imencode(dot_ext, self.image)[1].tostring())

    def image_buffer(self, dot_ext):
        success, buffer = cv.imencode(dot_ext, self.image)
        if success:
            return BytesIO(buffer.tobytes())
        raise RuntimeError(f"Cannot output image to buffer")

    def encode(self):
        """ message is a byte array """
        #
        # if length of message in bytes exceeds the count of bytes in the image
        # the message is truncated
        #
        maxlen = self.image.size // 8
        message = self.data
        if len(message) >= maxlen:
            message = message[:maxlen - 1]  # - 1 accounts for the termination mark
        #
        # Starting position in the image, where the message will be encoded
        #
        i = 0  # row index
        j = 0  # column index
        k = 0  # color index (or channel index, for R,G or B)
        #
        # message is processed byte by byte
        # a null byte is added as the end of message to mark its end
        #
        for c in message + bytearray((0,)):
            #
            # c is a byte, bs is its representation as a string of 8  1s or 0s
            #
            bs = format(int(c), '08b')
            #
            # for each bit in the current byte - bit string
            #
            for b in bs:
                b = int(b)
                if b:
                    #
                    # to set last bit while preserving the others : or with 1
                    # uint8(1) to make sure the 1 byte ints are used.
                    #
                    self.image[i, j, k] |= np.uint8(1)
                else:
                    #
                    # to clear last bit while preserving the others : and with ~1
                    # ~1 meand -2 and some versions of numpy cause an out of bounds error for
                    # an uint8. To avoid that the and is made with FE instead
                    #
                    self.image[i, j, k] &= 0xFE
                #
                # move  next channel
                #
                k = (k + 1) % 3
                if k == 0:
                    #
                    # move next pixel in the line
                    #
                    j = (j + 1) % self.p
                    if j == 0:
                        #
                        # move  next line
                        #
                        i += 1
        return len(message)

    def decode(self):
        #
        # the message to be recovered from the image
        #
        message = bytearray()
        #
        # bit string - representing a byte
        #
        bs = ""
        #
        # loop on all bytes in the image, collecting 1 bit per byte,
        # assembling bits in bytes, appended one by one to the growing message
        # until a null byte is encountered
        #
        for i in range(self.n):
            for j in range(self.p):
                for k in range(3):
                    #
                    # collect low weight bit
                    #
                    b = self.image[i, j, k] & 1
                    #
                    # catenate to growing bitstring
                    #
                    bs += str(b)
                    #
                    # until a byte is assembled
                    #
                    if len(bs) == 8:
                        #
                        # convert 8 bit string to int
                        #
                        #
                        x = int(bs, 2)
                        if x == 0:
                            #
                            # null byte terminates the message
                            #
                            self.data = message
                            logger.info(f"{len(self.data)} bytes decoded")
                            return
                        else:
                            #
                            # catenate byte to the growing msg
                            #
                            message += bytearray((x,))

                            bs = ""


def test_bs():
    # Load image as string from file/database
    with open('tests/bonjour.jpg', 'rb') as fd:
        img_str = fd.read()
    s = Stegano()
    s.bs2image(img_str)
    s.data = bytearray("Salut", 'utf-8')
    s.encode()
    s.write_image("salut.png")


def main():
    """ a short test"""
    logger.info("Starting interactive test session")
    s = Stegano()
    s.read_image(input("Enter path to image file: "))
    while (op := input("D to decode, E to encode, Q to quit: ")) not in "DEQ":
        pass
    if op == "Q":
        logger.info("Ending interactive test session")
        return
    if op == 'D':
        logger.info("Decoding")
        s.decode()
        print(s.data)
    if op == "E":
        logger.info("Encoding")
        s.read_data(input("Enter path to text file: "))
        s.encode()
        s.write_image(input("Enter path to output image file: "))


if __name__ == '__main__':
    from util.fullog import Full_Log
    Full_Log(name="Stegano")
    main()
