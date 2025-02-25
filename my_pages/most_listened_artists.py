import io
import base64
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if "playlist_data" in st.session_state and st.session_state.playlist_data:
    playlist_data = st.session_state.playlist_data
    tracks = playlist_data['tracks']

    # Group by artist
    artist_counts = pd.Series([track['artist'] for track in tracks]).value_counts()

    # Create a figure
    fig, ax = plt.subplots(figsize = (8, 6), dpi = 100)

    sns.barplot(
        x = artist_counts.values,
        y = artist_counts.index,
        hue = artist_counts.values,
        palette = "Greens_d",
        ax = ax,
        legend = False,
    )

    ax.set_title("Most listened artists", fontsize = 16, weight = "bold")
    ax.set_xlabel("Number of songs", fontsize = 12)
    ax.set_ylabel("Artist", fontsize = 12)
    ax.grid(axis = "x", linestyle = "--", alpha = 0.5)
    sns.despine(left = True, bottom = True)

    buffer = io.BytesIO()
    fig.savefig(buffer, format = "png", bbox_inches = "tight", dpi = 100)
    buffer.seek(0)

    # Convert buffer to Base64 string
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Embed the image in HTML and center it
    html_code = f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{encoded_image}" alt="Chart">
        </div>
        """

    # Display the HTML in Streamlit
    st.markdown(html_code, unsafe_allow_html = True)

    # Extract the top 5 most listened-to artists
    top_5_artists = artist_counts.head(5)

    # Generate a witty message
    if len(top_5_artists) >= 5:
        message = (
            f"Your top 5 artists are an eclectic mix of pure genius! Here's the lineup:\n\n"
            f"🎤 **{top_5_artists.index[0]}**: Clearly the reigning champion of your playlist. "
            f"You might as well start writing their fan mail now!\n\n"
            f"🎸 **{top_5_artists.index[1]}**: A close second, proving that talent knows no bounds. "
            f"They're basically the sidekick every superhero playlist needs.\n\n"
            f"🎶 **{top_5_artists.index[2]}**: Ah, the middle child of your playlist! They might not steal the spotlight, "
            f"but they hold the vibe together like glue.\n\n"
            f"🥁 **{top_5_artists.index[3]}**: The wildcard. A little mysterious, always intriguing, "
            f"and the one you play when you're feeling adventurous.\n\n"
            f"🎷 **{top_5_artists.index[4]}**: The underdog of the group. They may not have the numbers, "
            f"but their tunes hit you right in the feels every time.\n\n"
            f"Together, this powerhouse quintet defines your unique taste in music. "
            f"Keep vibing, keep thriving, and maybe throw them a thank-you dance!"
        )
    else:
        message = "Looks like your playlist is still growing—just like your impeccable taste in music!"

    # Display the message
    st.markdown("\n")
    st.subheader("Top 5 Artists")
    st.markdown(message)
    st.markdown("\n\n")

else:
    st.warning("Please enter a valid Spotify playlist link on the home page to proceed.")
