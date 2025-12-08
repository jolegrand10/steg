import unittest
import io
from api.server import app


class TestApi(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_encode_http(self):
        url = "http://localhost:5000/steg/encode"
        with open(r".\tests\Bonjour.jpg", "rb") as img, \
             open(r".\tests\testinput.txt", "rb") as txt:
            data = {
                "image": (io.BytesIO(img.read()), "Bonjour.jpg"),
                "text": (io.BytesIO(txt.read()), "testinput.txt")
            }
            response = self.client.post(url, data=data, 
                                        content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/png')

    def test_decode_http(self):
        url = "http://localhost:5000/steg/decode"
        with open(r".\tests\imageavecmessage.png", "rb") as img:
            data = {"image": (io.BytesIO(img.read()), "imageavecmessage.png")}
            response = self.client.post(url, data=data, 
                                        content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.headers['Content-Type'].startswith('text/plain'))


if __name__ == '__main__':
    unittest.main()