'''
This file reads in the community file, finds all abstract associated with this community, and extracts tf-idf feature for each community.
'''

from extract_feature_util import *
import numpy as np
import extract_community_util

data_dir = '../data/'
community_filename = '2_cmtyvv.txt'
abstract_filename = 'title'
id_to_abstract_line_filename = 'id_to_abstract_line'
tfidf_filename = 'community_tfidf'
yearly_filepath = 'yearly_paper'

# Extract paper id for every year.
year_paper_map = \
        extract_community_util.get_yearly_paper(
                data_dir+yearly_filepath)
print sorted(year_paper_map.keys())

# Some constants on yearly information.
time_window_size = 5
start_year = 1951
stop_year = 2015
# Some constants on feature config.
num_top_words = 500
num_top_community = 30

'''

for year_range_start in \
        xrange(start_year, stop_year+1, time_window_size):
    year_range_stop = year_range_start + time_window_size
    yearly_paper = []
    for year in xrange(year_range_start, year_range_stop):
        yearly_paper += year_paper_map[year]
    yearly_paper_dict = dict.fromkeys(yearly_paper)

    # Extract tf-idf features.
    features, dictionary, vocabulary = \
            extract_tfidf(data_dir=data_dir,
                    community_filename=community_filename,
                    abstract_filename=abstract_filename,
                    id_to_abstract_line_filename=id_to_abstract_line_filename,
                    year_filter=yearly_paper_dict)

    # Order tf-idf features by weights.
    # features is 100 x 44305 sparse matrix.
    num_community, vocabulary_size = features.shape
    community_top_words = []

    for community_id in range(num_top_community):
        community_words_weight = features[community_id]
        top_word_index = np.argsort(community_words_weight.toarray()[0])[-num_top_words:]
        community_top_words.append([dictionary[i] for i in top_word_index[::-1]])

    write_tfidf_file(data_dir+tfidf_filename+'_'+str(year_range_start)+'_'+str(year_range_stop), community_top_words)

'''

# Extract tf-idf features.
features, dictionary, vocabulary = \
        extract_tfidf(data_dir=data_dir,
                community_filename=community_filename,
                abstract_filename=abstract_filename,
                id_to_abstract_line_filename=id_to_abstract_line_filename,
                year_filter=None)

# Order tf-idf features by weights.
# features is 100 x 44305 sparse matrix.
num_community, vocabulary_size = features.shape
community_top_words = []

for community_id in range(num_top_community):
    community_words_weight = features[community_id]
    top_word_index = np.argsort(community_words_weight.toarray()[0])[-num_top_words:]
    community_top_words.append([dictionary[i] for i in top_word_index[::-1]])

write_tfidf_file(data_dir+tfidf_filename, community_top_words)
