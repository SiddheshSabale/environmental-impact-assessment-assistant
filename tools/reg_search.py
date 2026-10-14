from pathlib import Path
import re

REGULATIONS_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "regulations"
)

STOP_WORDS = {
    "a", "an", "and", "are", "for", "in", "is", "of",
    "on", "or", "the", "to", "with", "near", "project"
}

SYNONYMS = {
    "solar": {"solar", "photovoltaic", "renewable", "electricity"},
    "farm": {"farm", "plant", "facility", "project"},
    "clearing": {"clearing", "clearance", "vegetation", "land"},
    "water": {"water", "runoff", "groundwater", "surface"},
    "air": {"air", "dust", "emission", "pollution"},
    "waste": {"waste", "disposal", "recycling", "hazardous"},
    "biodiversity": {"biodiversity", "ecology", "habitat", "wildlife"},
}

# Plurals that the general rules below would get wrong.
IRREGULAR_PLURALS = {"gases": "gas"}


def normalize_word(word: str) -> str:
    """Reduce a plural word to its singular form so both forms match."""

    if word in IRREGULAR_PLURALS:
        return IRREGULAR_PLURALS[word]

    # industries -> industry
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"

    # processes -> process, classes -> class, boxes -> box,
    # branches -> branch, washes -> wash
    if len(word) > 4 and word.endswith(("sses", "xes", "ches", "shes")):
        return word[:-2]

    # discharges -> discharge, emissions -> emission, wastes -> waste.
    # Words ending in ss, us, is are left alone (process, status, analysis).
    if (
        len(word) > 3
        and word.endswith("s")
        and not word.endswith(("ss", "us", "is"))
    ):
        return word[:-1]

    return word


def tokenize(text: str) -> set[str]:
    """Convert text into normalized keyword tokens."""

    return {
        normalize_word(word)
        for word in re.findall(r"[a-z0-9]+", text.lower())
        if word not in STOP_WORDS
    }


def expand_terms(terms: set[str]) -> set[str]:
    """Expand normalized terms using the synonym dictionary."""

    expanded = set(terms)

    for term in terms:
        expanded.update(
            normalize_word(word)
            for word in SYNONYMS.get(term, set())
        )

    return expanded


def search_regulations(query: str, top_k: int = 10) -> list[dict]:
    """Search local regulation summaries using keyword relevance."""

    if not query or not query.strip():
        return []

    if not REGULATIONS_DIR.exists():
        return []

    query_terms = tokenize(query)
    expanded_terms = expand_terms(query_terms)

    if not expanded_terms:
        return []

    results = []
    normalized_query = " ".join(query.lower().split())

    for file_path in sorted(REGULATIONS_DIR.glob("*")):
        if file_path.suffix.lower() not in {".md", ".txt"}:
            continue

        try:
            lines = file_path.read_text(
                encoding="utf-8"
            ).splitlines()
        except OSError:
            continue

        for line_number, line in enumerate(lines, start=1):
            text = line.strip()

            if not text or text.startswith("#"):
                continue

            line_terms = tokenize(text)
            matched_terms = sorted(expanded_terms & line_terms)

            if not matched_terms:
                continue

            score = len(matched_terms)
            normalized_line = " ".join(text.lower().split())

            if (
                len(normalized_query) > 3
                and normalized_query in normalized_line
            ):
                score += 3

            results.append({
                "source": file_path.name,
                "line_number": line_number,
                "text": text,
                "matched_terms": matched_terms,
                "score": score,
            })

    results.sort(
        key=lambda item: (
            -item["score"],
            item["source"],
            item["line_number"],
        )
    )

    return results[:max(0, top_k)]