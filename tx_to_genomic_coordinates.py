import argparse
import pandas as pd
from cigar_parser import convert_to_genomic_coordinates
from pathlib import Path


def main():
	parser = argparse.ArgumentParser(
		description='This program will convert tx coordinate to genomic coordates based on the provided CIGAR strings.'
	)
	parser.add_argument(
		'-t',
		'--mapping_file',
		type=str,
		help='Path to a mapping file containing the tx ID, genome coordinates and cigar string to alignment'
	)
	parser.add_argument(
		'-q',
		'--queries',
		type=str,
		help='Path to query file to extract data for'
	)

	# Parse arguments
	args = parser.parse_args()

	# Use the parsed arguments
	if not args.mapping_file or not args.queries:
		parser.error("Missing input. Both mapping and query files are required.")

	mapping_file = Path(args.mapping_file)
	mapping = pd.read_csv(mapping_file, sep="\t", names=["tx_name", "chrom", "mapping_start_pos", "cigar"])
	if len(mapping) > len(set(mapping.tx_name)):
		raise ValueError("Found duplicate transcript IDs in mapping file.")
	mapping = mapping.set_index("tx_name")

	query_file = Path(args.queries)
	queries = pd.read_csv(query_file, sep="\t", names=["tx_name", "tx_coordinate"])

	for i in queries.index:
		query_tx_name: str = queries.loc[i, "tx_name"]
		query_tx_coordinate: int = int(queries.loc[i, "tx_coordinate"])
		tx_pos = 0

		genome_coordinate: int = int(mapping.loc[query_tx_name, "mapping_start_pos"])
		cigar: str = mapping.loc[query_tx_name, "cigar"]

		corresponding_genome_coordinate: int = convert_to_genomic_coordinates(
			query_tx_name, query_tx_coordinate, genome_coordinate, cigar
		)

		queries.loc[i, "chrom"] = mapping.loc[query_tx_name, "chrom"]
		queries.loc[i, "genome_coordinate"] = corresponding_genome_coordinate

	output_file = query_file.with_name(query_file.stem + "_genome_coordinates" + query_file.suffix)
	queries.to_csv(output_file, sep="\t")


if __name__ == "__main__":
	main()
