import streamlit as st
import requests

API_KEY = "acd076a8-b019-4744-b9af-247a8b62014b"
PLAYER_NICKNAMES = ["MeLLon_", "Malkoc02", "nyousz", "PaLaCs2", "0reily", "ctVandaL", "IRubisco", "KhalEgo"]

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_last_matches_result(nickname, game="cs2"):
    # Oyuncu ID'sini al
    player_url = f"https://open.faceit.com/data/v4/players?nickname={nickname}"
    player_resp = requests.get(player_url, headers=headers)
    if player_resp.status_code != 200:
        return None

    player_data = player_resp.json()
    player_id = player_data.get("player_id")
    if not player_id:
        return None

    # Son 5 maç listesini al
    matches_url = f"https://open.faceit.com/data/v4/players/{player_id}/history?game={game}&limit=5"
    matches_resp = requests.get(matches_url, headers=headers)
    if matches_resp.status_code != 200:
        return None

    matches = matches_resp.json().get("items", [])
    wins = 0
    total = 0

    for match in matches:
        match_id = match.get("match_id")
        if not match_id:
            continue

        stats_url = f"https://open.faceit.com/data/v4/matches/{match_id}/stats"
        stats_resp = requests.get(stats_url, headers=headers)
        if stats_resp.status_code != 200:
            continue

        try:
            rounds = stats_resp.json()["rounds"]
            for team in rounds[0]["teams"]:
                for player in team["players"]:
                    if player["player_id"] == player_id:
                        result = player.get("player_stats", {}).get("Result")
                        if result == "1":
                            wins += 1
                        total += 1
                        raise StopIteration  # break all loops
        except StopIteration:
            continue
        except Exception:
            continue

    return f"{wins}/{total}" if total > 0 else "Yok"



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
        result = get_last_matches_result(nickname)

        elo_list.append({
            "Oyuncu": nickname,
            "ELO": elo if elo is not None else "Bilinmiyor",
            "Son 5 Maç (W/L)": result if result is not None else "Bilinmiyor"
        })

    elo_list = sorted(elo_list, key=lambda x: (x["ELO"] if isinstance(x["ELO"], int) else -1), reverse=True)

    st.subheader("ELO Sıralaması")
    st.table(elo_list)