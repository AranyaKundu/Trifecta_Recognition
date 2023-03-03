import streamlit as st, numpy as np
from streamlit_option_menu import option_menu
from io import StringIO
from PIL import Image
import data_prep, all_funcs
import jarvis
import subprocess, os
import tensorflow as tf
from tensorflow import keras

#make it look nice from the start
st.set_page_config(layout='wide')

# create a horizontal menu
selected = option_menu(None, ["Home", "Analysis", "Image Recognition", "ChatGPTLite"], 
    icons=['house', 'graph-down', 'cloud-upload', "gear"], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Home":
    st.sidebar.title("Welcome to the most iconic Streamlit multipage Dashboard")
    image = Image.open("D:/Coursework\Mod-3/Unstructured Data Analytics/Project/NDGD.jpeg")
    aspect_ratio = image.width / image.height
    height = int(st.experimental_get_query_params().get("height", ["1000"])[0])
    width = int((height - 100) * aspect_ratio)
    resized_image = image.resize((width, height - 100))
    st.image(resized_image, caption="The Heavenly Iconic Golden Dome")

if selected == "Analysis":

    st.sidebar.title("GroupMe Chat Analytics Dashboard") # Title in the sidebar

    file_upload = st.sidebar.file_uploader(label="Choose a File to upload") # File upload space

    # Code will be executed only after a file is uploaded
    if file_upload is not None:
        str_data = file_upload.getvalue().decode("utf-8") # convert to "utf-8" format
        final_df = data_prep.data_prep(str_data) # prepares the data into a pandas dataframe (works only for GroupMe chat messages) 
        # Need to include code for other chat analyzers with selectbox
        st.dataframe(final_df) # displays prepared data in the form of a dataframe

        user_list = final_df['Name'].unique().tolist() # Get the list of unique users of the group
        user_list.sort() # Sort the user list (optional)
        user_list.insert(0, "OverAll") # Add Overall to analyze the whole group
        
        st.sidebar.header('Show user specific analysis') # User of dash board to select whose chat to analyze
        user_choice = st.sidebar.selectbox("Choose user", options = user_list)

        # Analysis will be displayed after clicking the button
        if st.sidebar.button('Display Analysis'):
            total_messages = all_funcs.tot_msgs(user_choice, final_df) # Check all_funcs.py for the analysis functions
            tot_words = all_funcs.tot_words(user_choice, final_df)
            tot_attachments = all_funcs.tot_attachments(user_choice, final_df)
            tot_urls = all_funcs.total_urls(user_choice, final_df)
            plot1, table_1 = all_funcs.active_users_bar(final_df)
            wc_1 = all_funcs.create_wc(user_choice, final_df)
            table_2 = all_funcs.user_sentiment(user_choice, final_df)

            # Group and individual stats
            # Create a container and all columns in it
            with st.container():
                col1, col2, col3, col4 = st.columns(4) # Create 4 equal-sized columns
                # Add content in 1st column
                with col1:
                    st.header("Total Messages")
                    st.title(total_messages)
                # Add content in 2nd column
                with col2:
                    st.header("Words Count")
                    st.title(tot_words)

                # Add content in 3rd column
                with col3:
                    st.header("Attachments Count")
                    st.title(tot_attachments)

                # Add content in 4th column
                with col4:
                    st.header("URLs Count")
                    st.title(tot_urls)

            if (user_choice == "OverAll"):
                # Start container 2: Plot top 5 most active users
                with st.container():
                    st.title("Most Active Users")
                    col5, col6 = st.columns(2) # Create 2 equal sized columns

                    # Add content to 1st column
                    with col5:
                        st.pyplot(plot1)
                    
                    with col6:
                        st.dataframe(table_1, use_container_width = True)
                
                with st.container():
                    st.dataframe(table_2, use_container_width = True)
            
            else: pass

            with st.container():
                st.title("WordCloud")
                st.pyplot(wc_1)
            
            


if selected == "ChatGPTLite":
    image = Image.open("D:/Coursework\Mod-3/Unstructured Data Analytics/Project/BOT.jpeg")
    aspect_ratio = image.width / image.height
    height = int(st.experimental_get_query_params().get("height", ["1000"])[0])
    width = int((height - 100) * aspect_ratio)
    resized_image = image.resize((width, height - 100))
    st.image(resized_image, caption="Chat GPT Lite")

    if st.sidebar.button("Launch chatGPT Lite"):
        subprocess.Popen(["python", "jarvis.py"])

if selected == "Image Recognition":
    st.sidebar.title("Image Recognition Dashboard")
    file_upload_2 = st.sidebar.file_uploader(label="Choose a File to upload") # File upload space

    if file_upload_2 is not None:
        classnames = os.listdir("D:/Coursework/Mod-3/Unstructured Data Analytics/Project/images/MSBA_FACE")
        model = keras.models.load_model('D:/Coursework/Mod-3/Unstructured Data Analytics/Project/face_recognition_model.h5')
        img = keras.preprocessing.image.load_img(
            file_upload_2, target_size = (180, 180))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        st.title(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(classnames[np.argmax(score)], 100 * np.max(score))
            )
        st.image(file_upload_2)








if st.sidebar.button('Exit'):
    st.success('Exiting...')
    st.stop()
