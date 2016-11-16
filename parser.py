'''
This file reads in the data file line by line and parse it.
'''

from paper import Paper
import IPython

data_dir = '../data/'
data_filename = 'citation-acm-v8.txt'

index_id_map = {}
adjacent_matrix = []
paper_list = []

# Sequentially parse every paper.
with open(data_dir + data_filename, 'r') as f:
    paper = Paper()
    id_counter = 0
    for line in f:
        line = line.strip("\n")
        # Write out when we have reached the end of a paper.
        # TODO: Remove this early-breaking line.
        if id_counter == 200:
            break
        if len(line) == 0 or line[0] != '#':
            if id_counter % 10000 == 0:
                print "Parsed file", id_counter
            if len(paper.ref) > 0:
                paper_list.append(paper)
                print "ref length:", len(paper.ref)
                print "ref id:", paper.ref
            # Write to file.
            # if paper.abstract:
            #     f_out = open('../data/abstract/'+str(paper.id), 'w')
            #     f_out.write(paper.abstract)
            #     f_out.close()
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
            paper.id = id_counter
            index_id_map[line[6:]] = id_counter
            id_counter += 1
        # Parse references.
        elif line[1] == '%':
            paper.ref.append(line[2:])
        # Parse abstract.
        elif line[1] == '!':
            paper.abstract = line[2:]

IPython.embed()

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

