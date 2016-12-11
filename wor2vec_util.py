
# input - word embedding file generated from all titles
# output - embedding matrix, dictionary and reverse_dictionary
# usage: embedding, dictionary, reverse_dictionary = load_embedding(filename)
# embedding - numWords by dim(=200)
# dictionary - dictionary[word] = idx
# reverse_dictionary - reverse_dictionary[idx] = word

def load_embedding(filename='title'):

    # filename = "title"
    fd = open("./" + filename + "_stemvec.txt")
    headline = fd.readline()[:-1]
    headline = headline.split(' ')
    numWords = int(headline[0])
    dim = int(headline[1])

    embedding = np.zeros([numWords, dim])
    reverse_dict = dict()
    dictionary = dict()

    print "start readind file ..."
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
    print "finish reading file ..."
    assert len(reverse_dict) == numWords

    return (embedding, dictionary, reverse_dict)

