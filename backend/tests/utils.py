import numpy as np


def compare_results(result, expected_result, exception_list=None):
    """
    Compares json like objects (dictionaries, lists, and types with equality).

    This handles float comparison using np.isclose for better comparison. Also, accepts
    a list of keys to ignore in comparison, useful for data that should not be compared (
    e.g. ids, timestamps, ...etc).

    """
    if type(expected_result) != type(result):
        assert (
            False
        ), f"expected_result: ({type(expected_result)}), result: ({type(result)}) have different types"
    elif not isinstance(expected_result, (list, dict)) and not isinstance(
        result, (list, dict)
    ):
        if isinstance(result, float) or isinstance(expected_result, float):
            assert np.isclose(result, expected_result), f"{result} != {expected_result}"
        else:
            assert result == expected_result, f"{result} != {expected_result}"
    else:
        assert len(result) == len(expected_result), (
            f"Different lengths len(result)={len(result)} != {len(expected_result)}=len(nexpected_result)"
            f"\nresult:{result}\nexpected_result:{expected_result}"
        )
        for i, k in enumerate(expected_result):
            if isinstance(expected_result, dict):
                if exception_list is not None and k in exception_list:
                    continue
                assert k in result, f"Key ({k}) does not exists in result"
                compare_results(result[k], expected_result[k], exception_list)
            elif isinstance(expected_result, list):
                compare_results(result[i], expected_result[i], exception_list)
            else:
                raise ValueError(
                    f"Type ({type(result)}) is not supported by this function"
                )


TEST_USER = [
    {
        "username": "test_new_user@mozn.sa",
        "password": "VeryStrongPassWordDontChangeEver",
        "full_name": "Test_new_user",
    },
    {
        "username": "test_new_user@mozn.sa",
        "password": "VeryVeryVeryStrongPassWordDontChangeEver",
        "full_name": "Test_new_user new_full_name",
    },
    {
        "username": "the_ultimate_user@mozn.sa",
        "password": "VeryVeryVeryStrongPassWordDontChangeEverEvenIfYouReallyWantTo",
        "full_name": "The ultimate new_user",
    },
]
