from tools.reg_search import normalize_word, tokenize, search_regulations


def test_singular_and_plural_give_same_token():
    assert tokenize("discharge") == tokenize("discharges")


def test_normalize_word_cases():
    assert normalize_word("processes") == "process"
    assert normalize_word("gases") == "gas"
    assert normalize_word("industries") == "industry"
    assert normalize_word("emissions") == "emission"
    assert normalize_word("status") == "status"


def test_empty_query_returns_nothing():
    assert search_regulations("") == []
    assert search_regulations("   ") == []


def test_results_are_sorted_by_score():
    results = search_regulations("water discharge effluent consent", top_k=10)
    scores = [r["score"] for r in results]
    assert results
    assert scores == sorted(scores, reverse=True)


def test_water_query_returns_water_act_first():
    results = search_regulations("water discharge effluent consent", top_k=5)
    assert results[0]["source"] == "water_act_1974.md"


def test_all_four_eia_stages_are_retrievable():
    results = search_regulations(
        "environmental clearance screening scoping consultation appraisal",
        top_k=10,
    )
    combined = " ".join(r["text"] for r in results)
    for stage in ["Screening", "Scoping", "Public Consultation", "Appraisal"]:
        assert stage in combined