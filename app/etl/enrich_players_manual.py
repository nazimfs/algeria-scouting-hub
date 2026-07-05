from app.services.player_enrichment_service import PlayerEnrichmentService


PLAYER_ENRICHMENT_PAYLOADS = [
    {
        "display_name": "Rayan Cherki",
        "birth_date": "2003-08-17",
        "height_cm": 176,
        "preferred_foot": "both",
    },
    {
        "display_name": "Michael Olise",
        "birth_date": "2001-12-12",
        "height_cm": 184,
        "preferred_foot": "left",
    },
    {
        "display_name": "Maghnes Akliouche",
        "birth_date": "2002-02-25",
        "height_cm": 183,
        "preferred_foot": "left",
    },
]


def main() -> None:
    service = PlayerEnrichmentService()
    updated_count = service.enrich_players(PLAYER_ENRICHMENT_PAYLOADS)

    print(f"✅ Players enriched: {updated_count}")


if __name__ == "__main__":
    main()