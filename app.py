import sys,os
import pandas as pd
import streamlit as st
import base64
print(os.getcwd())
import mongo_test
import logging
import datetime

logging.basicConfig(filename='app_logger.log', encoding='utf-8', level=logging.DEBUG,filemode="w")

from PIL import Image
try:
    time_stmp=os.path.getmtime('app_logger.log')
    time_mod=datetime.datetime.fromtimestamp(time_stmp)
except Exception as e:
    st.write(e)


def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

if __name__ == "__main__":

    my_logo = add_logo(logo_path="./imgs/Kalika logo.png", width=300, height=60)
    st.image(my_logo)
    st.title("PO TRACKER")

    PO = st.text_input("Enter your PO Number"," ")
    PO = PO.replace(" ","").upper()

    df_list=[]
    N=15
    num_of_days=(datetime.datetime.now()-time_mod).days
    if num_of_days>N:
        os.remove('app_logger.log')
    try:
        if PO:
            plot_items=['Quantity Ordered','Quantity Shipped','Quantity Received','PENDING']
            df_list=[]
            columns = ["PO Number", "Item No", "Item Description", "Quantity Shipped"]

            if st.button("Track"):
                st.write("PO_DB connect inprogress")
                with st.spinner('Wait for it...'):
                    po_status_data = mongo_test.find_with_po(PO)
                    # st.write(po_status_data)

                    if po_status_data!=None:
                        df=mongo_test.records_dataframe(po_status_data)
                        # st.table(df)
                        if len(df) > 0:
                            st.table(df[['PO Number', 'Item No', 'Item Description', 'Quantity Ordered', 'Material Status']])

                    else:
                        st.write('No Data Updated Please check PO number')

    except Exception as e:
        st.write('Connection Error please connect after some time')
