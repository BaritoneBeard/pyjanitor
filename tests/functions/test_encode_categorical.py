import numpy as np
import pandas as pd
import pytest
from hypothesis import given
from pandas.testing import assert_frame_equal

from janitor.testing_utils.strategies import (
    categoricaldf_strategy,
    df_strategy,
)


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_encode_categorical(df):
    df = df.encode_categorical("names")
    assert df["names"].dtypes == "category"


@pytest.mark.functions
@given(df=df_strategy())
def test_encode_categorical_missing_column(df):
    """
    Raise ValueError for missing columns
    when only one arguments is provided to
    `column_names`.
    """
    with pytest.raises(ValueError):
        df.encode_categorical("aloha")


@pytest.mark.functions
@given(df=df_strategy())
def test_encode_categorical_missing_columns(df):
    """
    Raise ValueError for missing columns
    when the number of arguments to `column_names`
    is more than one.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(["animals@#$%^", "cities", "aloha"])


@pytest.mark.functions
@given(df=df_strategy())
def test_encode_categorical_invalid_input(df):
    """
    Raise ValueError for wrong input type
    for `column_names`.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(1)


@pytest.mark.functions
@given(df=df_strategy())
def test_encode_categorical_invalid_input_2(df):
    """
    Raise TypeError for wrong input type
    for `column_names`.
    """
    with pytest.raises(TypeError):
        df.encode_categorical({"names"})


@pytest.mark.functions
@given(df=df_strategy())
def test_encode_categorical_multiple_column_names(df):
    """
    Test output when more than one column is provided
    to `column_names`.
    """
    result = df.astype({"a": "category", "cities": "category"})
    assert_frame_equal(
        df.encode_categorical(column_names=["a", "cities"]),
        result,
    )


@pytest.mark.functions
@given(df=df_strategy())
def test_both_column_names_kwargs(df):
    """
    Raise Error if both `column_names`
    and kwargs are provided.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(
            column_names=["a", "cities"], Bell__Chart=(None, "sort")
        )


@pytest.mark.functions
@given(df=df_strategy())
def test_check_presence_column_names_in_kwargs(df):
    """
    Raise ValueError if column names in `kwargs`
    do not exist in the dataframe.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(col_1=(None, "sort"))


@pytest.mark.functions
@given(df=df_strategy())
def test_check_type_tuple_in_kwargs(df):
    """
    Raise TypeError if the categories, order pairing
    in `kwargs` is not a tuple.
    """
    with pytest.raises(TypeError):
        df.encode_categorical(a=[None, "sort"])


@pytest.mark.functions
@given(df=df_strategy())
def test_tuple_length_in_kwargs(df):
    """
    Raise ValueError if the length of the tuple
    in kwargs is not equal to 2.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(a=(None, None, 2))


@pytest.mark.functions
@given(df=df_strategy())
def test_categories_type_in_kwargs(df):
    """
    Raise TypeError if the wrong argument is supplied to
    the `categories` parameter in kwargs.
    """
    with pytest.raises(TypeError):
        df.encode_categorical(a=("category", None))


@pytest.mark.functions
@given(df=df_strategy())
def test_categories_ndim_array_gt_1_in_kwargs(df):
    """
    Raise ValueError if the argument supplied to
    the `categories` parameter in kwargs is not
    1-D array-like.
    """
    arrays = [[1, 1, 2, 2], ["red", "blue", "red", "blue"]]
    with pytest.raises(ValueError):
        df.encode_categorical(a=(arrays, None))


@pytest.mark.functions
@given(df=df_strategy())
def test_categories_ndim_MultiIndex_gt_1_in_kwargs(df):
    """
    Raise ValueError if the argument supplied to
    the `categories` parameter in kwargs is not
    1-D array-like.
    """
    arrays = [[1, 1, 2, 2], ["red", "blue", "red", "blue"]]
    arrays = pd.MultiIndex.from_arrays(arrays, names=("number", "color"))
    with pytest.raises(ValueError):
        df.encode_categorical(a=(arrays, None))


@pytest.mark.functions
@given(df=df_strategy())
def test_categories_ndim_DataFrame_gt_1_in_kwargs(df):
    """
    Raise ValueError if the argument supplied to
    the `categories` parameter in kwargs is not
    1-D array-like.
    """
    arrays = {"name": [1, 1, 2, 2], "number": ["red", "blue", "red", "blue"]}
    arrays = pd.DataFrame(arrays)
    with pytest.raises(ValueError):
        df.encode_categorical(a=(arrays, None))


@pytest.mark.functions
@given(df=df_strategy())
def test_categories_null_in_categories(df):
    """
    Raise ValueError if there are nulls in the `categories`.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(a=([None, 2, 3], None))


