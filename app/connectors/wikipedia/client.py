import requests


class WikipediaClient:

    #  BASE_URL = "https://en.wikipedia.org/wiki/"
    BASE_URL = "https://fr.wikipedia.org/wiki/"


    def fetch_player_page(self, player_name: str) -> str:

        player_name = player_name.replace(" ", "_")

        url = self.BASE_URL + player_name

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "AlgeriaScoutingHub/1.0"
            }
        )

        response.raise_for_status()

        return response.text