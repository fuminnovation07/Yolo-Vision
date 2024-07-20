from PIL import Image
from helpers import get_youtube_stream_url, load_model, predict_and_annotate, process_video, process_youtube_video
import streamlit as st
from home import show_home

if 'model' not in st.session_state:
    st.session_state['model'] = load_model()

st.markdown("""
    <style>
        /* General font and layout adjustments */
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        .text-justify {
            text-align: justify;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #f1f1f1, #e5e5e5); /* Gradient background for sidebar */
        }
        header {
            background-color: #ff6347; /* Stylish orange-red header */
        }

        /* Centering the main title and adding an icon */
        h1 {
            text-align: center;
            color: #000000; /* You can choose a color that fits your branding */
            background: url('https://example.com/path_to_icon.png') no-repeat left; /* Replace URL with actual path to an icon */
            padding-left: 35px; /* Adjust padding to accommodate the icon size */
        }

        /* Gradient background theme for the app */
        body {
            background: linear-gradient(to right, #ffffff, #e6e9f0, #ccdde9); /* Enhanced subtle gradient from white to light blue */
            color: #333333; /* Darker text for better readability */
            font-family: Arial, sans-serif; /* Professional font family */
        }

        /* Button and interaction styling */
        .stButton>button {
            width: 100%; /* Make all buttons equal width */
            border-radius: 5px; /* Rounded corners for buttons */
            background-color: #0068c9; /* Blue background for buttons */
            color: white; /* White text for contrast */
        }

        /* Styling for images and videos to appear more professional */
        .stImage, .stVideo {
            border-radius: 8px; /* Rounded corners for images and videos */
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
            margin-bottom: 10px; /* Space below images and videos */
        }

        /* Styling for anchor tags and hover effects */
        a {
            margin-right: 10px; /* Adds spacing between icons */
            transition: transform 0.3s ease; /* Smooth transition for hover effect */
        }
        a:hover {
            transform: scale(1.1); /* Slightly enlarge icons on hover */
        }
        
    </style>
    """, unsafe_allow_html=True)

st.title("Yolo Vision")

# Define the navigation structure
st.sidebar.title('Navigation')
# Initialize or use existing session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Home'
# Function to change page
def set_page(page):
    st.session_state['current_page'] = page

# Creating buttons for each page in the sidebar with emojis
pages = {
    'Home': '🏠 Home',
    'Image': '🖼️ Image',
    'Video': '🎥 Video',
    'YouTube Video': '▶️ YouTube Video'
}
for page, label in pages.items():
    if st.sidebar.button(label):
        set_page(page)

st.sidebar.subheader('About Us')

st.sidebar.markdown("""
    <div style="text-align: justify;">
        This demo is prepared by <strong>FUMinnovation</strong>, a company that specializes in transforming and automating industries and enterprises with AI. We provide services in chatbots, computer vision, and more.
        <br><br>
        For any queries, contact us via WhatsApp at: <a href="https://fuminnovation.com/" target="_blank">
        <img src="https://img.icons8.com/color/48/000000/whatsapp--v1.png" style="width:24px;height:24px;"/> 03105472304</a> or visit our <a href="https://yourwebsite.com" target="_blank">website</a>.
        We hope you enjoy this demo!
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("Follow Us")
github_url = "https://github.com/fuminnovation07"
huggingface_url = "https://huggingface.co/fuminnovation07"
blog_url = "https://fuminnovation.com/"
linkedin_url = "https://www.linkedin.com/company/fuminnovationai/"

st.sidebar.markdown(f"""
    <a href="{github_url}" target="_blank">
        <img src="https://img.icons8.com/fluent/48/000000/github.png" alt="GitHub" style="width:32px;height:32px;">
    </a>
    <a href="{huggingface_url}" target="_blank">
        <img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="Hugging Face" style="width:32px;height:32px;">
    </a>
    <a href="{blog_url}" target="_blank">
        <img src="https://img.icons8.com/fluent/48/000000/blogger.png" alt="Blog" style="width:32px;height:32px;">
    </a>
    <a href="{linkedin_url}" target="_blank">
        <img src="https://img.icons8.com/color/48/000000/linkedin.png" alt="LinkedIn" style="width:32px;height:32px;">
    </a>
    """, unsafe_allow_html=True)

# Page functionality
if st.session_state['current_page'] == 'Home':
    show_home()

elif st.session_state['current_page'] == 'Image':
    st.subheader('Image Detection')
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"], on_change=None,
                                     help='Select an image file for object detection.')

    if st.button('Detect Objects 🚀'):
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')

            with st.spinner('⏳ Detecting..'):
                model = st.session_state['model']
                predicted_image = predict_and_annotate(model, image.copy())  # Preserve original
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption='Original Image', use_column_width=True)
                with col2:
                    st.image(predicted_image, caption='Detected Image', use_column_width=True)
        else:
            st.error('❗ Please upload an image.')

elif st.session_state['current_page'] == 'Video':
    st.subheader('Video Detection')
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"],
                                     help='Select a video file for object detection.')

    if st.button('Detect Video 🚀'):
        if uploaded_file is not None:
            with st.spinner('⏳ Detecting objects for 5 sec video...'):
                model = st.session_state['model']
                video_bytes = process_video(uploaded_file, model)
                st.video(video_bytes)
        else:
            st.error('❗ Please upload a video')

elif st.session_state['current_page'] == 'YouTube Video':
    st.subheader('YouTube Video Detection')
    url = st.text_input('🔗 Enter YouTube URL', help='Paste a YouTube URL to process the video.')
    if st.button('Download and Detect 🚀'):
        if url:
            with st.spinner('⏳ Detecting objects for 5 sec youtube video...'):
                st.info('ℹ️ Downloading...')
                stream = get_youtube_stream_url(url)

                if stream:
                    st.video(stream)
                    st.info('ℹ️ Detecting objects...')
                    model = st.session_state['model']
                    youtube_bytes = process_youtube_video(stream, model)
                    st.video(youtube_bytes)
                else:
                    st.error('❗ Failed to retrieve YouTube stream. Check the URL and try again.')
        else:
            st.error("❗ Please enter a YouTube URL")





