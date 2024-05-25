import unittest
from useful_tools.ip_address import is_public_ip_address, is_reserved_ip_address, is_valid_ip_address

class TestPublicIPAddress(unittest.TestCase):
    def test_is_public_ip_address_0_0_0_0(self):
        self.assertFalse(is_public_ip_address('0.0.0.0'))

    def test_is_public_ip_address_192_168_0_0(self):
        self.assertFalse(is_public_ip_address('192.168.0.0'))

    def test_is_public_ip_address_8_8_8_8(self):
        self.assertTrue(is_public_ip_address('8.8.8.8'))


class TestReservedIPAddress_Positive(unittest.TestCase):
    def test_is_reserved_ip_address_0_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('0.0.0.0'))

    def test_is_reserved_ip_address_10_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('10.0.0.0'))

    def test_is_reserved_ip_address_100_64_0_0(self):
        self.assertTrue(is_reserved_ip_address('100.64.0.0'))

    def test_is_reserved_ip_address_127_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('127.0.0.0'))

    def test_is_reserved_ip_address_169_254_0_0(self):
        self.assertTrue(is_reserved_ip_address('169.254.0.0'))

    def test_is_reserved_ip_address_172_16_0_0(self):
        self.assertTrue(is_reserved_ip_address('172.16.0.0'))

    def test_is_reserved_ip_address_172_31_0_0(self):
        self.assertTrue(is_reserved_ip_address('172.31.0.0'))

    def test_is_reserved_ip_address_192_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('192.0.0.0'))

    def test_is_reserved_ip_address_192_0_2_0(self):
        self.assertTrue(is_reserved_ip_address('192.0.2.0'))

    def test_is_reserved_ip_address_192_88_99_0(self):
        self.assertTrue(is_reserved_ip_address('192.88.99.0'))

    def test_is_reserved_ip_address_192_168_0_0(self):
        self.assertTrue(is_reserved_ip_address('192.168.0.0'))

    def test_is_reserved_ip_address_198_18_0_0(self):
        self.assertTrue(is_reserved_ip_address('198.18.0.0'))

    def test_is_reserved_ip_address_198_51_100_0(self):
        self.assertTrue(is_reserved_ip_address('198.51.100.0'))

    def test_is_reserved_ip_address_203_0_113_0(self):
        self.assertTrue(is_reserved_ip_address('203.0.113.0'))

    def test_is_reserved_ip_address_224_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('224.0.0.0'))

    def test_is_reserved_ip_address_233_252_0_0(self):
        self.assertTrue(is_reserved_ip_address('233.252.0.0'))

    def test_is_reserved_ip_address_240_0_0_0(self):
        self.assertTrue(is_reserved_ip_address('240.0.0.0'))

    def test_is_reserved_ip_address_255_255_255_255(self):
        self.assertTrue(is_reserved_ip_address('255.255.255.255'))


class TestReservedIPAddress_Negative(unittest.TestCase):
    def test_is_not_reserved_ip_address_1_0_0_0(self):
        self.assertFalse(is_reserved_ip_address('1.0.0.0'))

    def test_is_not_reserved_ip_address_11_0_0_0(self):
        self.assertFalse(is_reserved_ip_address('11.0.0.0'))

    def test_is_not_reserved_ip_address_100_65_0_0(self):
        self.assertFalse(is_reserved_ip_address('100.65.0.0'))

    def test_is_not_reserved_ip_address_128_0_0_0(self):
        self.assertFalse(is_reserved_ip_address('128.0.0.0'))

    def test_is_not_reserved_ip_address_169_255_0_0(self):
        self.assertFalse(is_reserved_ip_address('169.255.0.0'))

    def test_is_not_reserved_ip_address_172_15_0_0(self):
        self.assertFalse(is_reserved_ip_address('172.15.0.0'))

    def test_is_not_reserved_ip_address_172_32_0_0(self):
        self.assertFalse(is_reserved_ip_address('172.32.0.0'))

    def test_is_not_reserved_ip_address_192_0_1_0(self):
        self.assertFalse(is_reserved_ip_address('192.0.1.0'))

    def test_is_reserved_ip_address_192_0_3_0(self):
        self.assertFalse(is_reserved_ip_address('192.0.3.0'))

    def test_is_reserved_ip_address_192_88_100_0(self):
        self.assertFalse(is_reserved_ip_address('192.88.100.0'))

    def test_is_reserved_ip_address_192_169_0_0(self):
        self.assertFalse(is_reserved_ip_address('192.169.0.0'))

    def test_is_reserved_ip_address_198_20_0_0(self):
        self.assertFalse(is_reserved_ip_address('198.20.0.0'))

    def test_is_reserved_ip_address_198_51_101_0(self):
        self.assertFalse(is_reserved_ip_address('198.51.101.0'))

    def test_is_reserved_ip_address_203_0_114_0(self):
        self.assertFalse(is_reserved_ip_address('203.0.114.0'))

    def test_is_reserved_ip_address_225_0_0_0(self):
        self.assertFalse(is_reserved_ip_address('225.0.0.0'))

    def test_is_reserved_ip_address_233_252_1_0(self):
        self.assertFalse(is_reserved_ip_address('233.252.1.0'))

    def test_is_reserved_ip_address_241_0_0_0(self):
        self.assertFalse(is_reserved_ip_address('241.0.0.0'))

    def test_is_reserved_ip_address_255_255_255_254(self):
        self.assertFalse(is_reserved_ip_address('255.255.255.254'))


