#!/usr/bin/env python3
import argparse
import os.path


def load_gold(g_path):
	gold_f = open(g_path, "r")
	all_ref_ali = {}
	all_ref_count = 0.

	for line in gold_f:
		line = line.strip().split("\t")
		line[1] = line[1].split()   # list of strings like '0,6-0,7'
		all_ref_ali[line[0]] = set([x for x in line[1]])
		all_ref_count += len(all_ref_ali[line[0]])
	return all_ref_ali, all_ref_count

def calc_score(input_path, all_ref_ali, all_ref_count):
	total_hit = 0.
	correct_hit = 0.
	target_f = open(input_path, "r")

	for line in target_f:
		line = line.strip().split("\t")
		line[1] = line[1].split()
		
		correct_hit += len(set(line[1]) & set(all_ref_ali[line[0]]))
		total_hit += len(set(line[1]))
	target_f.close()

	prec = correct_hit/total_hit
	rec = correct_hit/all_ref_count
	return prec,rec


if __name__ == "__main__":
	'''
	The gold annotated file should be selected by "gold_path".
	The generated alignment file should be selected by "input_path".

	usage: python calc_align_score.py gold_file generated_file
	'''

	parser = argparse.ArgumentParser(description="Calculate alignment quality scores based on the gold standard.", epilog="example: python calc_align_score.py gold_path input_path")
	parser.add_argument("gold_path")
	parser.add_argument("input_path")
	args = parser.parse_args()

	if not os.path.isfile(args.input_path):
		print("The input file does not exist:\n", args.input_path)
		exit()

	surs, surs_count = load_gold(args.gold_path)
	prec,rec = calc_score(args.input_path,surs, surs_count)

	print("prec: {}\trec: {}".format(prec,rec))

