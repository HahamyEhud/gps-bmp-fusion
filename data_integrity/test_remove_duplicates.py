import remove_duplicates
import numpy as np

def test_remove_duplicates_vanilla():
    out = remove_duplicates.build_unique_time_arr(np.array([0,1,2]), np.array([1,2,3]))
    assert out ==

# def test_remove_duplicates_inner():
#     remove_duplicates.build_unique_time_arr(np.array([1,2,3,3,3,4,5,5,8,8,8,9,9,10,10]))

# def test_remove_duplicates_left_edge():

# def test_remove_duplicates_right_edge():
