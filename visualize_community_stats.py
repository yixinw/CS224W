import matplotlib.pyplot as plt
import numpy as np
import IPython

data_dir = '../data/'
community_filename = '2_cmtyvv.txt'

community_size_list = []
with open(data_dir + community_filename, 'r') as f:
    for line in f:
        community_members = \
                [int(x) for x in line.strip("\n").strip("\t").split("\t")]
        community_size = len(community_members)
        community_size_list.append(community_size)

hist, bin_edges = np.histogram(community_size_list)
hist = np.cumsum(hist)
x = [bin_edges[i] for i in range(bin_edges.shape[0])]
y = [0] + [hist[i] for i in range(hist.shape[0])]
# plt.plot(x, y, 'r')

print community_size_list[:30]
plt.hist(np.array(community_size_list), color='r')
plt.grid()
plt.title("Community Size")
plt.xlabel("size (in number of nodes)")
plt.ylabel("number of such community")
plt.show()
