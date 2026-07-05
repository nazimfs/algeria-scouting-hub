from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_engine
from app.database.models import Player, PlayerEligibilityEvidence, RawIngestion


def check_unlinked_eligibility_evidences(session: Session) -> int:
    statement = select(PlayerEligibilityEvidence).where(
        PlayerEligibilityEvidence.player_id.is_(None)
    )

    evidences = session.execute(statement).scalars().all()

    if not evidences:
        print("✅ All eligibility evidences are linked to players")
        return 0

    print("⚠️ Unlinked eligibility evidences found:")

    for evidence in evidences:
        print(
            f"- player_name={evidence.player_name} | "
            f"country={evidence.eligibility_country} | "
            f"source={evidence.source_name}"
        )

    return len(evidences)


def check_failed_raw_ingestions(session: Session) -> int:
    statement = select(RawIngestion).where(
        RawIngestion.payload["status"].astext == "failed"
    )

    failed_ingestions = session.execute(statement).scalars().all()

    if not failed_ingestions:
        print("✅ No failed raw ingestions")
        return 0

    print("⚠️ Failed raw ingestions found:")

    for ingestion in failed_ingestions:
        payload = ingestion.payload
        print(
            f"- entity_name={payload.get('entity_name')} | "
            f"source={payload.get('source')} | "
            f"error={payload.get('error')}"
        )

    return len(failed_ingestions)


def check_players_without_display_name(session: Session) -> int:
    statement = select(Player).where(
        Player.display_name.is_(None)
    )

    players = session.execute(statement).scalars().all()

    if not players:
        print("✅ All players have a display_name")
        return 0

    print("⚠️ Players without display_name found:")

    for player in players:
        print(f"- player_id={player.player_id}")

    return len(players)


def main() -> None:
    engine = get_engine()

    total_issues = 0

    with Session(engine) as session:
        print("=" * 60)
        print("DATA QUALITY CHECK")
        print("=" * 60)

        total_issues += check_unlinked_eligibility_evidences(session)
        total_issues += check_failed_raw_ingestions(session)
        total_issues += check_players_without_display_name(session)

    print("=" * 60)

    if total_issues == 0:
        print("✅ Data quality check passed")
    else:
        print(f"⚠️ Data quality check completed with {total_issues} issue(s)")


if __name__ == "__main__":
    main()