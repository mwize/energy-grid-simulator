import streamlit as st

def inject_custom_css():
    # Moves Buttons to the bottom
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"][height="430px"] {
            display: flex !important;
            flex-direction: column !important;
        }

        div[data-testid="stVerticalBlock"][height="445px"] > div:last-child {
            margin-top: auto !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
                <style>
                    .block-container {
                        padding-top: 60px;
                        padding-bottom: 60px;
                        padding-left: 10px !important;
                        padding-right: 10px !important;
                    }
                </style>
            """, unsafe_allow_html=True)

