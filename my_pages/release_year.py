import io
import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if "playlist_data" in st.session_state and st.session_state.playlist_data:
    playlist_data = st.session_state.playlist_data
    tracks = playlist_data['tracks']
    years = [track['release_year'] for track in tracks]

    # DataFrame for analysis
    df = pd.DataFrame({'Release Year': years})
    year_counts = df['Release Year'].value_counts().sort_index()

    # Plotting with Seaborn
    sns.set_theme(style = "whitegrid")  # Set Seaborn theme with green palette

    fig, ax = plt.subplots(figsize = (8, 5))  # Adjust figure size
    sns.barplot(
        x = year_counts.index,
        y = year_counts.values,
        ax = ax,
        hue = year_counts.index,
        palette = "Greens_d",
        legend = False
    )

    # Customize the chart aesthetics
    ax.set_title("Number of songs by release year", fontsize = 16, weight = 'bold')
    ax.set_xlabel("Release year", fontsize = 14)
    ax.set_ylabel("Count", fontsize = 14)
    ax.tick_params(axis = 'x', rotation = 45)  # Rotate x-axis labels for better readability
    sns.despine(left = True, bottom = True)  # Clean up the axes

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

    # Determine the year with the most listened-to songs
    most_listened_year = year_counts.idxmax()
    most_listened_count = year_counts.max()

    # Display a witty message based on the most listened-to year
    if most_listened_year < 2020:
        st.markdown(f"\n:sparkles: **{most_listened_year}** :sparkles: was your golden age! Nostalgia is your superpower, and you've made it your mission to keep the classics alive with **{most_listened_count} songs** from that year. The past called, and you picked up! :telephone_receiver:")
    else:
        st.markdown(f"\n:sparkles: **{most_listened_year}** :sparkles: is where your playlist shines! You're tuned into the rhythm of the present, riding the wave of fresh beats and bold sounds with **{most_listened_count} tracks**. Keep grooving—you're a trendsetter in the soundtrack of now! :woman-tipping-hand:")

else:
    st.warning("Please enter a valid Spotify playlist link on the home page to proceed.")
