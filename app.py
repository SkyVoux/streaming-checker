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

# Define countries to scan
countries = {
    'US': '🇺🇸', 'FR': '🇫🇷', 'BR': '🇧🇷', 'DE': '🇩🇪', 'GB': '🇬🇧', 'CA': '🇨🇦', 'AU': '🇦🇺',
    'JP': '🇯🇵', 'IN': '🇮🇳', 'IT': '🇮🇹', 'ES': '🇪🇸', 'NL': '🇳🇱', 'MX': '🇲🇽', 'AR': '🇦🇷',
    'BE': '🇧🇪', 'CH': '🇨🇭', 'SE': '🇸🇪', 'DK': '🇩🇰', 'FI': '🇫🇮', 'NO': '🇳🇴', 'IE': '🇮🇪',
    'NZ': '🇳🇿', 'KR': '🇰🇷', 'ZA': '🇿🇦', 'RU': '🇷🇺', 'CN': '🇨🇳', 'PL': '🇵🇱', 'PT': '🇵🇹',
    'CL': '🇨🇱', 'CO': '🇨🇴', 'PE': '🇵🇪', 'TR': '🇹🇷', 'GR': '🇬🇷', 'AT': '🇦🇹', 'CZ': '🇨🇿',
    'HU': '🇭🇺', 'SG': '🇸🇬', 'HK': '🇭🇰', 'MY': '🇲🇾', 'TH': '🇹🇭', 'PH': '🇵🇭', 'ID': '🇮🇩',
    'AE': '🇦🇪', 'SA': '🇸🇦', 'IL': '🇮🇱'
}

def get_all_providers():
    url = f"https://api.themoviedb.org/3/watch/providers/movie?api_key={TMDB_API_KEY}&language=en-US"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return sorted(set(p['provider_name'] for p in data['results']))

all_platforms = get_all_providers()

# Streamlit UI
st.title("🌍 Movie Availability by Platform (Powered by TMDb)")
query = st.text_input("Enter a movie title:")

selected_platforms = st.multiselect(
    "Filter by platform (optional):", options=all_platforms, default=[]
)

if query:
    # Step 1: Search for the movie
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    res = requests.get(search_url)
    results = res.json().get("results", [])

    if not results:
        st.error("Movie not found.")
    else:
        movie = results[0]
        movie_id = movie["id"]
        title = movie["title"]
        release_year = movie.get("release_date", "")[:4]  # Get year only
        
        st.subheader(f"🎬 {title} ({release_year})")

        # Step 2: Get watch providers per country
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
        providers_data = requests.get(url).json().get("results", {})

        # Step 3: Aggregate by provider
        platform_map = {}
        for country_code, emoji in countries.items():
            country_providers = providers_data.get(country_code, {})
            flatrate = country_providers.get("flatrate", [])
            for p in flatrate:
                name = p['provider_name']
                if selected_platforms and name not in selected_platforms:
                    continue  # skip if filtered out
                if name not in platform_map:
                    platform_map[name] = []
                platform_map[name].append(emoji)
    
        if not platform_map:
            st.info("No streaming availability found in selected countries.")
        else:
            st.markdown("📡 **Streaming Platforms:**")
            for platform, flags in sorted(platform_map.items()):
                st.markdown(f"- **{platform}**: {' '.join(flags)}")
                