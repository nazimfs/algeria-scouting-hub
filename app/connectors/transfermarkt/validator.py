from bs4 import BeautifulSoup


class TransfermarktValidator:
    def validate(self, html: str) -> bool:
        if not html:
            return False

        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1")
        if title is None:
            return False

        profile_header = soup.find("header", class_="data-header")
        if profile_header is None:
            return False

        return True