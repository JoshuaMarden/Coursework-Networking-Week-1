def reverse_words(text: str) -> str:
    str_as_list = list(text)

    str_as_list.append(" ")

    word_found = False

    for index, character in enumerate(str_as_list):
        if character != " " and not word_found:
            word_found = True
            start_index = index
        elif character == " " and word_found:
            end_index = index
            segment = str_as_list[start_index:end_index]
            segment = segment[::-1]
            str_as_list[start_index:end_index] = segment
            word_found = False

    str_as_list.pop()
    string_with_words_reversed = ''.join(str_as_list)
    return string_with_words_reversed


if __name__ == "__main__":
    test_string = "ehT kciuq nworb xof spmuj revo eht yzal .god"
    print(reverse_words(test_string))
