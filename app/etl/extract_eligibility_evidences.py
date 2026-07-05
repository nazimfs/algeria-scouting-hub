from app.services.eligibility_evidence_service import EligibilityEvidenceService


def main() -> None:
    service = EligibilityEvidenceService()
    inserted_count = service.extract_from_raw_ingestions()

    print(f"✅ Eligibility evidences inserted: {inserted_count}")


if __name__ == "__main__":
    main()