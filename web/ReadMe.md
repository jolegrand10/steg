# Wsteg #

`wsteg` uses a web page as the human interface to the Stegano class.

There is only 1 web page and it is called `index.html`.

It refers to a skeletal CSS stylesheet and uses PyScript instead of JavaScript.

To operate properly, it is necessary that the following files reside together with the html page:
- index.html
- css stuff
- wsteg.py
- wsteg.toml
- stegano.py

`stegano.py` contains the Class with the necessary methods to encode/decode texts in image.
The `toml` document is necessary to state the modules and the libraries required by the `wsteg.py` script.

## Usage

The page allows to upload a picture file. 

A text can, similarly, be uploaded and/or edited, in the text box, next to the image.\
This text is necessary only when the
page is used for encoding.\
For decoding, the text box should be left empty.

Clicking on "Hide" creates an encoded image that can be collected using the mouse ("Save as", "Send to") and the 
native capabilities of the browser.

Clicking on "Reveal" extracts the text contained in the image and displays it in the text box.

The last line of the screen may show the status of the application and messages when something does not happen as expected.

As PyScript requires `opencv` to be installed, when the page is first loaded, there is a time during which it is not
fully functional and the status field shows "Wait...". Operation may start when this message disappears (replaced by "Ready!"
or erased).