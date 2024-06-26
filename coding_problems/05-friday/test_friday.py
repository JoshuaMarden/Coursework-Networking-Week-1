# pylint: skip-file

import pytest

from friday import cleaned_counts


def test_basic_test_1():
    assert cleaned_counts([2, 1, 2]) == [2, 2, 2]


def test_basic_test_2():
    assert cleaned_counts([4, 4, 4, 4]) == [4, 4, 4, 4]


def test_basic_test_3():
    assert cleaned_counts([1, 1, 2, 2, 1, 2, 2, 2, 2]) == [
        1, 1, 2, 2, 2, 2, 2, 2, 2]


def test_basic_test_4():
    assert cleaned_counts([5, 5, 6, 5, 5, 5, 5, 6]) == [5, 5, 6, 6, 6, 6, 6, 6]


def test_input_not_modified():
    input = [10, 11, 10]
    cleaned_counts(input)
    assert input == [10, 11, 10]


def test_zero_errors_1():
    assert cleaned_counts([4, 5, 6, 7]) == [4, 5, 6, 7]


def test_zero_errors_2():
    assert cleaned_counts([4, 4, 6, 7]) == [4, 4, 6, 7]


def test_zero_errors_3():
    assert cleaned_counts([4, 4, 5, 7]) == [4, 4, 5, 7]


def test_one_error_1():
    assert cleaned_counts([4, 3, 6, 7]) == [4, 4, 6, 7]


def test_one_error_2():
    assert cleaned_counts([4, 4, 6, 5]) == [4, 4, 6, 6]


def test_two_errors():
    assert cleaned_counts([1, 1, 2, 1, 2, 2, 3, 2]) == [1, 1, 2, 2, 2, 2, 3, 3]


def test_consecutive_errors_1():
    assert cleaned_counts([1, 1, 2, 2, 1, 1, 3, 3]) == [1, 1, 2, 2, 2, 2, 3, 3]


def test_consecutive_errors_2():
    assert cleaned_counts([2, 2, 2, 2, 1, 1, 1, 3]) == [2, 2, 2, 2, 2, 2, 2, 3]


