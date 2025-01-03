import pytest


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Adriana, Captain of the Guard", ("Adriana, Captain of the Guard", "DMC", "139")),
        ("Chain Reaction", ("Chain Reaction", "scd", "126")),
        ("Boros Signet", ("Boros Signet", "rvr", "251")),
        ("Korvold, Fae-Cursed King", ("Korvold, Fae-Cursed King", "pl24", "6")),
        ("Finale of Glory", ("Finale of Glory", "war", "12")),
        ("Boros Charm", ("Boros Charm", "otc", "216")),
        ("Commander's Sphere", ("Commander's Sphere", "cmm", "377")),
        ("Dragonmaster Outcast", ("Dragonmaster Outcast", "scd", "136")),
        ("Mentor of the Meek", ("Mentor of the Meek", "ltc", "173")),
    ],
)
def test_recommond_print(name: str, expected):
    from pathlib import Path

    import sbwsz

    sbwsz.set_cache_path(Path(__file__).parent.parent / ".cache")
    card = sbwsz.recommend_print(card_name=name)
    print(card)
    assert card["card_name"] == expected[0]
    assert card["card_set"].lower() == expected[1].lower()
    assert card["collector_number"] == expected[2]
