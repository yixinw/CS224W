'''
This file calculates the variance of key words under word embedding representation.
'''

import extract_feature_util
import numpy as np
import extract_community_util
import matplotlib.pyplot as plt
import wor2vec_util

def compute_mean_cosine_distance(m1, m2):
    # Normalize each column.
    col_norm = np.linalg.norm(m1, axis=0)
    m1 = m1 / col_norm
    col_norm = np.linalg.norm(m2, axis=0)
    m2 = m2 / col_norm
    similarity = m1.T.dot(m2)
    mean_similarity = np.mean(similarity)
    print 1 - np.min(similarity)
    print 1 - np.max(similarity)
    return mean_similarity

data_dir = '../data/'
tfidf_filename = 'community_tfidf'
community_filename = '2_cmtyvv.txt'

# Get community keywords.
community_words = extract_feature_util.read_tfidf_file(
        data_dir + tfidf_filename)

# Extract community members.
community_member_list = extract_community_util.get_community_members(data_dir + community_filename)

num_top_communities = 30
num_top_words = 100

# Initialize empty confusion matrix.
confusion_matrix = np.empty(
        (num_top_communities, num_top_communities))
in_class_distance = 0
in_class_counter = 0
between_class_distance = 0
between_class_counter = 0

embedding, dictionary, reverse_dict = \
        wor2vec_util.load_embedding(
                'title')

for communityId in range(num_top_communities):
    print communityId
    for neighborId in range(communityId, num_top_communities):

        # Construct word matrix.
        # Each column represents a word.
        self_words = community_words[communityId]
        neighbor_words = community_words[neighborId]

        self_idx = []
        for word in self_words[:num_top_words]:
            if word in dictionary:
                self_idx.append(dictionary[word])
        self_idx = np.array(self_idx)
        self_word_matrix = embedding[self_idx, :].T

        neighbor_idx = []
        for word in neighbor_words[:num_top_words]:
            if word in dictionary:
                neighbor_idx.append(dictionary[word])
        neighbor_idx = np.array(neighbor_idx)
        neighbor_word_matrix = embedding[neighbor_idx, :].T

        mean_cosine_similarity = \
                compute_mean_cosine_distance(
                        self_word_matrix,
                        neighbor_word_matrix)
        mean_cosine_distance = 1 - mean_cosine_similarity

        # Fill in the confusion matrix.
        confusion_matrix[communityId, neighborId] = \
                mean_cosine_distance
        confusion_matrix[neighborId, communityId] = \
                mean_cosine_distance

        # Calculate average word cosine distance within class.
        if communityId == neighborId:
            in_class_distance += mean_cosine_distance
            in_class_counter += 1
        # Calculate average word cosine distance between class.
        else:
            between_class_distance += mean_cosine_distance
            between_class_counter += 1

# Calculate average cosine distance within and between classes.
in_class_distance = in_class_distance / float(in_class_counter)
between_class_distance = between_class_distance \
        / float(between_class_counter)
print in_class_distance, between_class_distance
print confusion_matrix
assert in_class_counter == num_top_communities
'''
plt.figure()
plt.clf()

plt.show()
'''
