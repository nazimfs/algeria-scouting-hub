from datetime import date
from typing import Any


class TransfermarktNormalizer:
    MONTHS_FR = {
        "janv.": 1,
        "janvier": 1,
        "févr.": 2,
        "février": 2,
        "mars": 3,
        "avr.": 4,
        "avril": 4,
        "mai": 5,
        "juin": 6,
        "juil.": 7,
        "juillet": 7,
        "août": 8,
        "sept.": 9,
        "septembre": 9,
        "oct.": 10,
        "octobre": 10,
        "nov.": 11,
        "novembre": 11,
        "déc.": 12,
        "décembre": 12,
    }

    MONTHS_EN = {
        "jan": 1,
        "jan.": 1,
        "january": 1,
        "feb": 2,
        "feb.": 2,
        "february": 2,
        "mar": 3,
        "mar.": 3,
        "march": 3,
        "apr": 4,
        "apr.": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "jun.": 6,
        "june": 6,
        "jul": 7,
        "jul.": 7,
        "july": 7,
        "aug": 8,
        "aug.": 8,
        "august": 8,
        "sep": 9,
        "sep.": 9,
        "sept": 9,
        "sept.": 9,
        "september": 9,
        "oct": 10,
        "oct.": 10,
        "october": 10,
        "nov": 11,
        "nov.": 11,
        "november": 11,
        "dec": 12,
        "dec.": 12,
        "december": 12,
    }

    def normalize(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        facts = parsed_data.get("facts", {})

        return {
            "player_name": self._clean_player_name(
                parsed_data.get("player_name")
            ),
            "birth_date": self._extract_birth_date(facts),
            "birth_city": self._extract_by_label_prefixes(
                facts,
                [
                    "Lieu de naissance:",
                    "Place of birth:",
                ],
            ),
            "height_cm": self._extract_height_cm(facts),
            "main_position": self._extract_by_label_prefixes(
                facts,
                [
                    "Position:",
                ],
            ),
            "nationality": self._extract_by_label_prefixes(
                facts,
                [
                    "Nationalité:",
                    "Citizenship:",
                ],
            ),
            "current_national_team": self._extract_by_label_prefixes(
                facts,
                [
                    "Joueur international actuel:",
                    "Current international:",
                ],
            ),
        }

    def _clean_player_name(self, player_name: str | None) -> str | None:
        if player_name is None:
            return None

        parts = player_name.split(" ", 1)

        if parts and parts[0].startswith("#") and len(parts) > 1:
            return parts[1]

        return player_name

    def _extract_by_label_prefix(
        self,
        facts: dict[str, str],
        label_prefix: str,
    ) -> str | None:
        for label, value in facts.items():
            if label.startswith(label_prefix):
                return value

        return None

    def _extract_by_label_prefixes(
        self,
        facts: dict[str, str],
        label_prefixes: list[str],
    ) -> str | None:
        for label_prefix in label_prefixes:
            value = self._extract_by_label_prefix(
                facts=facts,
                label_prefix=label_prefix,
            )

            if value is not None:
                return value

        return None

    def _extract_birth_date(self, facts: dict[str, str]) -> str | None:
        birth_date_text = self._extract_by_label_prefixes(
            facts,
            [
                "Naissance (âge):",
                "Date of birth/Age:",
                "Date of birth:",
            ],
        )

        if birth_date_text is None:
            return None

        date_part = birth_date_text.split("(")[0].strip()

        return self._parse_date(date_part)

    def _parse_date(self, value: str) -> str | None:
        numeric_date = self._parse_numeric_date(value)

        if numeric_date is not None:
            return numeric_date

        french_date = self._parse_french_date(value)

        if french_date is not None:
            return french_date

        return self._parse_english_date(value)

    def _parse_numeric_date(self, value: str) -> str | None:
        parts = value.strip().split("/")

        if len(parts) != 3:
            return None

        try:
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
        except ValueError:
            return None

        try:
            return date(year, month, day).isoformat()
        except ValueError:
            return None

    def _parse_french_date(self, value: str) -> str | None:
        parts = value.replace(",", "").split()

        if len(parts) != 3:
            return None

        try:
            day = int(parts[0])
            month = self.MONTHS_FR.get(parts[1].lower())
            year = int(parts[2])
        except ValueError:
            return None

        if month is None:
            return None

        try:
            return date(year, month, day).isoformat()
        except ValueError:
            return None

    def _parse_english_date(self, value: str) -> str | None:
        parts = value.replace(",", "").split()

        if len(parts) != 3:
            return None

        try:
            month = self.MONTHS_EN.get(parts[0].lower())
            day = int(parts[1])
            year = int(parts[2])
        except ValueError:
            return None

        if month is None:
            return None

        try:
            return date(year, month, day).isoformat()
        except ValueError:
            return None

    def _extract_height_cm(self, facts: dict[str, str]) -> int | None:
        height_text = self._extract_by_label_prefixes(
            facts,
            [
                "Taille:",
                "Height:",
            ],
        )

        if height_text is None:
            return None

        normalized = (
            height_text
            .replace(",", ".")
            .replace("m", "")
            .strip()
        )

        try:
            return int(float(normalized) * 100)
        except ValueError:
            return None