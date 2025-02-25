import streamlit as st
from utils import fetch_playlist_data

st.title("Welcome to Spotify data insights! 🎶")

st.markdown("This app allows you to :green-background[analyse] and :green-background[visualise] data from your :green[***Spotify playlists***].")

st.markdown("""\n### You can start with these simple steps:""")

st.markdown("""
1. Open :green[***Spotify***] and go to the playlist you want to analyze.
2. Click the three dots (:material/more_horiz:) next to the playlist name.
3. Select :green[***'Share'***] → :green[***'Copy Playlist Link'***].
4. Paste the link in the input field below.
""")

st.markdown(":red-background[**WARNING**] It must be a user created playlist! Sadly, Spotify doesn't provide API endpoints for editorial playlists anymore.")

# User input for playlist link
playlist_url = st.text_input("Enter a Spotify playlist link:")

if playlist_url:
    # Save the playlist URL to session state
    st.session_state.playlist_url = playlist_url

    # Fetch playlist data if not already loaded
    if "playlist_data" not in st.session_state or st.session_state.playlist_url != playlist_url:
        with st.spinner("Fetching playlist data..."):
            st.session_state.playlist_data = fetch_playlist_data(playlist_url)

    playlist_data = st.session_state.playlist_data

    # Display playlist information
    st.subheader("Playlist details :loud_sound:")
    st.markdown(f"""
            - **Name:** '{playlist_data['name']}'
            - **Description:** {playlist_data['description'] if playlist_data['description'] != '' else 'No description available.'}
            - **Number of tracks:** {len(playlist_data['tracks'])}
        """)

st.markdown("""\n### Available analyses:""")
st.markdown("""
     - **Release year :hourglass_flowing_sand:**: Visualise the distribution of song release years.
     - **Listening habits :headphones:**: Analyse when you listen to music most often.
     - **Popularity :sparkles:**: Compare the popularity of songs with your personal preferences.
""")
