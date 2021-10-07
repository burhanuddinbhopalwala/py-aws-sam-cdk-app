
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "unittest: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integrationtest: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "datasciencetest: mark test as datascience test"
