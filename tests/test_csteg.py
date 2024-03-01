import unittest
from unittest.mock import patch
from cli.csteg import Csteg
import sys
import argparse
from io import StringIO


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # print(message)
        # raise ValueError(message)  # reraise an error
        # re raise the same exception
        raise sys.exc_info()[1]


class Test_Parse(unittest.TestCase):

    def setUp(self):
        parser = ErrorRaisingArgumentParser()
        self.cmd = Csteg(parser)

    def test_parse_pic(self):
        self.cmd.parse(r"--pic tests/image.jpg -a decode".split())
        self.assertEqual(self.cmd.picfile, "tests/image.jpg")
        self.assertEqual(self.cmd.action, 'decode')
        self.assertEqual(self.cmd.infile, sys.stdin)
        self.assertEqual(self.cmd.outfile, sys.stdout)

        self.cmd.parse(r"--pic tests/image2.png --action decode ".split())
        self.assertEqual(self.cmd.picfile, "tests/image2.png")
        self.assertEqual(self.cmd.action, 'decode')
        self.assertEqual(self.cmd.infile, sys.stdin)
        self.assertEqual(self.cmd.outfile, sys.stdout)

    def test_parse_out(self):
        self.cmd.parse(r"--pic tests/image2.png -a decode -o toto.txt".split())
        self.assertEqual(self.cmd.picfile, "tests/image2.png")
        self.assertEqual(self.cmd.action, 'decode')
        self.assertEqual(self.cmd.infile, sys.stdin)
        self.assertEqual(self.cmd.outfile, "toto.txt")

    def test_parse_error(self):
        with self.assertRaises(argparse.ArgumentError):
            self.cmd.parse(r"--pic tests/image2.png -a truc -o toto.txt".split())


class Test_Encode(unittest.TestCase):
    def setUp(self):
        self.cmd = Csteg(argparse.ArgumentParser())
        self.cmd.infile = 'tests/testinput.txt'
        self.cmd.outfile = 'tests/image.png'
        self.cmd.picfile = 'tests/image.jpg'
        self.cmd.debug = True
        self.cmd.verbose = True

    def test_encode_decode_compare(self):
        self.cmd.infile = 'tests/Bonjour.txt'
        self.cmd.outfile = 'tests/Bonjour.png'
        self.cmd.picfile = 'tests/Bonjour.jpg'
        self.cmd.stegano.read_image(self.cmd.picfile)
        self.cmd.encode()
        self.cmd.outfile = 'tests/Bonjour2.txt'
        self.cmd.infile = None
        self.cmd.decode()
        with open('tests/Bonjour.txt') as f1:
            d1 = f1.read()
        with open('tests/Bonjour2.txt') as f2:
            d2 = f2.read()
        self.assertEqual(d1, d2)

    @patch('sys.stdin', StringIO('Bonjour'))
    def test_encode_stdin(self):
        self.cmd.infile = sys.stdin
        self.cmd.outfile = 'tests/Bonjour.png'
        self.cmd.picfile = 'tests/Bonjour.jpg'
        self.cmd.stegano.read_image(self.cmd.picfile)
        self.cmd.encode()
        self.cmd.outfile = 'tests/Bonjour2.txt'
        self.cmd.infile = None
        self.cmd.decode()
        with open('tests/Bonjour2.txt') as f2:
            d2 = f2.read()
        self.assertEqual("Bonjour", d2)


class Test_Decode(unittest.TestCase):
    def setUp(self):
        self.cmd = Csteg(argparse.ArgumentParser())
        self.cmd.debug = True
        self.cmd.verbose = True

    @patch('sys.stdout', new_callable=StringIO)
    def test_decode_stdout(self, fo):
        self.cmd.infile = None
        self.cmd.outfile = sys.stdout
        self.cmd.picfile = 'tests/Bonjour.png'
        self.cmd.stegano.read_image(self.cmd.picfile)
        self.cmd.decode()
        self.assertEqual(fo.getvalue(), "Bonjour")


if __name__ == '__main__':
    unittest.main()
