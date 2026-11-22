"""Convert the raw Google Forms export into the de-identified analysis file.

Input : data/raw/survey_raw_google_forms.csv  (Russian headers, git-ignored)
Output: data/survey/survey_clean.csv          (English schema, no timestamps)

Steps: keep only respondents who gave consent, drop the timestamp, assign
anonymous identifiers S01..Snn, translate categorical answers, and split the
multi-select barrier question into a ';'-separated list of canonical labels.
"""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "survey_raw_google_forms.csv"
OUT_FILE = PROJECT_ROOT / "data" / "survey" / "survey_clean.csv"

# Header fragments (Russian) -> English column names.
HEADER_KEYS = {
    "Согласие": "consent",
    "Курс": "study_year",
    "Основное направление": "track",
    "профессиональный опыт": "professional_experience",
    "проектов": "academic_projects",
    "стажировку": "internship",
    "технических навыков": "technical_skills",
    "коммуникативных навыков": "communication_skills",
    "откликов": "applications_sent",
    "приглашению на собеседование": "interview_invitations",
    "офферов": "job_offers",
    "Работаете ли вы сейчас": "working_in_it",
    "Насколько трудно": "perceived_difficulty",
    "мешает больше всего": "barriers",
}

YES_NO = {"Да": "yes", "Нет": "no"}
TRACK = {
    "Другое IT-направление": "Other IT",
    "Кибербезопасность": "Cybersecurity",
    "Данные / ИИ": "Data / AI",
    "Сети и инфраструктура": "Networks and infrastructure",
    "Разработка ПО": "Software development",
}
WORKING = {
    "Нет, но ищу": "no_searching",
    "Нет, не ищу": "no_not_searching",
    "Да, частичная занятость / стажировка": "yes_part_time_or_internship",
}
BARRIERS = {
    "Нет профессионального опыта": "No professional experience",
    "Недостаточно технических навыков": "Insufficient technical skills",
    "Недостаточно коммуникативных навыков": "Insufficient communication skills",
    "Нет портфолио / проектов": "No portfolio / projects",
    "Нет ответа от работодателей": "No response from employers",
    "Мало подходящих вакансий": "Few suitable vacancies",
    "Языковой барьер": "Language barrier",
}


def rename_columns(raw: pd.DataFrame) -> pd.DataFrame:
    mapping = {}
    for column in raw.columns:
        for key, name in HEADER_KEYS.items():
            if key in column and name not in mapping.values():
                mapping[column] = name
                break
    missing = set(HEADER_KEYS.values()) - set(mapping.values())
    if missing:
        raise ValueError(f"Survey columns not recognised: {sorted(missing)}")
    return raw.rename(columns=mapping)[list(HEADER_KEYS.values())]


def translate(series: pd.Series, mapping: dict, name: str) -> pd.Series:
    unknown = set(series.dropna().str.strip()) - set(mapping)
    if unknown:
        raise ValueError(f"Unknown values in '{name}': {sorted(unknown)}")
    return series.str.strip().map(mapping)


def main() -> None:
    raw = pd.read_csv(RAW_FILE)
    data = rename_columns(raw)

    consented = data["consent"].str.startswith("Да")
    data = data.loc[consented].drop(columns="consent").reset_index(drop=True)

    data["study_year"] = (
        data["study_year"].str.extract(r"(\d)")[0].astype(int)
    )
    data["track"] = translate(data["track"], TRACK, "track")
    for column in ("professional_experience", "internship"):
        data[column] = translate(data[column], YES_NO, column)
    data["working_in_it"] = translate(
        data["working_in_it"], WORKING, "working_in_it"
    )
    data["barriers"] = data["barriers"].map(
        lambda cell: ";".join(
            BARRIERS[item.strip()] for item in str(cell).split(";")
        )
    )

    numeric = [
        "academic_projects", "technical_skills", "communication_skills",
        "applications_sent", "interview_invitations", "job_offers",
        "perceived_difficulty",
    ]
    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="raise")

    data.insert(0, "student_id", [f"S{i + 1:02d}" for i in range(len(data))])

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUT_FILE, index=False)

    print("Survey preparation completed successfully.")
    print(f"Raw responses: {len(raw)}; with consent: {len(data)}")
    print(f"Output saved to: {OUT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
