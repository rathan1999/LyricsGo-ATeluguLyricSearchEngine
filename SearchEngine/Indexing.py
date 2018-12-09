import os
import re 
class InvertedIndex:
    matchdict=dict()
    terms=[]
    postings=dict()
    def retrieveIndex(self,termspath='terms.txt',postingspath='postings.txt',matchdictpath='matchdict.txt'):
        f=open(termspath,'r')
        data=f.read().split("\n")
        f.close()
        self.terms=[i for i in data if i]
        g=open(postingspath,'r')
        data=g.read().split('\n')
        g.close()
        self.postings=dict()
        for i in data:
            if not(i):
                break
            val=i.split(',')
            self.postings[val[0]]=[[val[1]],val[2:]]
        h=open(matchdictpath,'r')
        data=h.read().split('\n')
        self.matchdict=dict()
        h.close()
        for i in data:
            if not(i):
                break
            val=i.split(',')
            self.matchdict[val[0]]=val[1]
    def createIndex(self,path):
        data=[]
        p=[]
        for i in os.listdir(path):
            f=open(path+'\\'+i)
            s=f.read()
            f.close()
            words=[re.sub(r'(\w)\1+', r'\1', i.lower())for i in re.findall('[a-zA-Z]+',s)]
            data.append(words)
            p.extend(words)
        p=sorted(list(set(p)))
        self.terms=[p[0]]
        self.matchdict={p[0]:p[0]}
        for i in p[1:]:
            val=self.lcs(self.terms[-1],i)
            score=val/(len(self.terms[-1])+len(i)-val)
            if score <=0.5:
                self.terms.append(i)
                self.matchdict[self.terms[-1]]=self.terms[-1]
            else:
                self.matchdict[i]=self.matchdict[self.terms[-1]]
        self.postings=dict()
        for i in range(len(data)):
            changed=[self.matchdict[j] for j in data[i]]
            changed=sorted(list(set(changed)))
            for j in changed:
                try:
                    self.postings[j][0][0]=self.postings[j][0][0]+1
                    self.postings[j][1].append(i)
                except:
                    self.postings[j]=[[1],[i]]
    def lcs(self,X , Y):  
        m = len(X) 
        n = len(Y) 
        L = [[None]*(n+1) for i in range(m+1)] 
        for i in range(m+1): 
            for j in range(n+1): 
                if i == 0 or j == 0 : 
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]: 
                    L[i][j] = L[i-1][j-1]+1
                else: 
                    L[i][j] = max(L[i-1][j] , L[i][j-1]) 
        return L[m][n]
    def saveIndex(self):
        print(os.curdir)
        f=open('terms.txt','w')
        for i in self.terms:
            f.write(i+'\n')
        f.close()
        g=open('matchdict.txt','w')
        for i in self.matchdict:
            g.write(i+','+self.matchdict[i]+'\n')
        g.close()
        h=open('postings.txt','w')
        for i in sorted(list(self.postings)):
            h.write(i+','+str(self.postings[i][0][0])+','+','.join(str(j) for j in self.postings[i][1])+'\n')
        h.close()
    
    
    

    
            
