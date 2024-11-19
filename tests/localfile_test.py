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
    ],
)
def test_recommend_print(card, expected):
    import localfile

    localfile.set_local_scan_path("/mnt/nasz/magic_cn/cards,/mnt/nasz/forge_cn1/Forge/Cache/pics/cards")

    card = localfile.recommend_print(card)
    if expected:
        assert "image_uris" in card
        assert not card["image_uris"]["png"].startswith("http")
