def duplicate_count(text: str) -> int:

    str_as_list = list(text)
    checked_characters = []
    duplicate_already_recorded = []
    repeats = 0

    for character in str_as_list:

        character = character.lower()

        if character not in checked_characters and\
                character not in duplicate_already_recorded:
            checked_characters.append(character)
        else:
            repeats += 1
            duplicate_already_recorded.append(character)

    return repeats


if __name__ == "__main__":

    print(duplicate_count("ABBCCC"))
