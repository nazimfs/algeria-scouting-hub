from bs4 import BeautifulSoup


class TransfermarktParser:
    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        return {
            "player_name": self._extract_player_name(soup),
            "facts": self._extract_facts(soup),
        }

    def _extract_player_name(self, soup: BeautifulSoup) -> str | None:
        title = soup.find("h1")

        if title is None:
            return None

        return title.get_text(" ", strip=True)

    def _extract_facts(self, soup: BeautifulSoup) -> dict:
        facts = {}

        fact_items = soup.find_all("li", class_="data-header__label")

        for item in fact_items:
            label = item.get_text(" ", strip=True)

            value = item.find_next("span", class_="data-header__content")

            if value is None:
                continue

            facts[label] = value.get_text(" ", strip=True)

        return facts