from app.connectors.transfermarkt.client import TransfermarktClient
from app.connectors.transfermarkt.validator import TransfermarktValidator


def main() -> None:
    url = "https://www.transfermarkt.fr/rayan-cherki/profil/spieler/607223"

    client = TransfermarktClient()
    validator = TransfermarktValidator()

    html = client.fetch_player_page(url)

    is_valid = validator.validate(html)

    print(f"Is valid Transfermarkt page: {is_valid}")


if __name__ == "__main__":
    main()