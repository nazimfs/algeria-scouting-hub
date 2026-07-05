from app.connectors.transfermarkt.client import TransfermarktClient


def main() -> None:
    url = "https://www.transfermarkt.fr/rayan-cherki/profil/spieler/607223"

    client = TransfermarktClient()
    html = client.fetch_player_page(url)

    print(f"HTML length: {len(html)}")
    print(html[:500])


if __name__ == "__main__":
    main()