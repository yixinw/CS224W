'''
This file reads in the community file, finds all abstract associated with this community, and extracts tf-idf feature for each community.
'''

from extract_feature_util import *
import numpy as np

data_dir = '../data/'
community_filename = '2_cmtyvv.txt'
abstract_filename = 'title'
id_to_abstract_line_filename = 'id_to_abstract_line'
tfidf_filename = 'community_tfidf'

# Extract tf-idf features.
features, dictionary, vocabulary = extract_tfidf(data_dir=data_dir,
        community_filename=community_filename,
        abstract_filename=abstract_filename,
        id_to_abstract_line_filename=id_to_abstract_line_filename)

# Order tf-idf features by weights.
# features is 100 x 44305 sparse matrix.
num_top_words = 500
num_top_community = 30
num_community, vocabulary_size = features.shape
community_top_words = []

for community_id in range(num_top_community):
    community_words_weight = features[community_id]
    top_word_index = np.argsort(community_words_weight.toarray()[0])[-num_top_words:]
    community_top_words.append([dictionary[i] for i in top_word_index[::-1]])

write_tfidf_file(data_dir+tfidf_filename, community_top_words)

#np.save("top.npy", community_top_words)


