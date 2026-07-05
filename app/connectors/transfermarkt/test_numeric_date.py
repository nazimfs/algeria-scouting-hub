from app.services.transfermarkt_normalizer import TransfermarktNormalizer


def main() -> None:
    normalizer = TransfermarktNormalizer()

    parsed_data = {
        "player_name": "Amine Gouiri",
        "facts": {
            "Date of birth/Age: 16/02/2000 (26)": "16/02/2000 (26)",
            "Place of birth: Bourgoin-Jallieu": "Bourgoin-Jallieu",
            "Height: 1,80 m": "1,80 m",
            "Citizenship: Algeria": "Algeria",
            "Position: Centre-Forward": "Centre-Forward",
            "Current international: Algeria": "Algeria",
        },
    }

    normalized_data = normalizer.normalize(parsed_data)

    print(normalized_data)


if __name__ == "__main__":
    main()