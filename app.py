#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 20:04:47 2025

@author: victor
"""

import requests
import streamlit as st

# 👉 Replace with your TMDb API Key
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

# 🌍 Countries to check
countries = {
    "US": {"flag": "🇺🇸", "name": "United States"},
    "FR": {"flag": "🇫🇷", "name": "France"},
    "BR": {"flag": "🇧🇷", "name": "Brazil"},
    "DE": {"flag": "🇩🇪", "name": "Germany"},
    "GB": {"flag": "🇬🇧", "name": "United Kingdom"},
    "CA": {"flag": "🇨🇦", "name": "Canada"},
    "AU": {"flag": "🇦🇺", "name": "Australia"},
    "JP": {"flag": "🇯🇵", "name": "Japan"},
    "IN": {"flag": "🇮🇳", "name": "India"},
    "IT": {"flag": "🇮🇹", "name": "Italy"},
    "ES": {"flag": "🇪🇸", "name": "Spain"},
    "NL": {"flag": "🇳🇱", "name": "Netherlands"},
    "MX": {"flag": "🇲🇽", "name": "Mexico"},
    "AR": {"flag": "🇦🇷", "name": "Argentina"},
    "BE": {"flag": "🇧🇪", "name": "Belgium"},
    "CH": {"flag": "🇨🇭", "name": "Switzerland"},
    "SE": {"flag": "🇸🇪", "name": "Sweden"},
    "DK": {"flag": "🇩🇰", "name": "Denmark"},
    "FI": {"flag": "🇫🇮", "name": "Finland"},
    "NO": {"flag": "🇳🇴", "name": "Norway"},
    "IE": {"flag": "🇮🇪", "name": "Ireland"},
    "NZ": {"flag": "🇳🇿", "name": "New Zealand"},
    "KR": {"flag": "🇰🇷", "name": "South Korea"},
    "ZA": {"flag": "🇿🇦", "name": "South Africa"},
    "PL": {"flag": "🇵🇱", "name": "Poland"},
    "PT": {"flag": "🇵🇹", "name": "Portugal"},
    "CL": {"flag": "🇨🇱", "name": "Chile"},
    "CO": {"flag": "🇨🇴", "name": "Colombia"},
    "TR": {"flag": "🇹🇷", "name": "Turkey"},
    "GR": {"flag": "🇬🇷", "name": "Greece"},
    "AT": {"flag": "🇦🇹", "name": "Austria"},
    "CZ": {"flag": "🇨🇿", "name": "Czech Republic"},
    "HU": {"flag": "🇭🇺", "name": "Hungary"},
    "SG": {"flag": "🇸🇬", "name": "Singapore"},
    "HK": {"flag": "🇭🇰", "name": "Hong Kong"},
    "MY": {"flag": "🇲🇾", "name": "Malaysia"},
    "TH": {"flag": "🇹🇭", "name": "Thailand"},
    "PH": {"flag": "🇵🇭", "name": "Philippines"},
    "ID": {"flag": "🇮🇩", "name": "Indonesia"},
    "AE": {"flag": "🇦🇪", "name": "United Arab Emirates"},
    "SA": {"flag": "🇸🇦", "name": "Saudi Arabia"},
    "IL": {"flag": "🇮🇱", "name": "Israel"},
}

# ---------- API helpers ----------

@st.cache_data
def get_all_providers(media_type: str):
    url = f"https://api.themoviedb.org/3/watch/providers/{media_type}?api_key={TMDB_API_KEY}&language=en-US"
    res = requests.get(url, timeout=20)
    res.raise_for_status()
    data = res.json()
    return sorted(set(p["provider_name"] for p in data.get("results", [])))


def search_titles(query: str, media_type: str):
    url = f"https://api.themoviedb.org/3/search/{media_type}"
    params = {"api_key": TMDB_API_KEY, "query": query}
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json().get("results", [])


def get_watch_providers(title_id: int, media_type: str):
    url = f"https://api.themoviedb.org/3/{media_type}/{title_id}/watch/providers"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json().get("results", {})


def get_tv_details(tv_id: int):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json()


def get_season_details(tv_id: int, season_number: int):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json()


def get_season_watch_providers(tv_id: int, season_number: int):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/watch/providers"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params, timeout=20)
    res.raise_for_status()
    return res.json().get("results", {})

# ---------- UI helpers ----------

def inject_flag_styles():
    st.html("""
    <style>
    .flag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 6px;
        margin-bottom: 6px;
    }

    .flag-chip {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        line-height: 1;
        cursor: default;
        user-select: none;
        padding: 2px 4px;
        border-radius: 8px;
        background: rgba(255,255,255,0.04);
    }

    .flag-chip .tooltiptext {
        visibility: hidden;
        opacity: 0;
        transition: opacity 0.15s ease;
        position: absolute;
        bottom: 135%;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        background: rgba(25,25,25,0.95);
        color: white;
        text-align: center;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.80rem;
        z-index: 9999;
        pointer-events: none;
    }

    .flag-chip:hover .tooltiptext,
    .flag-chip:active .tooltiptext,
    .flag-chip:focus .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """)


def render_country_flags(country_codes):
    parts = ['<div class="flag-row">']
    for code in country_codes:
        flag = countries[code]["flag"]
        name = countries[code]["name"]
        parts.append(
            f"""
            <span class="flag-chip" tabindex="0" aria-label="{name}">
                {flag}
                <span class="tooltiptext">{name}</span>
            </span>
            """
        )
    parts.append("</div>")
    st.html("".join(parts))


def build_platform_map(providers_data, selected_platforms):
    platform_map = {}

    for country_code in countries.keys():
        country_info = providers_data.get(country_code, {})
        flatrate = country_info.get("flatrate", [])

        for provider in flatrate:
            provider_name = provider["provider_name"]

            if selected_platforms and provider_name not in selected_platforms:
                continue

            if provider_name not in platform_map:
                platform_map[provider_name] = []

            platform_map[provider_name].append(country_code)

    return platform_map

# ---------- App ----------

st.set_page_config(page_title="Streaming Availability", layout="centered")
inject_flag_styles()

st.title("🌍 Streaming Check")

media_choice = st.segmented_control(
    "Choose type:",
    options=["Movie", "TV Show"],
    default="Movie",
)

media_type = "movie" if media_choice == "Movie" else "tv"

query = st.text_input(f"Enter a {media_choice.lower()} title:")

if query:
    results = search_titles(query, media_type)

    if not results:
        st.warning("No results found.")
    else:
        def option_label(item):
            if media_type == "movie":
                title = item.get("title", "Unknown title")
                year = item.get("release_date", "")[:4]
            else:
                title = item.get("name", "Unknown title")
                year = item.get("first_air_date", "")[:4]
            return f"{title} ({year})" if year else title

        options = [option_label(item) for item in results]
        selected_option = st.selectbox("Select the correct result:", options=options)
        selected_item = results[options.index(selected_option)]

        title_id = selected_item["id"]

        if media_type == "movie":
            title = selected_item.get("title", "Unknown title")
            year = selected_item.get("release_date", "")[:4]
        else:
            title = selected_item.get("name", "Unknown title")
            year = selected_item.get("first_air_date", "")[:4]

        poster_path = selected_item.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            st.image(poster_url, width=250)

        st.subheader(f"🎬 {title} ({year})" if year else f"🎬 {title}")

        all_platforms = get_all_providers(media_type)
        selected_platforms = st.multiselect(
            "Filter by platform (optional):",
            options=all_platforms,
            default=[],
        )

        providers_data = {}
        scope_label = ""

        # ---------- Movie logic ----------
        if media_type == "movie":
            providers_data = get_watch_providers(title_id, media_type)
            scope_label = "Movie availability"

        # ---------- TV logic ----------
        else:
            tv_details = get_tv_details(title_id)
            seasons = tv_details.get("seasons", [])

            availability_scope = st.radio(
                "Availability scope:",
                ["Whole show", "Specific season"],
                horizontal=True
            )

            if availability_scope == "Whole show":
                providers_data = get_watch_providers(title_id, "tv")
                scope_label = "TV show availability"

            else:
                valid_seasons = [
                    s for s in seasons
                    if s.get("season_number", 0) > 0
                ]

                if valid_seasons:
                    season_options = [
                        f"Season {s['season_number']}" for s in valid_seasons
                    ]

                    selected_season_label = st.selectbox(
                        "Select a season:",
                        options=season_options
                    )

                    selected_season_number = int(selected_season_label.replace("Season ", ""))

                    # Episode selector for info only
                    season_details = get_season_details(title_id, selected_season_number)
                    episodes = season_details.get("episodes", [])

                    if episodes:
                        episode_options = [
                            f"Episode {ep.get('episode_number')} - {ep.get('name', 'Unknown episode')}"
                            for ep in episodes
                        ]

                        st.selectbox(
                            "Select an episode (info only):",
                            options=episode_options
                        )

                        st.caption(
                            "Episode-level streaming availability is not provided by TMDb. "
                            "Results below are shown at the season level."
                        )

                    providers_data = get_season_watch_providers(title_id, selected_season_number)
                    scope_label = f"Season {selected_season_number} availability"
                else:
                    st.info("No selectable seasons found for this TV show.")
                    providers_data = {}
                    scope_label = "TV show availability"

        if scope_label:
            st.caption(scope_label)

        platform_map = build_platform_map(providers_data, selected_platforms)

        if platform_map:
            st.markdown("### 📡 Streaming Platforms")

            for platform, country_codes in sorted(platform_map.items()):
                st.markdown(f"**{platform}**")
                render_country_flags(sorted(country_codes))

                with st.popover(f"See country names for {platform}"):
                    for code in sorted(country_codes):
                        st.write(f'{countries[code]["flag"]} {countries[code]["name"]}')
        else:
            st.info("No streaming availability found in the selected countries/platforms.")

st.markdown(
    """
    ---
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Powered by <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a> 🎬
    </div>
    """,
    unsafe_allow_html=True
)
