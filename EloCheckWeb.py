import streamlit as st
import requests

API_KEY = "acd076a8-b019-4744-b9af-247a8b62014b"
PLAYER_NICKNAMES = ["MeLLon_", "Malkoc02", "nyousz", "PaLaCs2", "0reily", "ctVandaL", "IRubisco", "KhalEgo"]

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_player_elo(nickname):
    url = f"https://open.faceit.com/data/v4/players?nickname={nickname}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    try:
        games_data = data["games"]
        if "cs2" in games_data:
            return games_data["cs2"]["faceit_elo"]
        elif "csgo" in games_data:
            return games_data["csgo"]["faceit_elo"]
    except KeyError:
        return None
    return None

st.title("🎮 Faceit ELO Sıralayıcı")

if st.button("ELO'ları Getir"):
    elo_list = []
    for nickname in PLAYER_NICKNAMES:
        elo = get_player_elo(nickname)
        elo_list.append({
            "Oyuncu": nickname,
            "ELO": elo if elo is not None else "Bilinmiyor"
        })

    elo_list = sorted(elo_list, key=lambda x: (x["ELO"] if isinstance(x["ELO"], int) else -1), reverse=True)
    st.table(elo_list)
