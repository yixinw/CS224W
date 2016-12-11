'''
This file reads in the data file line by line and parse it.
'''

from paper import Paper
import re
from nltk.stem import *

data_dir = '../data/'
data_filename = 'citation-acm-v8.txt'

index_id_map = {}
adjacent_matrix = []
paper_list = []
paper_abstract_we_care = {}
# Set this to true if we actually want to write abstract
# of every paper in graph to a huge file. This may significantly
# slow down the parsing process.
write_to_abstract_file = False
write_to_title_file = True
id_to_abstract_line = []
stemmer = PorterStemmer()
title_file_content_list = []

# Sequentially parse every paper.
with open(data_dir + data_filename, 'r') as f:
    paper = Paper()
    id_counter = 0
    abstract_line_counter = 0
    for line in f:
        line = line.strip("\n")
        # Write out when we have reached the end of a paper.
        # TODO: Remove this early-breaking line.
        #if id_counter == 1000:
        #    break
        if len(line) == 0 or line[0] != '#':
            if id_counter % 10000 == 0:
                print "Parsed file", id_counter
            # Write to file.
            if paper.index in paper_abstract_we_care and paper.abstract is not None:
                if write_to_abstract_file:
                    f_out = open('../data/abstract', 'a')
                    f_out.write(paper.abstract)
                    f_out.write("\n")
                    f_out.close()
                if write_to_title_file:
                    # Lower case and stem the title.
                    title = re.sub('\W+',' ',paper.title)
                    title = title.lower()
                    title_stemmed = [stemmer.stem(word)
                            for word in title.split(' ')]
                    title_file_content_list.append(' '.join(title_stemmed))
                id_to_abstract_line.append( \
                        (paper.id, abstract_line_counter))
                abstract_line_counter += 1

            if len(paper.ref) > 0:
                paper_list.append(paper)
            paper = Paper()
            continue
        # Parse title.
        if line[1] == '*':
            paper.title = line[2:]
        # Parse authors.
        elif line[1] == '@':
            author_string = line[2:]
            author_list = author_string.split(",")
            paper.authors = [author.strip(" ") for author in author_list]
        # Parse year.
        elif line[1] == 't':
            paper.year = int(line[2:])
        # Parse publication venue.
        elif line[1] == 'c':
            paper.venue = line[2:]
        # Parse index.
        elif line[1:6] == 'index':
            paper.index = line[6:]
            paper.id = id_counter
            index_id_map[line[6:]] = id_counter
            id_counter += 1
        # Parse references.
        elif line[1] == '%':
            neighbor_index = line[2:]
            paper.ref.append(neighbor_index)
            paper_abstract_we_care[neighbor_index] = None
        # Parse abstract.
        elif line[1] == '!':
            paper.abstract = line[2:]

# Write index id map to file.
f_out = open('../data/index_id_map', 'w')
for k,v in index_id_map.iteritems():
    f_out.write(str(k) + "," + str(v) + "\n")
f_out.close()

# Write edgelist to file.
f_out = open('../data/edgelist', 'w')
for paper in paper_list:
    for neighbor in paper.ref:
        this_id = paper.id
        if neighbor in index_id_map:
            neighbor_id = index_id_map[neighbor]
            f_out.write(str(this_id) + "\t" + str(neighbor_id) + "\n")
f_out.close()

# Write to a file mapping from paper id to line number in abstract file.
f_out = open('../data/id_to_abstract_line', 'w')
for (id, line_number) in id_to_abstract_line:
    f_out.write(str(id) + "," + str(line_number) + "\n")
f_out.close()

f_out = open('../data/title', 'w')
for title in title_file_content_list:
    f_out.write(title + "\n")
f_out.close()
