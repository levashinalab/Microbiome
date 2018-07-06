import argparse
import re
import os
import shutil
from shutil import move
import gzip
# on the terminal, source activate qiime2-2018.4

parser = argparse.ArgumentParser("Joins paired-end reads from microbiota sequencing")
parser.add_argument('-md','--mother_directory',help = "Write name of mother directory ended by slash", required = True)
parser.add_argument('-v','--version',action = "store", help = "Write name of version", required = True)
parser.add_argument('-op','--output_path',help = "Write path of output folder", required = True)
args = parser.parse_args()
#print(args.output_path)

os.mkdir(args.output_path)

#Transfer files from server to other place
##########################################################

#change name of all files in a certain format
for root, dirs, files in os.walk(args.mother_directory):
	for file in files:
		r = re.search("(.*)_(.*)_(.*)_(.*)_(.*)_(.*)_(.*)_(.*)_(.*)_(.*).fastq.gz",file)
		print(r)
		if r is not None:
			one = r.group(1)
			two = r.group(2)
			three = r.group(3)
			four = r.group(4)
			five = r.group(5)
			six = r.group(6)
			seven = r.group(7)
			eight = r.group(8)
			nine = r.group(9)
			ten = r.group(10)
			#dirpath = os.getcwd()
			#print("current directory is : " + dirpath)
			
			new = one + two + three + four + five + "_" + six + "_" + seven + "_" + eight + "_" + nine + ".fastq.gz"
			os.rename(args.mother_directory + "/" + file,args.mother_directory + "/" + new)


#3539A7run496TTCCTAGGCCAG_S24_L002_R1_001
#3539_A_2_run496_AGGGTGACTTTA_S19_L002_R2_001_3

#assemble reverse and forward files in one folder having the name of the barcode
for root, dirs, files in os.walk(args.mother_directory):
	for file in files:
		if re.match(".*R1.*.fastq.gz",file):
			fileR1 = file
			a=re.search(".*run\d*(.*)_.*_.*_R1.*.fastq.gz",file)
			
			if  a is not None:
				b=a.group(1)
				for root, dirs, files in os.walk(args.mother_directory):
					for file in files:
						if re.match(".*R2.*.fastq",file):
							c=re.search(".*run\d*(.*)_.*_.*_R2.*.fastq.gz",file)
							if  c is not None:
								d=c.group(1)
								if d == b:
									fileR2 = file
									#print(args.mother_directory)
									
									
									o_folder = args.output_path+"/"+b
									o_folderR1 = o_folder + "/" + fileR1
									print(o_folderR1)
									print(o_folder)
									os.makedirs(o_folder)
									#os.makedirs(o_folder + "/filtered_sequences")
									
									
									os.system("cp " + args.mother_directory + "/" + fileR1 + " " + o_folder + "/" + fileR1)
									os.system("cp " + args.mother_directory + "/" + fileR2 + " " + o_folder + "/" + fileR2)
							
									#r = os.system("qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path /home/charlotte/Try_QIIME_2/Sequences/fileR1 --source-format CasavaOneEightSingleLanePerSampleDirFmt --output-path o_folder/demux.qza")
									
									os.chdir(o_folder)
#extract R1 or R2
									#for root, dirs, files in os.walk(o_folder):
									#	for file in files:
									#		R12 = re.search("(.*)_(.*)_(.*)_(.*)_(.*).fastq.gz",file)
									#		r12 = R12.group(4)
									#		print(r12)

#convert fastq.gz files into qza files
									r = os.system("qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path $PWD --source-format CasavaOneEightSingleLanePerSampleDirFmt --output-path " + o_folder + "/demux.qza")

									#os.makedirs(o_folder + "/" + "filtered sequences")
									#os.makedirs(o_folder + "/filtered_sequences")
									#q = os.system("qiime quality-filter q-score --i-demux " + o_folder + "/demux.qza --p-min-quality 10 --o-filtered-sequences " +o_folder + "/filtered_sequences/filtered_seq.qza --o-filter-stats " + o_folder + "/filtered_sequences/filtered_stats.qza")

# problem: I cannot know the result of this filtering step

									#d= os.system("qiime dada2 denoise-paired --i-demultiplexed-seqs " + o_folder + "/demux.qza --p-trim-left-r 0 --p-trim-left-f 0 --p-trunc-len-f 0 --p-trunc-len-r 0 --p-chimera-method consensus --o-table " + o_folder + "/table.qza --o-representative-sequences " + o_folder + "/rep-seqs.qza --o-denoising-stats " + o_folder + "/denoising-stats.qza")

###################################################################### TO INSERT ####################################################################################
#import Anopheles gambiae sequence
#put the fasta file in mother directory!!!!!
#									anopheles = os.system("qiime tools import --input-path " + args.mother_directory + "/result_1.fasta --output-path " + args.mother_directory + "/result_1.qza --type 'FeatureData[Sequence]'")


#separate Anopheles gambiae sequences from the rest
#									exclude = os.system("qiime quality-control exclude-seqs --i-query-sequences " + o_folder + "/rep-seqs.qza --i-reference-sequences " + args.mother_directory + "/result_1.qza --p-method blast --p-perc-identity 0.97 --p-perc-query-aligned 0.80 --o-sequence-hits " + o_folder + "/seq_anopheles_1.qza --o-sequence-misses " + o_folder + "/seq_exclude_anopheles_1.qza")

######################################################################################################################################################################



