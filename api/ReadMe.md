# Flask API
The present API is requires the installation of Flask with:

`pip install flask`

It provides access through HTTP to the steganography functions: encode and decode.

## Base URL
`http//localhost:5000/`

## POST /steg/encode

### Form-data parameters
- `image`: image file (JPEG, PNG, BMP)
- `text`: text file containing the message to be encoded in the image

### Response
- (Binary): image/png,  PNG image with the concealed message

## POST /steg/decode

### Form-data parameters
- `image`: Image file (PNG or other lossless formats) with a text message encoded inside

### Response
- `decoded.txt`: text/plain, text file containing the message decoded from the image

## Example usage in Python
```
import request
#
# encode the text in the image
#
url = "http://localhost:5000/steg/encode"
with open(r".\tests\Bonjour.jpg", "rb") as img, open(r".\tests\testinput.txt", "rb") as txt:
    files = {"image": img, "text": txt}
    response = requests.post(url, files=files)
#
# collect the encoded image
#
if response.status_code == 200:
    with open("encoded_image.png", "wb") as f:
        f.write(response.content)
else:
    print("Error:", response.status_code, response.text)
```