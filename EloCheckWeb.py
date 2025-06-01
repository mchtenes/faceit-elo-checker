import streamlit as st
import requests

API_KEY = "acd076a8-b019-4744-b9af-247a8b62014b"
PLAYER_NICKNAMES = ["MeLLon_", "Malkoc02", "nyousz", "PaLaCs2", "0reily", "ctVandaL", "IRubisco", "KhalEgo"]

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_player_elo(nickname):
    # Oyuncu bilgilerini al
    player_url = f"https://open.faceit.com/data/v4/players?nickname={nickname}"
    player_response = requests.get(player_url, headers=headers)

    if player_response.status_code != 200:
        return None, None

    player_data = player_response.json()
    player_id = player_data.get("player_id")

    # ELO bilgisini al
    elo = None
    try:
        games_data = player_data["games"]
        if "cs2" in games_data:
            elo = games_data["cs2"]["faceit_elo"]
        elif "csgo" in games_data:
            elo = games_data["csgo"]["faceit_elo"]
    except KeyError:
        pass

    return elo

st.title("🎮 Faceit ELO Sıralayıcı")

if st.button("ELO'ları Getir"):
    elo_list = []

    for nickname in PLAYER_NICKNAMES:
        elo = get_player_elo(nickname)

        elo_list.append({
            "Oyuncu": nickname,
            "ELO": elo if elo is not None else "Bilinmiyor",
        })

    elo_list = sorted(elo_list, key=lambda x: (x["ELO"] if isinstance(x["ELO"], int) else -1), reverse=True)

    st.subheader("ELO Sıralaması")
    st.table(elo_list)