'''
A class describing each paper.
'''

class Paper(object):

    def __init__(self):
        self.title = None
        self.authors = []
        self.year = None
        self.venue = None
        self.index = None
        self.id = None
        self.ref = []
        self.abstract = None

'''
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract
'''
