import streamlit as st
def show_home():
    # Embedding CSS for styling the home page
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, 
                #e8eff1,  /* very light grey-blue at the top */
                #f0f5f8,  /* softer light grey */
                #f7fafc,  /* almost white */
                #e8eff1); /* repeat of the first to ensure smoothness at the bottom */
            color: #333; /* Ensure text is still readable */
            font-family: 'Helvetica Neue', Arial, sans-serif; /* Clean, professional font choice */
        }
            /* General text and layout enhancements */
            h1, h2, h3, .big-font, .stMarkdown {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
            .big-font {
                font-size:20px !important;
                font-weight: bold;
            }
            h1 {
                text-align: center;
            }
            h2 {
                padding-top: 0.5em;
                color: #4a4a4a;
            }
            .text-content {
                padding: 10px;
                text-align: justify;
                line-height: 1.5;
            }

            /* Styling for columns and images */
            .stImage {
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            /* Notification styling */
            .notification {
                padding: 10px;
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                margin-top: 20px;
            }

        </style>
    """, unsafe_allow_html=True)

    st.header('Welcome to Our Object Detection App')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Explore Object Detection with YOLOv8")
        st.markdown("""
            <div class="text-content">
                This app leverages YOLOv8, the latest in the series of YOLO (You Only Look Once) models, known for its exceptional speed and accuracy in real-time object detection. YOLOv8 enhances detection with improved model architectures and training strategies, making it ideal for practical applications in AI.
                Upload your files and witness the AI pinpoint various objects with remarkable precision.
                <br><br>
                <a href="https://github.com/ultralytics/ultralytics" target="_blank">YOLOv8 GitHub Repository</a>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("explore.png", caption="Explore AI", use_column_width=True)

    st.write("---")
    st.header("Features of the App")
    st.image("features.png", caption="App Features", use_column_width=True)
    st.markdown("""
        <style>
            .features-list {
                padding-left: 20px; /* Add space to align text properly */
            }
            .features-list li {
                margin-bottom: 10px; /* Space between list items */
                line-height: 1.6; /* Adjust line spacing for better readability */
            }
            .features-list li strong {
                color: #4a4a4a; /* Dark grey color for bold text */
            }
        </style>
        <div class="text-content">
            <ul class="features-list">
                <li><strong>Image Detection:</strong> Upload images to detect objects.</li>
                <li><strong>Video Detection:</strong> Upload videos to perform real-time object detection, limited to the first 5 seconds of video for processing.</li>
                <li><strong>YouTube Integration:</strong> Provide a YouTube link to analyze videos directly from YouTube, processing only the first 5 seconds.</li>
                <li><strong>Interactive Results:</strong> View and interact with the detection results.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("Get Started")
    st.markdown("""
        <div class="notification">
            Navigate through the sidebar to access the different functionalities of the app. Please note that only the first 5 seconds of any video or YouTube content will be processed for object detection.
        </div>
    """, unsafe_allow_html=True)
    st.image("tumblr_mg4rofgfuY1qc8m6fo1_500.gif", caption="See It in Action", use_column_width=True)

