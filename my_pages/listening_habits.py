import io
import base64
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import fetch_recently_played

st.markdown("This feature doesn't involve a playlist. Instead, we will fetch your recently played on Spotify data and analyze your listening habits!")

try:
    recently_played = fetch_recently_played()

    timestamps = [item['played_at'] for item in recently_played['items']]
    track_names = [item['track']['name'] for item in recently_played['items']]
    df = pd.DataFrame({'played_at': pd.to_datetime(timestamps), 'track_name': track_names})
    df['hour'] = df['played_at'].dt.hour

    fig, ax = plt.subplots(figsize = (8, 6), dpi = 100)

    sns.barplot(
        x = df['hour'].value_counts().sort_index().index,
        y = df['hour'].value_counts().sort_index().values,
        hue = df['hour'].value_counts().sort_index().index,
        palette = "Greens_d",
        ax = ax,
        legend = False,
    )

    ax.set_title("Listening habits by hour", fontsize = 16, weight = "bold")
    ax.set_xlabel("Hour of day", fontsize = 12)
    ax.set_ylabel("Number of songs played", fontsize = 12)
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
    st.markdown(html_code, unsafe_allow_html=True)

    # Additional Insight: Message based on the most listened hour
    peak_hour = df['hour'].value_counts().idxmax()

    if 0 <= peak_hour < 6:
        message = f"🌙 You're a **night owl**! You’re most active late at night, when the world is quiet and your tunes take center stage. Keep rocking those midnight jams!"
    elif 6 <= peak_hour < 12:
        message = f"🌇 You're an **early bird**! You start your day with energy, and your tunes help set the tone for a great morning. Keep those morning jams alive!"
    elif 12 <= peak_hour < 18:
        message = f"🌞 **Afternoon vibes** are your sweet spot! You're at your peak energy, grooving to the rhythm of the day. Keep riding that midday wave!"
    else:
        message = f"🌆 Looks like you’re a **sunset person**! When the sun sets, your playlist shines. You’ve got the evening vibes on lock."

    st.markdown("\n")
    st.markdown(message)

except Exception as e:
    st.error("Could not fetch recently played tracks. Please ensure you're logged in to Spotify and have granted the necessary permissions.")
    st.error(f"Error: {e}")
