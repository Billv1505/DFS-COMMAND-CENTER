import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        /* Dark base */
        .stApp {
            background: #0e1117;
            color: #e6e6e6;
        }

        /* Hide Streamlit default header/footer */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* App header */
        .app-header {
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            padding: 1rem 0 0.5rem 0;
            color: #4ade80;
            border-bottom: 1px solid #1f2937;
            margin-bottom: 1rem;
        }

        /* Section labels */
        .section-label {
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            color: #9ca3af;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }

        /* Slate meta */
        .slate-meta {
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: -0.5rem;
        }

        /* Footer note */
        .footer-note {
            text-align: center;
            font-size: 0.75rem;
            color: #4b5563;
            letter-spacing: 0.1em;
            padding: 1rem 0;
        }

        /* Dataframe container */
        [data-testid="stDataFrame"] {
            border: 1px solid #1f2937;
            border-radius: 8px;
            overflow: hidden;
        }

        /* Select box styling */
        div[data-baseweb="select"] > div {
            background-color: #111827 !important;
            border-color: #1f2937 !important;
            color: #e6e6e6 !important;
        }

        /* Buttons */
        .stButton button {
            background-color: #111827;
            color: #4ade80;
            border: 1px solid #1f2937;
            border-radius: 6px;
        }
        .stButton button:hover {
            border-color: #4ade80;
            color: #4ade80;
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            border: 1px dashed #1f2937;
            border-radius: 8px;
            padding: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
