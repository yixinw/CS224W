from collections import Counter
from paper import Paper
import extract_community_util

'''
This function extracts community members. It should go to util.py.
'''

data_dir = '../data/'
community_filename = '2_cmtyvv.txt'
data_filename = 'citation-acm-v8.txt'

community_member_list = extract_community_util.get_community_members(data_dir + community_filename)

num_top_communities = 30
community_conf_counter_list = []
id_to_community = {}
for communityId in range(num_top_communities):
    community_conf_counter_list.append(Counter())
    for nodeId in community_member_list[communityId]:
        if nodeId not in id_to_community:
            id_to_community[nodeId] = [communityId]
        else:
            id_to_community[nodeId].append(communityId)

# Sequentially parse every paper.
with open(data_dir + data_filename, 'r') as f:
    paper = Paper()
    id_counter = 0
    for line in f:
        line = line.strip("\n")
        # Write out when we have reached the end of a paper.
        # TODO: Remove this early-breaking line.
        # if id_counter == 30000:
        #     break
        if len(line) == 0 or line[0] != '#':
            if id_counter % 10000 == 0:
                print "Parsed file", id_counter
            # Update conference counter for community.
            if id_counter in id_to_community:
                for communityId in id_to_community[id_counter]:
                    community_conf_counter_list[communityId][paper.venue] += 1
            paper = Paper()
            id_counter += 1
            continue
        if line[1] == 'c':
            paper.venue = line[2:]

# Count the most frequent conference for each community.
community_top_conf = []
num_top_conf = 20
for counter in community_conf_counter_list:
    community_top_conf.append(counter.most_common(num_top_conf))
#print community_top_conf

# Write to file.
f_out = open('../data/community_conference', 'w')
for c in community_top_conf:
    for conf in c:
        f_out.write(conf[0] + ",")
    f_out.write("\n")
f_out.close()
