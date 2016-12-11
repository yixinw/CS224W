'''
This file contains some util functions for extracting community detection output from BigCLAM.
'''

def get_community_members(community_filepath):
    community_member_list = []
    with open(community_filepath, 'r') as f:
        for community_line in f:
            community_members = \
                    [int(x) for x in \
                    community_line.strip("\n").strip("\t").split("\t")]
            community_member_list.append(community_members)
    return community_member_list

def get_yearly_paper(yearly_filepath):
    year_to_id_map = {}
    with open(yearly_filepath, 'r') as f:
        for line in f:
            year_paper_list_pair = line.strip("\n").split(' ')
            str_year = year_paper_list_pair[0]
            if str_year != 'None':
                year = int(str_year)
                paper_list_string = year_paper_list_pair[1]
                paper_list = paper_list_string.split(',')
                paper_list = [int(x) for x in paper_list]
                year_to_id_map[year] = paper_list
    return year_to_id_map