class TestIsValidIPAddress_Good(unittest.TestCase):
    # test is_valid_ip_address -- good

    def test_is_valid_ip_address_123_4_5_6(self):
        self.assertTrue(is_valid_ip_address('123.4.5.6'))

    def test_is_valid_ip_address_192_167_1_1(self):
        self.assertTrue(is_valid_ip_address('192.167.1.1'))

    def test_is_valid_ip_address_1_1_1_1(self):
        self.assertTrue(is_valid_ip_address('1.1.1.1'))

    def test_is_valid_ip_address_255_255_255_254(self):
        self.assertTrue(is_valid_ip_address('255.255.255.254'))

class TestIsValidPAddress_Invalid(unittest.TestCase):
    # test is_valid_ip_address -- invalid

    def test_is_valid_ip_address_192_0_2_256(self):
        self.assertFalse(is_valid_ip_address('192.0.2.256'))

    def test_is_valid_ip_address_300_88_99_30(self):
        self.assertFalse(is_valid_ip_address('300.88.99.30'))

    def test_is_valid_ip_address_192_1680_0_100(self):
        self.assertFalse(is_valid_ip_address('192.1680.0.100'))

    def test_is_valid_ip_address_198_18_1000_1(self):
        self.assertFalse(is_valid_ip_address('198.18.1000.1'))

    def test_is_valid_ip_address_localhost(self):
        self.assertFalse(is_valid_ip_address('localhost'))

    def test_is_valid_ip_address_a_0_113_30(self):
        self.assertFalse(is_valid_ip_address('a.0.113.30'))

    def test_is_valid_ip_address_224_b_0_4(self):
        self.assertFalse(is_valid_ip_address('224.b.0.4'))

    def test_is_valid_ip_address_233_252_c_50(self):
        self.assertFalse(is_valid_ip_address('233.252.c.50'))

    def test_is_valid_ip_address_240_0_0_d(self):
        self.assertFalse(is_valid_ip_address('240.0.0.d'))

    def test_is_valid_ip_address_minus1_255_255_254(self):
        self.assertFalse(is_valid_ip_address('-1.255.255.254'))

    def test_is_valid_ip_address_192_0(self):
        self.assertFalse(is_valid_ip_address('192.0'))

    def test_is_valid_ip_address_192_0_2(self):
        self.assertFalse(is_valid_ip_address('192.0.2'))

    def test_is_valid_ip_address_192_88_99_0_0(self):
        self.assertFalse(is_valid_ip_address('192.88.99.0.0'))

    def test_is_valid_ip_address_198_18_0_minus_1(self):
        self.assertFalse(is_valid_ip_address('198.18.0.-1'))


class TestIsValidIPAddress_Reserved(unittest.TestCase):
    def test_is_valid_ip_address_192_0_2_0(self):
        self.assertTrue(is_valid_ip_address('192.0.2.0'))

    def test_is_valid_ip_address_192_88_99_0(self):
        self.assertTrue(is_valid_ip_address('192.88.99.0'))

    def test_is_valid_ip_address_192_168_0_0(self):
        self.assertTrue(is_valid_ip_address('192.168.0.0'))

    def test_is_valid_ip_address_198_18_0_0(self):
        self.assertTrue(is_valid_ip_address('198.18.0.0'))

    def test_is_valid_ip_address_198_51_100_0(self):
        self.assertTrue(is_valid_ip_address('198.51.100.0'))

    def test_is_valid_ip_address_203_0_113_0(self):
        self.assertTrue(is_valid_ip_address('203.0.113.0'))

    def test_is_valid_ip_address_224_0_0_0(self):
        self.assertTrue(is_valid_ip_address('224.0.0.0'))

    def test_is_valid_ip_address_233_252_0_0(self):
        self.assertTrue(is_valid_ip_address('233.252.0.0'))

    def test_is_valid_ip_address_240_0_0_0(self):
        self.assertTrue(is_valid_ip_address('240.0.0.0'))

    def test_is_valid_ip_address_255_255_255_255(self):
        self.assertTrue(is_valid_ip_address('255.255.255.255'))


if __name__ == '__main__':
    unittest.main()