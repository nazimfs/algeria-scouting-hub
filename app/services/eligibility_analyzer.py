class EligibilityAnalyzer:
    FAMILY_KEYWORDS = [
        "famille",
        "biographie",
        "père",
        "mère",
        "parents",
        "grand-père",
        "grand-mère",
        "originaire",
        "origine",
        "d'origine",
        "né",
        "née",
        "naît",
        "enfance",
        "jeunesse",
        "vie personnelle",
    ]

    COUNTRY_KEYWORDS = [
        "algérie",
        "algérien",
        "algérienne",
        "biskra",
        "oran",
        "alger",
        "constantine",
        "kabylie",
    ]

    def analyze(self, wikipedia_data: dict) -> dict:
        texts_to_analyze = self._collect_candidate_texts(wikipedia_data)

        evidences = []

        for source_name, text in texts_to_analyze.items():
            if self._contains_family_signal(text) and self._contains_country_signal(text):
                evidences.append(
                    {
                        "source_section": source_name,
                        "evidence_type": "family_origin",
                        "target_country": "Algeria",
                        "confidence": "medium",
                        "text": text,
                    }
                )

        return {
            "player_name": wikipedia_data.get("player_name"),
            "source": "Wikipedia",
            "eligibility_country": "Algeria",
            "evidences": evidences,
            "has_potential_eligibility_signal": len(evidences) > 0,
        }

    def _collect_candidate_texts(self, wikipedia_data: dict) -> dict:
        candidates = {}

        lead = wikipedia_data.get("lead")
        if lead:
            candidates["lead"] = lead

        sections = wikipedia_data.get("sections", {})

        priority_section_keywords = [
            "famille",
            "enfance",
            "jeunesse",
            "vie personnelle",
            "origines",
            "formation",
        ]

        fallback_section_keywords = [
            "biographie",
        ]

        # 1. Chercher d'abord les sections précises
        for section_title, section_text in sections.items():
            title_lower = section_title.lower()

            if any(keyword in title_lower for keyword in priority_section_keywords):
                candidates[section_title] = section_text

        # 2. Si aucune section précise n'est trouvée, utiliser Biographie
        if not candidates:
            for section_title, section_text in sections.items():
                title_lower = section_title.lower()

                if any(keyword in title_lower for keyword in fallback_section_keywords):
                    candidates[section_title] = section_text

        return candidates

    def _contains_family_signal(self, text: str) -> bool:
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.FAMILY_KEYWORDS)

    def _contains_country_signal(self, text: str) -> bool:
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.COUNTRY_KEYWORDS)