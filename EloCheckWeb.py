import streamlit as st
import requests

API_KEY = "acd076a8-b019-4744-b9af-247a8b62014b"
PLAYER_NICKNAMES = ["MeLLon_", "Malkoc02", "nyousz", "PaLaCs2", "0reily", "ctVandaL", "IRubisco", "KhalEgo"]

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_player_data(nickname):
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

    # Son 5 maçın verilerini al
    matches_url = f"https://open.faceit.com/data/v4/players/{player_id}/history?game=cs2&limit=5"
    matches_response = requests.get(matches_url, headers=headers)

    win_rate = None
    if matches_response.status_code == 200:
        matches_data = matches_response.json()
        items = matches_data.get("items", [])

        if items:
            wins = 0
            total_matches = len(items)

            for match in items:
                # Oyuncunun hangi takımda olduğunu bul
                teams = match.get("teams", {})
                faction1 = teams.get("faction1", {})
                faction2 = teams.get("faction2", {})

                player_team = None
                if any(player["player_id"] == player_id for player in faction1.get("roster", [])):
                    player_team = "faction1"
                elif any(player["player_id"] == player_id for player in faction2.get("roster", [])):
                    player_team = "faction2"

                # Kazanan takımı kontrol et
                if player_team and match.get("results", {}).get("winner") == player_team:
                    wins += 1

            win_rate = round((wins / total_matches) * 100, 1) if total_matches > 0 else None

    return elo, win_rate

st.title("🎮 Faceit ELO Sıralayıcı")

if st.button("ELO'ları Getir"):
    elo_list = []

    # Progress bar ekle
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, nickname in enumerate(PLAYER_NICKNAMES):
        status_text.text(f'Oyuncu verisi alınıyor: {nickname}')
        progress_bar.progress((i + 1) / len(PLAYER_NICKNAMES))

        elo, win_rate = get_player_data(nickname)
        elo_list.append({
            "Oyuncu": nickname,
            "ELO": elo if elo is not None else "Bilinmiyor",
            "Son 5 Maç Win Rate (%)": win_rate if win_rate is not None else "Bilinmiyor"
        })

    # Progress bar'ı temizle
    progress_bar.empty()
    status_text.empty()

    # ELO'ya göre sırala
    elo_list = sorted(elo_list, key=lambda x: (x["ELO"] if isinstance(x["ELO"], int) else -1), reverse=True)

    st.subheader("ELO ve Win Rate Sıralaması")
    st.table(elo_list)
