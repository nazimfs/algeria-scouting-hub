from pprint import pprint

from app.connectors.wikipedia.client import WikipediaClient
from app.connectors.wikipedia.parser import WikipediaParser
from app.services.eligibility_analyzer import EligibilityAnalyzer


def main() -> None:
    client = WikipediaClient()
    parser = WikipediaParser()
    analyzer = EligibilityAnalyzer()

    html = client.fetch_player_page("Maghnes Akliouche")
    wikipedia_data = parser.parse(html)

    result = analyzer.analyze(wikipedia_data)

    pprint(result)


if __name__ == "__main__":
    main()