from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "card,expected",
    [
        (
            {
                "name": "Air Servant",
                "set": "m14",
            },
            True,
        ),
        (
            {
                "name": "Air Servant",
                "set": "",
            },
            False,
        ),
        (
            {
                "name": "Air Servant",
                "set": "m20",
            },
            False,
        ),
        (
            {
                "name": "Angelic Guardian",
                "set": "m20",
            },
            True,
        ),
        (
            {
                "name": "Dragonlord's Servant",
                "set": "PL24",
            },
            True,
        ),
        (
            {
                "name": "Korvold, Fae-Cursed King",
                "set": "PL24",
            },
            True,
        ),
        (
            {
                "name": "Brave-Kin Duo",
                "set": "blb",
            },
            True,
        ),
        (
            {
                "name": "Zimone, Paradox Sculptor",
                "set": "fdn",
            },
            True,
        ),
    ],
)
def test_recommend_print(card, expected):
    import localfile
    from mtgproxies.decklists import Card

    localfile.set_local_scan_path("/mnt/nasz/magic_cn/cards,/mnt/nasz/forge_cn1/Forge/Cache/pics/cards")
    card = Card(1, card)
    card = localfile.recommend_print(card)
    if expected:
        assert card.proxy_local_scan


def test_parse_local_dir():
    import localfile

    dl, ok, warnings = localfile.parse_local_dir(Path(__file__).parent.parent / "examples")
    assert dl.name == "examples"
    assert len(dl.cards) == 4
    assert ok
    assert len(warnings) == 0