@pytest.mark.parametrize("data,cleaned_data",
                         [([2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8], [2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8]),
                          ([3, 3, 3, 3, 3, 3, 3, 3, 2, 4, 3, 4, 4, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10], [
                           3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10]),
                             ([4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 6, 6, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 7, 9, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 10, 11, 11], [
                              4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11]),
                             ([4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 5, 5, 5, 7, 6, 7, 6, 7, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 9, 10, 10, 10, 11, 10, 11, 11, 11, 11, 11], [
                              4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11]),
                             ([6, 6, 6, 6, 6, 5, 5, 6, 7, 7, 6, 7, 7, 6, 6, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 8, 9, 10, 10, 10, 11, 12, 12, 12, 11, 12, 12, 11, 12, 12, 13, 14, 14, 14, 14, 14, 15, 14, 15, 15], [
                              6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15]),
                             ([7, 6, 7, 7, 6, 7, 7, 7, 8, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 9, 9, 10, 10, 9, 10, 10, 10, 11, 11, 12, 11, 12, 12, 13, 12, 13, 13, 12, 13, 13, 14, 14, 14, 14, 15, 15, 16, 17, 17, 16], [
                              7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 16, 17, 17, 17]),
                             ([8, 7, 7, 7, 8, 8, 7, 7, 9, 8, 8, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 11, 12, 13, 13, 13, 13, 12, 13, 13, 13, 14, 13, 13, 13, 13, 14, 14, 13, 13, 14, 16], [
                              8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 16]),
                             ([9, 9, 9, 8, 9, 8, 9, 10, 10, 10, 11, 12, 12, 12, 12, 11, 12, 11, 12, 12, 12, 13, 13, 13, 12, 12, 13, 12, 14, 13, 15, 15, 15, 16, 16, 15, 15, 16, 16, 16, 17, 16, 17, 17, 16, 17, 17, 17, 18, 18], [
                              9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 14, 14, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18]),
                             ([10, 10, 9, 9, 9, 10, 10, 11, 11, 11, 11, 10, 11, 11, 12, 12, 12, 11, 11, 13, 13, 13, 13, 12, 12, 13, 13, 12, 13, 14, 13, 15, 15, 15, 16, 15, 17, 17, 16, 16, 17, 16, 18, 18, 18, 19, 19, 20, 20, 20], [
                              10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 15, 15, 15, 16, 16, 17, 17, 17, 17, 17, 17, 18, 18, 18, 19, 19, 20, 20, 20]),
                             ([10, 11, 10, 11, 10, 11, 11, 11, 12, 12, 11, 11, 12, 11, 11, 12, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 15, 14, 15, 15, 15, 14, 15, 15, 14, 16, 16, 16, 16, 16, 16, 15, 15, 16, 16, 17, 17, 17, 18, 18], [
                              10, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 18, 18]),
                             ([12, 12, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 12, 12, 13, 14, 15, 14, 16, 15, 16, 16, 16, 16, 16, 17, 17, 18, 19, 19, 18, 19, 19, 19, 20, 20, 19, 20, 20, 21, 21, 22, 22, 22, 22, 21], [
                              12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 15, 15, 16, 16, 16, 16, 16, 16, 16, 17, 17, 18, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 21, 21, 22, 22, 22, 22, 22]),
                             ([12, 12, 13, 14, 14, 13, 13, 15, 15, 15, 14, 14, 16, 16, 17, 17, 16, 16, 17, 17, 18, 18, 17, 17, 18, 18, 18, 18, 18, 19, 19, 19, 19, 18, 18, 18, 19, 20, 20, 19, 20, 19, 19, 19, 20, 21, 20, 20, 20, 21], [
                              12, 12, 13, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21]),
                             ([13, 14, 13, 13, 13, 13, 13, 14, 13, 14, 14, 14, 16, 16, 16, 16, 16, 17, 17, 16, 16, 16, 17, 18, 18, 17, 17, 18, 17, 17, 18, 17, 19, 18, 18, 18, 18, 18, 18, 19, 18, 18, 19, 19, 19, 19, 19, 19, 20, 19], [
                              13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20]),
                             ([15, 15, 15, 15, 14, 15, 14, 14, 16, 16, 15, 16, 15, 15, 15, 15, 15, 15, 17, 17, 16, 16, 17, 16, 17, 17, 17, 18, 18, 19, 18, 18, 19, 19, 20, 21, 20, 21, 22, 21, 22, 21, 21, 21, 21, 22, 22, 23, 22, 23], [
                              15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 19, 19, 19, 19, 19, 20, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23]),
                             ([16, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 16, 16, 16, 16, 17, 18, 17, 18, 18, 18, 17, 18, 17, 18, 17, 19, 19, 18, 18, 18, 18, 19, 20, 19, 20, 19, 19, 20, 20, 19, 20, 20, 22, 22, 23, 22, 22, 22], [
                              16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22, 22, 23, 23, 23, 23]),
                             ([16, 17, 18, 17, 18, 18, 19, 19, 19, 18, 19, 20, 19, 19, 19, 19, 20, 20, 19, 20, 21, 21, 20, 21, 20, 20, 21, 21, 20, 22, 23, 23, 22, 23, 23, 22, 23, 22, 24, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24], [
                              16, 17, 18, 18, 18, 18, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24]),
                             ([17, 17, 19, 18, 18, 18, 18, 18, 18, 19, 19, 19, 20, 19, 19, 19, 20, 19, 19, 20, 20, 22, 21, 21, 21, 21, 21, 21, 21, 22, 22, 23, 22, 22, 22, 24, 23, 23, 23, 23, 23, 24, 23, 24, 24, 24, 24, 25, 24, 25], [
                              17, 17, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25, 25, 25]),
                             ([19, 18, 19, 19, 19, 20, 20, 20, 21, 20, 20, 20, 20, 21, 22, 21, 21, 22, 22, 21, 21, 22, 22, 22, 23, 23, 24, 25, 24, 25, 24, 25, 25, 26, 25, 25, 27, 26, 27, 26, 26, 28, 27, 27, 28, 27, 28, 27, 27, 27], [19, 19, 19, 19, 19, 20, 20, 20, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 24, 25, 25, 25, 25, 25, 25, 26, 26, 26, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28])])
def test_random_test_cases(data, cleaned_data):
    assert cleaned_counts(data) == cleaned_data
