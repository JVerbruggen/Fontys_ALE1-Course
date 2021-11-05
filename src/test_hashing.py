from hashing import *

def test_hash():
    assert Hashing.get_hash("00110111") == "37"
    assert Hashing.get_hash("01010101") == "55"
    assert Hashing.get_hash("1111") == "F"
    assert Hashing.get_hash("0001") == "1"
    assert Hashing.get_hash("10001") == "11"
    assert Hashing.get_hash("100110111") == "137"