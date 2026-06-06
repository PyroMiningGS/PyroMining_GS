from src.processing.monte_alegre_index import calculate_monte_alegre

def test_monte_alegr():

    result = calculate_monte_alegr(
        35,
        30
    )

    assert result == 2450