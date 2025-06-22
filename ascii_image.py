import streamlit as st
import numpy as np
from PIL import Image

def convert_to_ascii(img_path, density_val):
    im = Image.open(img_path).convert('L')

    width = 100
    height = int(np.round(100*(im.size[1]/im.size[0])*0.5))
    density_len = len(density_val)

    resize_pic = np.array(im.resize((width, height), Image.Resampling.LANCZOS))

    ascii_pic = 'Ascii art:\n'
    for i in range(resize_pic.shape[0]):
        for j in range(resize_pic.shape[1]):
            cell_val = resize_pic[i,j]
            density_idx = int(np.floor(cell_val/256 * density_len))
            ascii_pic += density_val[density_len-density_idx-1] 
        ascii_pic += '\n'

    return ascii_pic

    
def main():
    st.html("""<style>
                    code.language-plaintext {
                        font-family: monospace;
                        font-size: 17px;
                        line-height: 0;
                        letter-spacing: 0px;
                        text-wrap: nowrap;
                    }
                </style>
            """)

    st.markdown("<h1 style='text-align: center; font-family:Monaco'> IMAGE to ASCII art converter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family:Monaco'> Welcome to our Image to ASCII Art tool! Use our free online generator to quickly and easily convert any photo into stunning ASCII artwork.</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        st.markdown('## Choose an image:')
        img = st.file_uploader('img', type = ['jpg', 'jpeg', 'png'],label_visibility = 'collapsed')
        if img != None:
            st.image(img)
        blocks = '█▓▒░'
        standard = "@%#*+=-:."
        long = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1}{[]?-_+~<>i!lI;:",^`.'
        ascii_type = {'standard': standard, 'blocks': blocks, 'long': long}
        ascii_selection=st.selectbox('Select the character set:',ascii_type.keys())
        density = ascii_type[ascii_selection]
        contrast=st.slider('Increase contrast level:', 0, 10, 0, 1)
        on = st.toggle("Inverse")
        st.markdown("<p style='text-align: left; font-family:Monaco'>Want to convert gifs to ASCII animation instead? Try our GIF to ASCII tool in the navigation bar and creating ASCII magic of your favorite GIFs!</p>", unsafe_allow_html=True)

    with col2:
        if img != None:
            density = density + contrast*" "
            if on:
                density = density[::-1]

            ascii_text = convert_to_ascii(img, density)
            st.code(ascii_text, language=None)


if __name__ == '__main__':
    main()
