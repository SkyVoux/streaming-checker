#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 20:04:47 2025

@author: victor
"""

import requests
import streamlit as st

# 👉 Replace with your TMDb API Key
TMDB_API_KEY = "e378b171f90b63371c1d4524cc5bf441"

# 🌍 Countries to check
countries = {
    'US': '🇺🇸', 'FR': '🇫🇷', 'BR': '🇧🇷', 'DE': '🇩🇪', 'GB': '🇬🇧', 'CA': '🇨🇦', 'AU': '🇦🇺',
    'JP': '🇯🇵', 'IN': '🇮🇳', 'IT': '🇮🇹', 'ES': '🇪🇸', 'NL': '🇳🇱', 'MX': '🇲🇽', 'AR': '🇦🇷',
    'BE': '🇧🇪', 'CH': '🇨🇭', 'SE': '🇸🇪', 'DK': '🇩🇰', 'FI': '🇫🇮', 'NO': '🇳🇴', 'IE': '🇮🇪',
    'NZ': '🇳🇿', 'KR': '🇰🇷', 'ZA': '🇿🇦', 'PL': '🇵🇱', 'PT': '🇵🇹', 'CL': '🇨🇱', 'CO': '🇨🇴',
    'TR': '🇹🇷', 'GR': '🇬🇷', 'AT': '🇦🇹', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'SG': '🇸🇬', 'HK': '🇭🇰',
    'MY': '🇲🇾', 'TH': '🇹🇭', 'PH': '🇵🇭', 'ID': '🇮🇩', 'AE': '🇦🇪', 'SA': '🇸🇦', 'IL': '🇮🇱'
}

# 📺 Get all streaming platforms for the dropdown
@st.cache_data
def get_all_providers():
    url = f"https://api.themoviedb.org/3/watch/providers/movie?api_key={TMDB_API_KEY}&language=en-US"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return sorted(set(p['provider_name'] for p in data['results']))

# 🌍 Search and select a movie
def search_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    res = requests.get(url)
    return res.json().get("results", [])

# 🎬 Get streaming providers for a movie
def get_watch_providers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
    res = requests.get(url)
    return res.json().get("results", {})

# UI start
st.set_page_config(page_title="Streaming Availability", layout="centered")
st.title("🌍 Stream Check")

# Step 1: Search query
query = st.text_input("Enter a movie title:")

if query:
    results = search_movies(query)

    if not results:
        st.warning("No results found.")
    else:
        # Step 2: Let user select from results
        options = [
            f"{m['title']} ({m.get('release_date', '')[:4]})" for m in results
        ]
        selected_index = st.selectbox("Select the correct movie:", options=options)
        selected_movie = results[options.index(selected_index)]

        movie_id = selected_movie["id"]
        title = selected_movie["title"]
        release_year = selected_movie.get("release_date", "")[:4]
        poster_path = selected_movie.get("poster_path")

        # Show poster
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            st.image(poster_url, width=250)

        st.subheader(f"🎬 {title} ({release_year})")

        # Step 3: Platform filter
        all_platforms = get_all_providers()
        selected_platforms = st.multiselect(
            "Filter by platform (optional):", options=all_platforms, default=[]
        )

        # Step 4: Check availability
        platform_map = {}
        providers_data = get_watch_providers(movie_id)

        for country_code, emoji in countries.items():
            country_info = providers_data.get(country_code, {})
            flatrate = country_info.get("flatrate", [])
            for p in flatrate:
                name = p["provider_name"]
                if selected_platforms and name not in selected_platforms:
                    continue
                if name not in platform_map:
                    platform_map[name] = []
                platform_map[name].append(emoji)

        if platform_map:
            st.markdown("📡 **Streaming Platforms:**")
            for platform, flags in sorted(platform_map.items()):
                st.markdown(f"- **{platform}**: {' '.join(flags)}")
        else:
            st.info("No streaming availability found in selected countries/platforms.")
            
            
st.markdown(
    """
    ---
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Powered by <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a> 🎬
    </div>
    """,
    unsafe_allow_html=True
)