@pytest.mark.functions
@given(df=df_strategy())
def test_non_unique_cat(df):
    """Raise ValueError if `categories` is not unique."""
    with pytest.raises(ValueError):
        df.encode_categorical(a=([1, 2, 3, 3], "sort"))


@pytest.mark.functions
@given(df=df_strategy())
def test_empty_cat(df):
    """Raise ValueError if `categories` is empty."""
    with pytest.raises(ValueError):
        df.encode_categorical(a=([], "sort"))


@pytest.mark.functions
@given(df=df_strategy())
def test_empty_col(df):
    """
    Raise ValueError if `categories`,
    and the relevant column is empty, or all nulls.
    """
    with pytest.raises(ValueError):
        df["col1"] = np.nan
        df.encode_categorical(col1=([1, 2, 3], "sort"))


@pytest.mark.functions
@given(df=df_strategy())
def test_empty_col_2(df):
    """
    Raise ValueError if `categories` is None,
    and the relevant column is empty, or all nulls.
    """
    with pytest.raises(ValueError):
        df["col1"] = np.nan
        df.encode_categorical(col1=(None, "sort"))


@pytest.mark.functions
@given(df=df_strategy())
def test_empty_col_3(df):
    """
    Raise ValueError if `categories` is None,
    and the relevant column is empty, or all nulls.
    """
    with pytest.raises(ValueError):
        df["col1"] = pd.Series([], dtype="object")
        df.encode_categorical(col1=(None, "appearance"))


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_warnings(df):
    """
    Test that warnings are raised if `categories` is provided, and
    the categories do not match the unique values in the column, or
    some values in the column are missing in `categories`.
    """
    with pytest.warns(UserWarning):
        df.encode_categorical(
            numbers=([4, 5, 6], None), names=(["John", "Mark", "Luke"], "sort")
        )


@pytest.mark.functions
@given(df=df_strategy())
def test_order_type_in_kwargs(df):
    """
    Raise TypeError if the wrong argument is supplied to
    the `order` parameter in kwargs.
    """
    with pytest.raises(TypeError):
        df.encode_categorical(a=({1, 2, 3, 3}, {"sort"}))


@pytest.mark.functions
@given(df=df_strategy())
def test_order_wrong_option_in_kwargs(df):
    """
    Raise ValueError if the value supplied to the `order`
    parameter in kwargs is not one of None, 'sort', or 'appearance'.
    """
    with pytest.raises(ValueError):
        df.encode_categorical(a=({1, 2, 3, 3}, "sorted"))


# directly comparing columns is safe -
# if the columns have differing categories
# (especially for ordered True) it will fail.
# if both categories are unordered, then the
# order is not considered.
# comparing with assert_frame_equal fails
# for unordered categoricals, as internally
# the order of the categories are compared
# which is irrelevant for unordered categoricals


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_all_None(df):
    """
    Test output where `categories` and `order` are None.
    """
    result = df.encode_categorical(names=(None, None))

    expected = df.astype({"names": "category"})
    assert expected["names"].equals(result["names"])


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_all_cat_None_1(df):
    """
    Test output where `categories` is None.
    """
    result = df.encode_categorical(names=(None, "sort"))
    categories = pd.CategoricalDtype(
        categories=df.names.factorize(sort=True)[-1], ordered=True
    )
    expected = df.astype({"names": categories})
    assert expected["names"].equals(result["names"])


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_all_cat_None_2(df):
    """
    Test output where `categories` is None.
    """
    result = df.encode_categorical(names=(None, "appearance"))
    categories = pd.CategoricalDtype(
        categories=df.names.factorize(sort=False)[-1], ordered=True
    )
    expected = df.astype({"names": categories})
    assert expected["names"].equals(result["names"])


@pytest.mark.functions
@given(df=categoricaldf_strategy())
def test_all_cat_not_None(df):
    """
    Test output where `categories` is  not None.
    """
    result = df.encode_categorical(numbers=(np.array([3, 1, 2]), "appearance"))
    categories = pd.CategoricalDtype(categories=[3, 1, 2], ordered=True)
    expected = df.astype({"numbers": categories})
    assert expected["numbers"].equals(result["numbers"])
