'''
This file implements tf-idf feature extraction.
If we have time, we need to revise the interface so that
it does not take in filenames.
'''

from sklearn.feature_extraction.text import *
import linecache

def extract_tfidf(data_dir,
        community_filename,
        abstract_filename,
        id_to_abstract_line_filename):

    id_to_abstract_line_map = {}
    with open(data_dir + id_to_abstract_line_filename, 'r') as id_to_abstract_line_file:
        for id_to_abstract_line in id_to_abstract_line_file:
            pair = id_to_abstract_line.strip("\n").split(",")
            id = int(pair[0])
            abstract_line = int(pair[1])
            id_to_abstract_line_map[id] = abstract_line

    with open(data_dir + community_filename, 'r') as community_file:
        # Extract text content.
        # A list that stores the concatenated abstract of
        # each community. Community ID correspond to list index.
        all_community_abstract = []
        for community_line in community_file:
            community_members = \
                    [int(x) for x in community_line.strip("\n").strip("\t").split("\t")]
            abstract_list = []
            for member_id in community_members:
                if member_id in id_to_abstract_line_map:
                    abstract_line_number = id_to_abstract_line_map[member_id]
                    abstract = linecache.getline(
                            data_dir+abstract_filename,
                            abstract_line_number)
                    abstract_list.append(abstract.strip("\n"))
            all_community_abstract.append(' '.join(abstract_list))
        # Count words and extract tf-idf features.
        vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        word_count = vectorizer.fit_transform(all_community_abstract)
        dictionary = [x for x in vectorizer.get_feature_names()]
        vocabulary = vectorizer.vocabulary_
        return word_count, dictionary, vocabulary

def read_tfidf_file(filename):
    community_words = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip("\n").strip(' ')
            words = line.split(' ')
            community_words.append(words)
    return community_words

def write_tfidf_file(filename, community_top_words):
    f_out = open(filename, 'w')
    for words in community_top_words:
        for w in words:
            f_out.write(w + " ")
        f_out.write("\n")
    f_out.close()

