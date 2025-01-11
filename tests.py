import pytest
from cigar_parser import cigar_string_to_mapping_blocks, tx_length, convert_to_genomic_coordinates


def test_cigar_string_to_mapping_blocks(cigar="8M7D6M2I2M11D7M"):
    mapping_blocks = cigar_string_to_mapping_blocks(cigar)
    assert mapping_blocks == [(8, "M"), (7, "D"), (6, "M"), (2, "I"), (2, "M"), (11, "D"), (7, "M")]


def test_tx_length(cigar="8M7D6M2I2M11D7M"):
    total_tx_length = tx_length(cigar)
    assert total_tx_length == 25


def test_convert_to_genomic_coordinates(
        query_tx_name="TX1", query_tx_coordinate=4, genome_coordinate=3, cigar="8M7D6M2I2M11D7M",
):
    corresponding_genome_coordinate: int = convert_to_genomic_coordinates(
        query_tx_name, query_tx_coordinate, genome_coordinate, cigar
    )
    assert corresponding_genome_coordinate == 7


def test_tx_length_failure(
        query_tx_name="TX1", query_tx_coordinate=50, genome_coordinate=3, cigar="8M7D6M2I2M11D7M",
):
    # Test to confirm that program will successfully error out if provided tx coordinate is greater than the
    # transcript length
    # If exception is correctly raised, test will pass
    with pytest.raises(ValueError):
        convert_to_genomic_coordinates(
            query_tx_name, query_tx_coordinate, genome_coordinate, cigar
        )
