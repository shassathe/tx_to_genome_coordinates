from typing import List, Tuple
from enum import Enum
import sys
import re


class valid_cigar_characters(Enum):
	"""
	Define the allowed mapping characters in a cigar string. Use this as a reference to confirm that an appropriate
	cigar string has been provided.
	"""
	D = "Deletion"
	I = "Insertion"
	M = "Match"


def cigar_string_to_mapping_blocks(cigar: str) -> List[Tuple[int, str]]:
	"""
	This function will split a cigar string into its building blocks.
	For example: "4M1D3I45M will be returned as [(4, "M"), (1, "D"), (3, "I"), (45, "M")]
	This will also check whether the cigar string only contains the usual mapping types such as "M", "I" and "D"

	Args:
		cigar: Cigar string to split into mapping blocks
	Returns:
		mapping_blocks: Cigar string split into tuples to (mapping length and mapping type)
	"""
	cigar_characters: set = set(valid_cigar_characters.__members__)
	delimiters = r"([A-Z])"

	# Split cigar string into mapping blocks
	cigar_split = re.split(delimiters, cigar)
	mapping_blocks = [
		(int(cigar_split[i]), cigar_split[i + 1]) for i in range(0, len(cigar_split) - 1) if
		cigar_split[i] not in cigar_characters
	]

	mapping_type = {block[1] for block in mapping_blocks}
	if mapping_type.difference(cigar_characters):
		raise ValueError(f"Found non-canonical values in Cigar string {cigar}")
	return mapping_blocks


def tx_length(cigar: str) -> int:
	"""
	Args:
		cigar: Cigar string to calculate the tx length from.
	Returns:
		total_tx_length: int
	"""
	mapping_blocks = cigar_string_to_mapping_blocks(cigar)
	total_tx_length = 0
	for block in mapping_blocks:
		block_length = block[0]
		mapping_type = block[1]
		if mapping_type in ["M", "I"]:
			total_tx_length += block_length
	return total_tx_length


def convert_to_genomic_coordinates(
		query_tx_name: str, query_tx_coordinate: int, genome_coordinate: int, cigar: str,
) -> int:
	"""
	Args:
		query_tx_name: Name if the query transcript
		query_tx_coordinate: The query tx coordinate to return the corresponding genome coordinate for
		genome_coordinate: Geome coordinate at the start of the mapping.
		cigar: The cigar string for the corresponding mapping
	Returns:
		genome_coordinate: The genome coordinate for the query_tx_coordinate
	"""
	tx_pos = 0
	mapping_blocks = cigar_string_to_mapping_blocks(cigar)
	total_tx_length = tx_length(cigar)
	if query_tx_coordinate > total_tx_length:
		raise ValueError(
			f"Coordinate {query_tx_coordinate} for transcript {query_tx_name} is greater that the total transcript "
			f"length ({total_tx_length}). Genome coordinate cannot be calculated"
		)

	for block in mapping_blocks:
		block_length = block[0]
		mapping_type = block[1]
		if mapping_type == "M":
			genome_coordinate += block_length
			tx_pos += block_length
			if tx_pos >= query_tx_coordinate:
				pos_diff = tx_pos - query_tx_coordinate
				genome_coordinate -= pos_diff
				break
		elif mapping_type == "D":
			genome_coordinate += block_length
		elif mapping_type == "I":
			tx_pos += block_length
			if tx_pos >= query_tx_coordinate:
				break
	return genome_coordinate
