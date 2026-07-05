from bs4 import BeautifulSoup


class WikipediaValidator:
    def validate(self, html: str) -> bool:
        if not html:
            return False

        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1")
        if title is None:
            return False

        content = soup.find("div", id="mw-content-text")
        if content is None:
            return False

        return True