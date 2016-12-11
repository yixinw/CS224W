import IPython
import csv
import numpy as np
from nltk.stem import *
import extract_feature_util
import scipy

# 30 community top 500 words
community_keywords = extract_feature_util.read_tfidf_file("./community_tfidf")
num_community = len(community_keywords)
num_word = len(community_keywords[0])

'''
stemmer = PorterStemmer()
top = []
for community in community_keywords:
    temp = []
    for word in community:
        word_stem = stemmer.stem(word)
        temp.append(word_stem.lower())
    assert len(temp) == num_word
    top.append(temp)
assert len(top) == num_community
'''
top = community_keywords

filename = "title"
fd = open("./" + filename + "_stemvec.txt")
headline = fd.readline()[:-1]
headline = headline.split(' ')
numWords = int(headline[0])
dim = int(headline[1])

embedding = np.zeros([numWords, dim])
reverse_dict = dict()
dictionary = dict()

print "start reading files ...."
fileItr = csv.reader(fd, delimiter='\t')
idx = 0
for row in fileItr:
    row = row[0][:-1].split(' ')
    word = row[0]
    vec = np.array(row[1:])
    vec = vec.astype('float')
    reverse_dict[idx] = word
    dictionary[word] = idx
    embedding[idx,:] = vec
    idx += 1
    if idx % 5000 == 0:
        print idx

fd.close()
assert len(reverse_dict) == numWords

# clustering
def closest_community(vec, centers):
    n = centers.shape[0]
    dist = float('inf')
    community = None
    for i in range(n):
        # temp = np.sum((vec-centers[i,:])**2)
        temp = scipy.spatial.distance.cosine(vec, centers[i,:])
        if temp < dist:
            dist = temp
            community = i
    return community

top_idx = []
center_coord = np.zeros([num_community, dim])
for i in range(num_community):
    temp_idx = []
    for word in top[i]:
        if word in dictionary:
            idx = dictionary[word]
            temp_idx.append(idx)
            center_coord[i,:] += embedding[idx,:]
    top_idx.append(temp_idx)
    center_coord[i,:] /= len(temp_idx)

itr = 0
while itr < 10:
    top_idx_next = []
    center_coord_next = np.zeros([num_community, dim])
    for i in range(num_community):
        temp_idx = []
        for idx in top_idx[i]:
            if closest_community(embedding[idx,:], center_coord) == i:
                temp_idx.append(idx)
                center_coord_next[i,:] += embedding[idx,:]
        top_idx_next.append(temp_idx)
        if len(temp_idx) != 0:
            center_coord_next[i,:] /= len(temp_idx)


    itr += 1
    if top_idx_next == top_idx:
        break
    else:
        top_idx = top_idx_next[:]

fd = open("keyword_profile_30",'w')
for i in range(num_community):
    # print "for community " + str(i)
    for idx in top_idx[i]:
        # print reverse_dict[idx]
        fd.write(reverse_dict[idx]+' ')
    fd.write('\n')

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

color = [(np.random.rand(),np.random.rand(),np.random.rand()) for _ in range(num_community)]

threshold = 99
plt_vec = None
labels = []
c = []
l = []
for i in range(num_community):
    if len(top_idx[i]) < threshold:
        continue
    l.append(i)
    for idx in top_idx[i]:
        if plt_vec == None:
            plt_vec = embedding[idx:idx+1,:]
        else:
            plt_vec = np.append(plt_vec,embedding[idx:idx+1,:],axis=0)
        labels.append(reverse_dict[idx])
        c.append(color[i])
        l.append(0)
    l.pop(-1)

assert len(c) == len(l)
print len(c)

def plot_with_labels(low_dim_embs, labels, colors, l, showlabel=True, filename="tsne_"+ filename + '_' + str(threshold) +".png"):
  assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
  plt.figure(figsize=(18, 18))  # in inches
  for i, label in enumerate(labels):
    x, y = low_dim_embs[i, :]
    if l[i] != 0:
        plt.scatter(x, y, color=colors[i], label=str(l[i]))
    else:
        plt.scatter(x, y, color=colors[i])
    if showlabel:
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
  plt.legend()
  plt.savefig(filename)

tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
low_dim_embs = tsne.fit_transform(plt_vec)
plot_with_labels(low_dim_embs, labels, c, l, False)

IPython.embed()
