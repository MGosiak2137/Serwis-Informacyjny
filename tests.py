from serwis_info.create_tests import create_tests

create_tests()

if __name__ == "__main__":
	import sys
	import pytest

	sys.exit(pytest.main())
