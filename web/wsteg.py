from js import document, console, window, FileReader, File, Uint8Array, Element
from pyodide.ffi import create_proxy
from stegano import Stegano



# These are globals
pic=bytearray()
txt=""

async def get_bytes_from_file(file):
    array_buf = await file.arrayBuffer()
    return array_buf.to_bytes()


async def _upload_text_file(event):
    global txt

    file_list = event.target.files
    first_item = file_list.item(0)

    status(f"Uploading text in {first_item}")
    bs = await get_bytes_from_file(first_item)
    txt = bs.decode('utf-8')
    document.getElementById("content").innerHTML = txt
    status("")
    message("")



upload_text_file = create_proxy(_upload_text_file)
document.getElementById("text-upload").addEventListener("change", upload_text_file)



async def _upload_pic_file(event):
    global pic
    file_list = event.target.files
    first_item = file_list.item(0)


    # TODO create img if not exists ONLY
    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(first_item)
    document.getElementById("show_pic").appendChild(new_image)

    status(f"Uploading picture {first_item}")
    pic = await get_bytes_from_file(first_item)
    status("")
    message("")


upload_pic_file = create_proxy(_upload_pic_file)
document.getElementById("pic-upload").addEventListener("change", upload_pic_file)

def _reveal(event):
    try:
        status("Revealing...")
        #
        if len(pic) == 0:
            raise ValueError("Missing picture")
        #
        #
        # Instantiate stegano
        #
        s = Stegano()
        s.bs2image(pic)
        #
        # Decode contained text
        #
        s.decode()
        #
        # Display text in web page
        #
        document.getElementById("content").innerHTML = s.data.decode('utf-8')
        console.log("Image is ", document.getElementById("show_pic"))
        #
        status("")
        message("")
    except UnicodeDecodeError:
        status("Failed")
        message("No text in this picture")
    except Exception as e:
        status("Failed")
        message(str(e))


reveal = create_proxy(_reveal)
document.getElementById("button_reveal").addEventListener("click", reveal)

def status(s):
    document.getElementById("status").innerHTML = s

def message(s):
    document.getElementById("message").innerHTML = s

def _hide(event):
    """ conceal text - data in the pic """
    try:
        status("Hiding...")
        #
        if len(pic) == 0:
            raise ValueError("Missing picture")
        #
        # collect possibly edited text from web page
        #
        txt = document.getElementById("content").innerText
        #
        if len(txt.strip()) == 0:
            raise ValueError("Missing text")
        #
        # instantiate Stegano
        #
        s = Stegano()
        s.bs2image(pic)
        s.data = bytearray(txt,'utf-8')
        #
        # encode
        #
        s.encode()
        #
        #
        # Create a JS File object with our data and the proper mime type
        #image_file = File.new([Uint8Array.new(s.image)], "new_image_file.png", {type: "image/png"})
        image_file = File.new([Uint8Array.new(s.image2bs(".png"))], "new_image_file.png", {type: "image/png"})
        #
        # Add new modified image, so that it can be visually compared and then saved
        #
        new_image = document.createElement('img')
        new_image.src = window.URL.createObjectURL(image_file)
        document.getElementById("show_pic").appendChild(new_image)
        #
        status("")
        message("")
    except Exception as e:
        status("Failed")
        message(str(e))


hide = create_proxy(_hide)
document.getElementById("button_hide").addEventListener("click", hide)

def _clear_pic(event):
    global pic
    document.getElementById("show_pic").innerHTML = ""
    pic = bytearray()
    document.getElementById("pic-upload").value = ""
    message("")
    status("")

clear_pic = create_proxy(_clear_pic)
document.getElementById("button_clear_pic").addEventListener("click", clear_pic)

def _clear_txt(event):
    global txt
    document.getElementById("content").innerText = ""
    txt = bytearray()
    document.getElementById("text-upload").value = ""
    message("")
    status("")

clear_txt = create_proxy(_clear_txt)
document.getElementById("button_clear_txt").addEventListener("click", clear_txt)

status("Ready!")
message("")