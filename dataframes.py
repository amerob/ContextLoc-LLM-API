import pandas as pd
from fuzzywuzzy import fuzz
from doublemetaphone import doublemetaphone


class locDataFrame:
    def __init__(self):
        # self.countrydf = pd.read_csv('countriesName.csv')
        # self.statedf = pd.read_csv('statesName.csv')
        # self.citydf = pd.read_csv('Names.csv')
        self.df = pd.read_csv('Names.csv')

    def insert(self, name, inputType):
        if name not in self.df['name'].values and inputType == 'city':
            new = {"name": name, "Alternate Names": name,
                   "city": 1, "state": 0, "country": 0}
            print("**********Inserted Successfully|||||||||||||||||||||||")
        elif name not in self.df['name'].values and inputType == 'state':
            new = {"name": name, "Alternate Names": name,
                   "city": 0, "state": 1, "country": 0}
            print("**********Inserted Successfully|||||||||||||||||||||||")
        elif name not in self.df['name'].values and inputType == 'country':
            new = {"name": name, "Alternate Names": name,
                   "city": 0, "state": 0, "country": 1}
            print("**********Inserted Successfully|||||||||||||||||||||||")
        self.df = self.df._append(new,ignore_index=True)
        self.df.to_csv('Names.csv',index = False)

    def delete(self, name):
        if name in self.df['name'].values:
            index_to_drop = self.df[(self.df['name'] == name)].index
            self.df = self.df.drop(index_to_drop).reset_index(drop=True)
            print("**********Deleted Successfully|||||||||||||||||||||||")
            self.df.to_csv('Names.csv',index = False)

    def spellCheck(self,word):
        names = self.df[name]
    def findy(self,word):
        if word in self.df['name'].values:
            return True
        else:
            return False
        
    def findMulti(self,words):
        l = []
        for w in words:
            if w in self.df['name'].values:
                l.append(w)
            else:
                l.append('NA')