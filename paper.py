'''
A class describing each paper.
'''

class Paper(object):

    def __init__(self, title=None, authors=[], \
            year=None, venue=None, id=None, ref=[], abstract=None):
        self.title = title
        self.authors = authors
        self.year = year
        self.venue = venue
        self.id = id
        self.ref = ref
        self.abstract = abstract

'''
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract
'''
