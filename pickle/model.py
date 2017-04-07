#!/usr/bin/env python3
'''
Modeling users, interactions and items from
the recsys challenge 2017.

by Daniel Kohlsdorf
'''

class User:

    def __init__(self, title, clevel, indus, disc, country, region, wtcj):
        self.title   = title
        self.clevel  = clevel
        self.indus   = indus
        self.disc    = disc
        self.country = country
        self.region  = region
        self.wtcj = wtcj

class Item:

    def __init__(self, title, clevel, indus, disc, country, region, employ):
        self.title   = title
        self.clevel  = clevel
        self.indus   = indus
        self.disc    = disc
        self.country = country
        self.region  = region
        self.employ = employ

class Interaction:
    
    def __init__(self, user, item, interaction_type):
        self.user = user
        self.item = item
        self.interaction_type = interaction_type

    def title_match(self):
        return float(len(set(self.user.title).intersection(set(self.item.title))))

    def clevel_match(self):
        if self.user.clevel == self.item.clevel:
            return 1.0
        else:
            return 0.0

    def indus_match(self):
        if self.user.indus == self.item.indus:
            return 1.0
        else:
            return 0.0

    def discipline_match(self):
        if self.user.disc == self.item.disc:
            return 2.0
        else:
            return 0.0

    def country_match(self):
        if self.user.country == self.item.country:
            return 1.0
        else:
            return 0.0

    def region_match(self):
        if self.user.region == self.item.region:
            return 1.0
        else:
            return 0.0

    def student_match(self):
        if self.user.clevel==1 and (self.item.employ == 2 or self.item.employ == 4):
            return 1.0
        else:
            return 0.0
            
    def ceo_volunt_mismatch(self):
        if (self.user.clevel==6 or self.user.clevel==5) and self.item.employ == 5:
            return 0.0
        else:
            return 1.0
            
    def wtcj(self):
        return self.user.wtcj
    
    def features(self):
        return [
            self.title_match(), self.clevel_match(), self.indus_match(), 
            self.discipline_match(), self.country_match(), self.region_match(),
            self.student_match(),self.ceo_volunt_mismatch(), self.wtcj()
        ]

    def label(self): 
        if self.interaction_type == 4: 
            return 0.0
        else:
            return 1.0


