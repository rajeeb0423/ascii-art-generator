import streamlit as st

def main():

    ascii_image = st.Page('ascii_image.py', title='Image to ASCII generator')
    ascii_gif = st.Page('ascii_gif.py', title='GIF to ASCII generator')

    pg = st.navigation([ascii_image, ascii_gif])#, position='hidden')

    st.set_page_config(page_title= 'ASCII Image Generator', layout='wide')
    pg.run()

if __name__ == '__main__':
    main()