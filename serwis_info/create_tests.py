def create_tests():
    
    from serwis_info.modules.exchange.tests import test_stockmarket
    from serwis_info.modules.exchange.tests import test_currencies
    from serwis_info.modules.exchange.tests import test_journey

    return [test_stockmarket, test_journey, test_currencies]


if __name__ == "__main__":
    create_tests()
