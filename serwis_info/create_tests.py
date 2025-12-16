def create_tests():
    
    from serwis_info.modules.exchange.tests import test_stockmarket

    return [test_stockmarket]


if __name__ == "__main__":
    create_tests()
