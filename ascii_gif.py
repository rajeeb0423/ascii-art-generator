from PIL import Image, ImageSequence
import sys
import base64
import numpy as np
import matplotlib.pyplot as plt
import io
import streamlit as st

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches = "tight")
    buf.seek(0)
    img = Image.open(buf)
    return img

def convert_to_ascii(img, density_val, ascii_imgs, col_val):
    with col_val:
        plt.ioff()   
        num_frames =img.n_frames
        progress_text = st.columns(3)[1].markdown("#### :red[Converting to ASCII gif. Please wait...]")
        my_bar = st.columns(3)[1].progress(0, width=500)

        for i, frame in enumerate(ImageSequence.Iterator(img)):
                my_bar.progress(i/num_frames, width=500)
                ascii_gif = []
                ascii_text = ''
                width = 100
                height = int(np.round(100*(frame.size[1]/frame.size[0])*0.5))
                resize_frame = np.array(frame.convert('L').resize((width, height), Image.Resampling.LANCZOS))

                new_array = (np.zeros_like(resize_frame)).astype('str')

                for i in range(resize_frame.shape[0]):
                    for j in range(resize_frame.shape[1]):
                        cell_val = resize_frame[i,j]
                        density_idx = int(np.floor(cell_val/256 * len(density_val)))
                        new_array[i,j] = density_val[density_idx]
                

                ascii_gif.append(new_array)
                for i in range(new_array.shape[0]):
                    a = ''.join(new_array[i])
                    ascii_text += a+'\n'

                fig, ax= plt.subplots()
                x = plt.text(0, 1, ascii_text, ha='left', va='top', transform=ax.transAxes, fontdict=dict(family='monospace'), parse_math=False)# transform = ax.transAxes)
                x = plt.axis('off')
                
                temp_frame = fig2img(fig)
                ascii_imgs.append(temp_frame)
                plt.close()
                
        return ascii_imgs, my_bar, progress_text


def main():

    st.set_page_config(page_title="GIF to ASCII Generator", layout='wide')

    st.markdown("<h1 style='text-align: center; font-family:Monaco'> GIF to ASCII art converter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-family:Monaco'> Welcome to our GIF to ASCII Art tool! Use our free online generator to quickly and easily convert any GIF into stunning ASCII animation.</p>", unsafe_allow_html=True)
    st.divider()

    ascii_images = []

    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        st.markdown('## Choose a gif:')
        im = st.file_uploader('img', type = ['gif'],label_visibility = 'collapsed')
        blocks = '█▓▒░'
        standard = "@%#*+=-:."
        long = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'.'
        ascii_type = {'blocks': blocks, 'standard': standard, 'long': long}
        ascii_selection=st.selectbox('**Select the character set:**',ascii_type.keys())
        density = ascii_type[ascii_selection]
        contrast=st.slider('**Increase contrast level:**', 0, 10, 0, 1)
        density = density + contrast*" "

        on = st.toggle("Inverse")

        if on:
            density = density[::-1]

        duration = st.slider('**Choose time delay between each frame in milliseconds:**', 10, 200, 50, 10)

    if im != None:
        gif_img = Image.open(im)
        ascii_gif, bar, text_val = convert_to_ascii(gif_img, density, ascii_images, col2)
        ascii_gif[0].save('gif_ascii.gif', save_all=True, append_images = ascii_gif[1:], duration = duration, loop=0)

        with col2:
            with open('gif_ascii.gif', 'rb') as f:
                contents = f.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                text_val.empty()
                bar.empty()
                st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="ASCII gif">',unsafe_allow_html=True,)
                st.write(' ')
                st.download_button('Download', f, file_name='%s_ASCII.gif' %(im.name[:-4]), type='primary', on_click='ignore')  
            
        #st.markdown("<p style='text-align: left; font-family:Monaco'>Want to convert gifs to ASCII animation instead? Try our GIF to ASCII tool in the navigation bar and creating ASCII magic of your favorite GIFs!</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()