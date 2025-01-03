import pytest


@pytest.mark.parametrize(
    "id,n_faces",
    [
        ("76ac5b70-47db-4cdb-91e7-e5c18c42e516", 1),
        ("c470539a-9cc7-4175-8f7c-c982b6072b6d", 2),  # Modal double-faced
        ("c1f53d7a-9dad-46e8-b686-cd1362867445", 2),  # Transforming double-faced
        ("6ee6cd34-c117-4d7e-97d1-8f8464bfaac8", 1),  # Flip
    ],
)
def test_get_faces(id: str, n_faces: int):
    import scryfall

    card = scryfall.card_by_id()[id]
    faces = scryfall.get_faces(card)

    assert type(faces) is list
    assert len(faces) == n_faces
    for face in faces:
        assert "illustration_id" in face


@pytest.mark.parametrize(
    "name,expected_id",
    [
        ("Vedalken Aethermage", "496eb37d-5c8f-4dd7-a0a7-3ed1bd2210d6"),
        ("vedalken aethermage", "496eb37d-5c8f-4dd7-a0a7-3ed1bd2210d6"),
        ("vedalken Æthermage", "496eb37d-5c8f-4dd7-a0a7-3ed1bd2210d6"),
        ("vedalken æthermage", "496eb37d-5c8f-4dd7-a0a7-3ed1bd2210d6"),
    ],
)
def test_canonic_card_name(name: str, expected_id: str):
    import scryfall

    card = scryfall.get_card(name)

    assert card["id"] == expected_id


@pytest.mark.parametrize(
    "name,set,collector_number,lang,expected",
    [
        ("Korvold, Fae-Cursed King", "", "", "zhs", {"lang": "zhs", "id": "9eb6ec66-d467-458f-a5b8-0c7aa426ee52"}),
        ("Brave-Kin Duo", "", "", "zhs", {"lang": "en", "id": "b8dd4693-424d-4d6e-86cf-24401a23d6b1"}),
        (
            "Liliana, Dreadhorde General",
            "WAR",
            "",
            "zhs",
            {"lang": "zhs", "id": "05480a5a-3f2c-4420-9f8b-718efa532fa7"},
        ),
        ("Boros Signet", "", "", "zhs", {"lang": "zhs", "id": "d6f7f444-7101-472f-bc07-91d2c6bb72ec"}),
    ],
)
def test_get_cards_lang(name, set, collector_number, lang: str, expected):
    from pathlib import Path

    import sbwsz
    import scryfall

    scryfall.set_cache_path(Path(__file__).parent.parent / ".cache")
    scryfall.set_prefer_lang(lang)
    sbwsz.set_cache_path(Path(__file__).parent.parent / ".cache")
    cards = scryfall.get_cards(name=name, set=set, collector_number=collector_number)
    assert cards[0]["lang"] == expected["lang"]
    assert cards[0]["id"] == expected["id"]


@pytest.mark.parametrize(
    "name,lang,expected",
    [
        ("Korvold, Fae-Cursed King", "zhs", {"lang": "zhs", "id": "9eb6ec66-d467-458f-a5b8-0c7aa426ee52"}),
        ("Brave-Kin Duo", "zhs", {"lang": "en", "id": "b8dd4693-424d-4d6e-86cf-24401a23d6b1"}),
        (
            "Liliana, Dreadhorde General",
            "zhs",
            {"lang": "en", "id": "ba461127-2220-4274-81cb-423a1700c9eb"},
        ),
        ("Boros Signet", "zhs", {"lang": "zhs", "id": "d6f7f444-7101-472f-bc07-91d2c6bb72ec"}),
    ],
)
def test_recommend_print(name, lang: str, expected):
    from pathlib import Path

    import sbwsz
    import scryfall

    scryfall.set_cache_path(Path(__file__).parent.parent / ".cache")
    scryfall.set_prefer_lang(lang)
    sbwsz.set_cache_path(Path(__file__).parent.parent / ".cache")
    cards = scryfall.recommend_print(card_name=name)
    assert cards["lang"] == expected["lang"]
    assert cards["id"] == expected["id"]
