from app.connectors.wikipedia.client import WikipediaClient
from app.connectors.wikipedia.parser import WikipediaParser


def main():
    players = [
       # "Rayan Cherki",
       # "Michael Olise",
        "Maghnes Akliouche"
    ]
    
    client = WikipediaClient()
    parser = WikipediaParser()
    for player in players:
        print("=" * 50)
        print(player)
        html = client.fetch_player_page(player)
        print("=" * 50)
        data = parser.parse(html)
        print("=" * 50)
        print(data)
        print("=" * 50)


    

   


if __name__ == "__main__":
    main()