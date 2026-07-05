import requests


class TransfermarktClient:
    def fetch_player_page(self, url: str) -> str:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            },
        )

        response.raise_for_status()

        return response.text