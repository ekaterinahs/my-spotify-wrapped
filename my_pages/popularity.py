import io
import base64
from sklearn.linear_model import LinearRegression
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("Here, we will analyse the popularity distribution of your playlist!")

if "playlist_data" in st.session_state and st.session_state.playlist_data:
    playlist_data = st.session_state.playlist_data
    tracks = playlist_data['tracks']

    df = pd.DataFrame([{
        'name': track['name'],
        'artist': track['artist'],
        'popularity': track['popularity'],
        'album_img': track['album_img']
    } for track in tracks])

    # Plotting the popularity distribution using Seaborn with a green palette
    fig, ax = plt.subplots(figsize = (8, 6), dpi = 100)
    sns.histplot(df['popularity'], kde = True, color = 'green', bins = 10, palette = 'darkgreen')

    ax.set_title("Popularity distribution", fontsize = 16, weight = "bold")
    ax.set_xlabel("Popularity", fontsize = 12)
    ax.set_ylabel("Number of songs", fontsize = 12)
    ax.grid(axis = "y", linestyle = "--", alpha = 0.5)
    sns.despine(left = True, bottom = True)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
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

    # Calculate the mean popularity
    mean_popularity = df['popularity'].mean()

    # Display the mean popularity and a witty message
    st.write(f"\nThe average popularity of the songs in this playlist is {mean_popularity:.2f}.")

    # Witty, funny, and inspiring message based on the mean popularity
    if mean_popularity < 40:
        st.write("\nLooks like you're a true connoisseur of ✨ **hidden gems** ✨. You prefer the underdogs over the mainstream!")
    elif mean_popularity < 70:
        st.write("\nYou're all about the ✨ **balance** ✨. Not too mainstream, not too obscure. You've got a keen taste!")
    else:
        st.write("\nYou're a ✨ **crowd-pleaser** ✨! Looks like you enjoy those popular bangers everyone loves. Keep the party going!")

    # Display Most and Least Popular Songs
    most_popular = df.loc[df['popularity'].idxmax()]
    least_popular = df.loc[df['popularity'].idxmin()]

    # Display album artwork for the most and least popular songs side by side
    col1, col2 = st.columns(2)  # Create two columns for side by side display

    with col1:
        if most_popular['album_img']:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>📈 Most popular song</h3>", unsafe_allow_html = True)
            st.markdown(f"<div style='text-align: center;'><img src='{most_popular['album_img']}' width='250' style='display: block; margin-left: auto; margin-right: auto; border-radius: 50px;' /><p>{most_popular['name']} by {most_popular['artist']}</p></div>",
                unsafe_allow_html = True)
            st.markdown(f"<div style='text-align: center;'>(Popularity: {most_popular['popularity']})",
                        unsafe_allow_html = True)
        else:
            st.write("No album artwork available for the most popular song.")

    with col2:
        if least_popular['album_img']:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>📉 Least popular song</h3>", unsafe_allow_html = True)
            st.markdown(f"<div style='text-align: center;'><img src='{least_popular['album_img']}' width='250' style='display: block; margin-left: auto; margin-right: auto; border-radius: 50px;' /><p>{least_popular['name']} by {least_popular['artist']}</p></div>",
                unsafe_allow_html = True)
            st.markdown(f"<div style='text-align: center;'>(Popularity: {least_popular['popularity']})",
                        unsafe_allow_html = True)
        else:
            st.write("No album artwork available for the least popular song.")

    st.markdown("\n\n\nNow, let's see how the public's opinion of your top 10 playlist tracks compares to your own personal taste! Use the sliders below to rate the songs:")

    popularity = [track['popularity'] for track in tracks[:10]]

    # Initialize session_state for personal scores if not already initialized
    if 'personal_scores' not in st.session_state:
        st.session_state.personal_scores = [50] * len(tracks[:10])  # Default value of 50 for each track

    # Use sliders to collect personal preference ratings
    for i, track in enumerate(tracks[:10]):
        st.session_state.personal_scores[i] = st.slider(track['name'], 0, 100, st.session_state.personal_scores[i])

    # Now that the sliders have been interacted with, we can create the DataFrame
    df_comp = pd.DataFrame({
        'Popularity': popularity,
        'Personal preference': st.session_state.personal_scores
    })

    # Button to trigger the scatter plot
    show_plot_button = st.button("Show plot")

    if show_plot_button and st.session_state.personal_scores:
        # Create the scatter plot with a green palette
        fig, ax = plt.subplots(figsize = (10, 6), dpi=100)

        # Scatter plot with a green color palette based on popularity
        sns.scatterplot(data = df_comp, x = 'Popularity', y = 'Personal preference', hue = 'Popularity', palette = "dark:green", s = 100,
                        ax = ax)

        # Labels and title
        ax.set_title("Popularity vs. Personal Preference", fontsize = 16, fontweight = 'bold')
        ax.set_xlabel("Popularity", fontsize = 12)
        ax.set_ylabel("Personal preference", fontsize = 12)

        # Add y = x trend line (diagonal line where x = y)
        ax.plot([0, 100], [0, 100], color='green', linestyle='--')

        # Show track names as annotations
        for i in range(len(df_comp)):
            ax.annotate(df['name'][i], (df_comp['Popularity'][i], df_comp['Personal preference'][i]),
                        textcoords = "offset points", xytext = (0, 5), ha = 'center', fontsize = 9, color = 'black')

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
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

        # Add a witty and insightful message
        mean_popularity_10 = df_comp['Popularity'].mean()
        mean_preference = df_comp['Personal preference'].mean()

        if mean_preference < mean_popularity - 5:
            st.write(f"You're not here for the mainstream, are you? 😎 It looks like you prefer the hidden gems, leaving the chart-toppers in the dust. Keep doing you and stay unique!")
        elif mean_popularity - 5 <= mean_preference <= mean_popularity + 5:
            st.write(f"You're perfectly in sync with the public's taste! 🎶 It's like you've got a direct connection to the global vibe. Keep riding that wave!")
        else:
            st.write(f"Looks like you have a knack for **underrated gems**! Your personal preferences are ahead of the curve—like you're ahead of the trends, finding the tracks the world hasn't fully caught on to yet. 🔥")

else:
    st.warning("Please enter a valid Spotify playlist link on the home page to proceed.")
