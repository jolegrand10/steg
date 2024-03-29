import unittest
from stegano import Stegano
import sys


class TestStegano(unittest.TestCase):

    def test_read_encode_decode(self):
        s = Stegano()
        s.read_image('tests/image.jpg')
        s.read_data('tests/testinput.txt')
        t = s.data
        s.encode()
        s.decode()
        t1 = s.data
        self.assertEqual(t, t1)

    def test_read_encode_write_reread_decode(self):
        s = Stegano()
        s.read_image('tests/image.jpg')
        s.read_data('tests/testinput.txt')
        t = s.data
        s.encode()
        s.write_image('tests/image2.png')
        s.decode()
        t1 = s.data
        self.assertEqual(t, t1)
        s.write_data('tests/testoutput.txt')
        s.read_image('tests/image2.png')
        s.decode()
        t1 = s.data  # .decode('utf-8')
        self.assertEqual(t, t1)
        s.read_data('tests/testoutput.txt')
        t1 = s.data
        self.assertEqual(t, t1)

    def test_read_sick_file(self):
        s = Stegano()
        if sys.platform == 'win32':
            self.assertRaises(Exception, s.read_image, 'tests/îmàgé.jpg')
        # cv2 @linux seems to behave properly


if __name__ == '__main__':
    unittest.main()
