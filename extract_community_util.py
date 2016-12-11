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
