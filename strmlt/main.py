import logging
import os
import sys

import streamlit as st
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from stegano import Stegano

INTRO = """Hide a text in a picture or reveal the text hidden in a picture with steganography."""

st.set_page_config(page_title="Steg", layout="wide")


# --- Init état ---
if "action" not in st.session_state:
    st.session_state.action = None
if "text" not in st.session_state:
    st.session_state.text = ""
if "encoded_image" not in st.session_state:
    st.session_state.encoded_image = None
if "steg" not in st.session_state:
    st.session_state.steg = Stegano()

logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("watchdog").setLevel(logging.WARNING)
logger = logging.getLogger("wsteg")
logger.setLevel(logging.INFO)
logger.propagate = False
if "wsteg_handlers_attached" not in st.session_state:
    formatter = logging.Formatter('%(asctime)s *%(levelname)s* %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    st.session_state.wsteg_handlers_attached = True

st.title("Steganography")
st.write(INTRO)


# Image fournie
uploaded = st.file_uploader("Select an image:", type=["png", "jpg"])
if uploaded:
    #
    # this image is used for display only
    # PIL format
    imgPIL = Image.open(uploaded)
    st.image(imgPIL, caption="Loaded image", width=600)
    #
    # it has to be read again for processing
    # cv2 format
    # reset reading pointer to the beginning
    uploaded.seek(0)
    st.session_state.steg.bs2image(uploaded.read())
else:
    st.stop()

# Text initialisé à blanc
st.session_state.text = ""


# Choix du mode
action = st.radio("Select an action:", ["Hide", "Reveal"])
st.session_state.action = action

if action == "Hide":
    # --- Mode encodage ---
    # choice = st.radio("Text source:", ["File", "Manual input"])
        
    txt_file = st.file_uploader("Upload and/or edit the text to hide", type=["txt"])
    if txt_file:
        st.session_state.text = txt_file.read().decode("utf-8")


# --- Mode décodage ---
if action == "Reveal":
    try:
        #
        # Decode contained text
        #
        st.session_state.steg.decode()
        #
        st.session_state.text = st.session_state.steg.data.decode('utf-8')
    except UnicodeDecodeError:
        st.text_area("Decode error:",
                     "No text in this picture",
                     height=200)
        st.stop()
    except Exception as e:
        st.text_area("Decode error:", str(e), height=200)
        st.stop()

    
st.session_state.text = st.text_area(
    "Text:", st.session_state.text,
    height=200)

if action == "Hide":
    # Exécution
    if st.button("Do it !"):
        try:
            #
            # if len(pic) == 0:
            #    raise ValueError("Missing picture")
            #
            # collect possibly edited text
            #
            txt = st.session_state.text
            #
            if len(txt.strip()) == 0:
                raise ValueError("Missing text")
            st.session_state.steg.data = bytearray(txt, 'utf-8')
            #
            # encode
            #
            st.session_state.steg.encode()
            #
            #
            #
            st.session_state.encoded_image = st.session_state.steg.image2bs(".png")
        except Exception as e:
            print(e)
            st.session_state.encoded_image = None

    # Affichage + sauvegarde
    if st.session_state.encoded_image:
        st.image(st.session_state.encoded_image, caption="Encoded image" , width=600)
        st.download_button(
            "Download the image with the hidden text",
            data=st.session_state.encoded_image,
            file_name="encoded.png",
            mime="image/png"
        )
