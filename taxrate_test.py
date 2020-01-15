import pytest
import taxrate as t

def test_calculate_tax():
    assert t.calculate_tax(1000) == 60
    assert t.calculate_tax(1500) == 117
    assert t.calculate_tax(2000) == 192
    assert t.calculate_tax(2500) == 267
    assert t.calculate_tax(3000) == 342
    assert t.calculate_tax(3500) == 417
    assert t.calculate_tax(4000) == 492
    assert t.calculate_tax(4500) == 567
    assert t.calculate_tax(5000) == 678
    assert t.calculate_tax(6000) == 918
    assert t.calculate_tax(7000) == 1158
    assert t.calculate_tax(8000) == 1398
    assert t.calculate_tax(9000) == 1660
    assert t.calculate_tax(10000) == 2010
    assert t.calculate_tax(20000) == 5660
    assert t.calculate_tax(30000) == 9460
    assert t.calculate_tax(40000) == 13460
    assert t.calculate_tax(50000) == 17460
    assert t.calculate_tax(60000) == 21660

test_calculate_tax()