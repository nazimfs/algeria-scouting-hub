from bs4 import BeautifulSoup


class WikipediaParser:
    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        return {
            "player_name": self._extract_title(soup),
            "lead": self._extract_lead(soup),
            "infobox": self._extract_infobox(soup),
            "sections": self._extract_sections(soup),
        }

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find("h1")
        return title.get_text(" ", strip=True) if title else None

    def _extract_lead(self, soup: BeautifulSoup) -> str | None:
        content = soup.find("div", id="mw-content-text")

        if content is None:
            return None

        lead_parts = []

        for child in content.children:
            if getattr(child, "name", None) == "section":
                break

            if getattr(child, "name", None) == "p":
                text = child.get_text(" ", strip=True)
                if text:
                    lead_parts.append(text)

        return "\n".join(lead_parts) if lead_parts else None

    def _extract_infobox(self, soup: BeautifulSoup) -> dict:
        infobox = soup.find("table", class_="infobox")

        if infobox is None:
            return {}

        data = {}

        for row in infobox.find_all("tr"):
            header = row.find("th")
            value = row.find("td")

            if header and value:
                key = header.get_text(" ", strip=True)
                val = value.get_text(" ", strip=True)
                data[key] = val

        return data

    def _extract_sections(self, soup: BeautifulSoup) -> dict:
        sections = {}

        for section in soup.find_all("section"):
            heading = section.find(["h2", "h3"])

            if heading is None:
                continue

            title = heading.get_text(" ", strip=True)

            content = []

            for paragraph in section.find_all("p"):
                text = paragraph.get_text(" ", strip=True)

                if text:
                    content.append(text)

            if content:
                sections[title] = "\n".join(content)

        return sections