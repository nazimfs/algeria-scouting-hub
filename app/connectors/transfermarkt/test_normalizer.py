from app.connectors.transfermarkt.client import TransfermarktClient
from app.connectors.transfermarkt.parser import TransfermarktParser
from app.connectors.transfermarkt.validator import TransfermarktValidator
from app.services.transfermarkt_normalizer import TransfermarktNormalizer


def main() -> None:
    url = "https://www.transfermarkt.fr/rayan-cherki/profil/spieler/607223"

    client = TransfermarktClient()
    validator = TransfermarktValidator()
    parser = TransfermarktParser()
    normalizer = TransfermarktNormalizer()

    html = client.fetch_player_page(url)

    if not validator.validate(html):
        raise ValueError("Invalid Transfermarkt page")

    parsed_data = parser.parse(html)
    normalized_data = normalizer.normalize(parsed_data)

    print("RAW PARSED DATA:")
    print(parsed_data)

    print("\nNORMALIZED DATA:")
    print(normalized_data)


if __name__ == "__main__":
    main()