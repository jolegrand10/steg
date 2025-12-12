import argparse
import os.path
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from stegano import Stegano
from util.fullog import Full_Log


DEBUG = False

logger = logging.getLogger(__name__)

class Csteg:
    """ a command to run Steganography from the CLI"""

    def __init__(self, p):
        """ p is the parser, provided at init time to facilitate unit testing"""
        self.parser = p
        self.setup_parser()
        self.stegano = Stegano()
        self.verbose = False
        self.infile = sys.stdin
        self.outfile = sys.stdout
        self.picfile = 'NoName.jpg'
        self.action = 'encode'
        self.debug = DEBUG

    def is_valid_pic(self, arg):
        if not os.path.isfile(arg):
            self.parser.error(f'Picture file {arg} does not exist')
        else:
            return arg

    def is_valid_action(self, arg):
        if type(arg) is not str:
            self.parser.error(f"Action should be a string")
        else:
            arg = arg.lower()
            if arg not in {'encode', 'decode'}:
                self.parser.error(f"Action should be encode or decode")
            else:
                return arg

    def setup_parser(self):
        """ add args to parser p"""
        self.parser.add_argument('-a', '--action', help='Specify encode or decode',
                                 type=lambda x: self.is_valid_action(x))
        self.parser.add_argument('--pic', dest='picfile', required=True,
                                 help='Path to the picture file', metavar='PIC',
                                 type=lambda x: self.is_valid_pic(x))
        self.parser.add_argument('-o', '--output', dest='outfile',
                                 help='Output file. Pic or text, depending on action. Default is stdout.',
                                 default=sys.stdout)
        self.parser.add_argument('-i', '--input', dest='infile',
                                 help='Input file. Text. Default is stdin.',
                                 default=sys.stdin)
        self.parser.add_argument('-v', '--verbose', help='Show details',
                                 action='store_true', default=False)
        self.parser.description = """ Two way steganography.
    
            'encode' merges a text in a picture.
    
            'decode' retrieves the text from a picture. """

    def parse(self, args=None):
        pa = self.parser.parse_args(args)
        self.verbose = pa.verbose
        self.infile = pa.infile
        self.outfile = pa.outfile
        self.picfile = pa.picfile
        self.action = pa.action
        self.debug = DEBUG
        if DEBUG:
            #
            # check parsed args
            #
            for k in dir(pa):
                if not k.startswith('_'):
                    logger.debug(f"  {k}: {eval('pa.' + k)}")

    def run(self):
        try:
            self.stegano.read_image(self.picfile)
        except Exception as e:
            logger.error(f"Cannot read image at {self.infile}. Reason: {e}")
        else:
            if self.action == 'encode':
                self.encode()
            else:
                self.decode()

    def encode(self):
        try:
            logger.debug("Collecting input")
            if self.infile == sys.stdin:
                self.stegano.input_data()
            else:
                self.stegano.read_data(self.infile)
            logger.debug("Attempting encode")
            self.stegano.encode()
            input_filetype = self.picfile[-4:].lower()
            if self.outfile == sys.stdout:
                output_filetype = input_filetype
            else:
                output_filetype = self.outfile[-4:].lower()

            if output_filetype == ".jpg":
                logger.warning("Cannot save to jpg. Will save to png instead.")
                #
                # replace JPG by PNG in output image
                #
                output_filetype = '.png'
                if self.outfile != sys.stdout:
                    self.outfile = self.outfile[:-4] + ".png"
            logger.debug("Encoded image ready")
            if self.outfile == sys.stdout:
                logger.debug("Writing image to stdout")
                self.stegano.output_image(output_filetype)
            else:
                logger.info(f"Write image to {self.outfile}")
                self.stegano.write_image(self.outfile)
        except Exception as e:
            logger.error(f"Unexpected error while encoding: {e}", exc_info=self.debug)

    def decode(self):
        try:
            if self.infile and self.infile != sys.stdin:
                logger.warning(f"Infile parameter {self.infile} ignored. Not required for decoding")
            logger.debug("Attempting decode")
            self.stegano.decode()
            logger.debug("Image analysed")
            t = self.stegano.data.decode('utf-8')
            logger.debug("Text found utf-8")
            if self.outfile == sys.stdout:
                sys.stdout.write(t)
            else:
                logger.info(f"Write text to {self.outfile}")
                self.stegano.write_data(self.outfile)
        except UnicodeError:
            logger.error("Cannot find any text in this image")
        except OSError as e:
            logger.error(f"Failed to open {self.outfile} for write. Reason: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while decoding: {e}", exc_info=self.debug)


def main():
    c = Csteg(argparse.ArgumentParser())
    c.parse()
    Full_Log("csteg")
    c.run()


if __name__ == '__main__':
    main()
