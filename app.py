import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from io import BytesIO

# File to store comments
comments_file = "comments.txt"

# Function to load comments from the file
def load_comments():
    if os.path.exists(comments_file):
        with open(comments_file, "r") as f:
            comments = f.readlines()
        return [comment.strip() for comment in comments]
    return []

# Function to save a new comment
def save_comment(comment):
    with open(comments_file, "a") as f:
        f.write(comment + "\n")

# Function to generate a word cloud
def generate_wordcloud(comments):
    text = ' '.join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Main app
def main():
    st.title("Menti-Like Tool")
    st.subheader("Provide your comments below:")

    # Create a session state to track comments
    if 'comments' not in st.session_state:
        st.session_state.comments = load_comments()  # Load existing comments

    # Create a full-width container for layout
    with st.container():
        # Create two columns within the container
        col1, col2 = st.columns([3, 1])  # Adjust the proportions as needed

        # Show the comments and generate the word cloud in the first column
        with col1:
            if st.session_state.comments:
                # Generate and display the word cloud
                st.subheader("Word Cloud:")
                wordcloud = generate_wordcloud(st.session_state.comments)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')

                # Save word cloud to a BytesIO object to display in Streamlit
                img = BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                st.image(img, use_column_width=True)

                plt.close()  # Close the matplotlib figure

        # Text input for comments in the second column
        with col2:
            comment = st.text_input("Enter your comment:")
            
            if st.button("Submit"):
                if comment:
                    save_comment(comment)  # Save comment to file
                    st.session_state.comments.append(comment)  # Update session state

if __name__ == "__main__":
    main()
