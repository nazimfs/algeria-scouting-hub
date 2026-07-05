from app.connectors.transfermarkt.client import TransfermarktClient
from app.connectors.transfermarkt.parser import TransfermarktParser
from app.connectors.transfermarkt.validator import TransfermarktValidator


def main() -> None:
    url = "https://www.transfermarkt.fr/rayan-cherki/profil/spieler/607223"

    client = TransfermarktClient()
    validator = TransfermarktValidator()
    parser = TransfermarktParser()

    html = client.fetch_player_page(url)

    if not validator.validate(html):
        raise ValueError("Invalid Transfermarkt page")

    data = parser.parse(html)

    print(data)


if __name__ == "__main__":
    main()