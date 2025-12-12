import os
import logging
import sys
from flask import Flask, request, send_file
from io import BytesIO
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from stegano import Stegano
from util.fullog import Full_Log

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/steg/encode', methods=['POST'])
def encode():
    logger.info("Encoding")
    image_file = request.files.get('image')
    logger.debug(f"{image_file}")
    text_file = request.files.get('text')
    logger.debug(f"{text_file}")

    steg = Stegano()

    # Ingest text
    steg.data = text_file.read()#.decode('utf-8')
    # Ingest image
    steg.bs2image(image_file.read())

    steg.encode()

    # return encoded image
    # PNG format is hardcoded !
    return send_file(steg.image_buffer(".png"), mimetype='image/png')

@app.route('/steg/decode', methods=['POST'])
def decode():
    logger.info("Decoding")
    image_file = request.files.get('image')
    logger.debug(f"{image_file}")
 
    steg = Stegano()

    # Ingest image
    steg.bs2image(image_file.read())

    steg.decode()

    # BytesIO converts the BA into an in a suitable memory binary file
    return send_file(
        BytesIO(steg.data),
        mimetype='text/plain',
        download_name='decoded.txt',
        as_attachment=True
    )

if __name__ == '__main__':
    Full_Log('apiserver')
    app.run(host="0.0.0.0", port=5000, debug=True)
