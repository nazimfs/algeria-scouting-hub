from app.connectors.wikipedia.client import WikipediaClient


def main():
    players = [
        "Rayan Cherki",
        "Michael Olise",
        "Maghnes Akliouche",
        "Zineddine Belaïd"

    ]

    client = WikipediaClient()

    for player in players:
        print("=" * 50)
        print(player)

        html = client.fetch_player_page(player)

        print(f"Downloaded {len(html)} characters")

if __name__ == "__main__":
    main()