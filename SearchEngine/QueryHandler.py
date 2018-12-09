import re
from itertools import combinations
import os
from .Indexing import InvertedIndex
class Query:
    def __init__(self):
        self.InvertedIndex=InvertedIndex()
        self.InvertedIndex.retrieveIndex()
    def queryParser(self,query):
        words=[re.sub(r'(\w)\1+', r'\1', i.lower())for i in re.findall('[a-zA-Z]+',query)]
        updatedwords=[]
        for i in words:
            try:
                updatedwords.append(self.InvertedIndex.matchdict[i])
            except:
                score=0
                word=""
                for j in self.InvertedIndex.terms:
                    val=self.InvertedIndex.lcs(i,j)
                    val=val/(len(i)+len(j)-val)
                    if val>score:
                        word=j
                        score=val
                if score>0.3:
                    updatedwords.append(word)
        return list(set(updatedwords))
    def merge(self,words):
        words=sorted(words,key=lambda x:len(self.InvertedIndex.postings[x][1]))
        ans=[]
        if words:
            ans=self.InvertedIndex.postings[words[0]][1]
        for i in words[1:]:
            val=self.InvertedIndex.postings[i][1]
            temp=[]
            j=0
            k=0
            p=len(ans)
            q=len(val)
            while j<p and k<q:
                if ans[j]<val[k]:
                    j+=1
                elif ans[j]>val[k]:
                    k+=1
                else:
                    temp.append(ans[j])
                    j+=1
                    k+=1
            ans=temp
        return ans
    def rankedRetrieval(self,words):
        p=len(words)
        rankorder=[]
        finalrank=[]
        for i in range(p,0,-1):
            subset=[list(i) for i in set(combinations(words,i))]
            rankorder.append([])
            for j in subset:
                rankorder[-1].extend(self.merge(j))
            if i!=p:
                rankorder[-1]=[j for j in list(set(rankorder[-1]))]
        for i in range(p):
            if i==0:
                finalrank.append(sorted([int(j) for j in rankorder[0]]))
                continue
            finalrank.append(sorted([int(j) for j in rankorder[i] if j not in rankorder[i-1]]))
        return finalrank
    def search(self,query):
        words=self.queryParser(query)
        results=self.rankedRetrieval(words)
        return results
    
