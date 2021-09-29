#!/usr/bin/env python
# coding: utf-8

# ## Projet Decision Tree

# In[521]:


import csv
from copy import deepcopy 


# ### Classes That we will use in the project 

# In[522]:


class node:
   
    def __init__(self):
        self.constraint = None
        self.childlist = []
        self.class_value = None
        self.level = 0
        self.gini = 1
        self.set_records = []
    
    def set_node(self, cons, childs, val=None):
        self.constraint = cons
        for i in range(len(childs)):
            self.childlist.append(childs[i])
        self.class_value = val
    
    def set_level(self,level):
        self.level = level
    
    def Gini(self,gini):
        self.gini = gini
    
    def set_records(self, set_of_records):
        self.set_records = set_of_records
    
    def set_class_value(self, class_value):
        self.class_value = class_value
        
class record:
    
    def __init__(self, attributes, class_value):
        self.attributes = attributes
        self.class_value = class_value
        
    def set_record(self, att, val):
        self.class_value = val
        self.attributes = att

class set_of_records:
    
    def __init__(self):
        self.records = []
    
    def set_records(self,record):
        self.records.append(record)
            
set_of_attributes = {"Sex":[0,1], "Pclass":[1,2,3], "Embarked":[0,1,2]}


# ### BuildDecisionTree

# In[531]:


def BuildDecisionTree(file, minNum):
    global Tree
    
    Tree = [] # list of nodes 
    D,v = ConvertData(file) # v root 
    Build(D,set_of_attributes,minNum,v,0)
    Tree.reverse()
    
    return Tree
    
    
def ConvertData(file):
    D = set_of_records()
    data_frame = csv.reader(open('./data/data.csv','r')) 
    i=0
    for row in data_frame:
        if row != ['Sex', 'Pclass', 'Embarked', 'Survived'] and i<20:
            L = [row[0],row[1],row[2]]
            i+=1
            D.set_records(record(L,row[3]))
    v = node()
    v.set_node(set_of_attributes,[],None)

    return D, v #lecture de la classe dans le dataframe
    
    
def Build(D, A, minNum, v, d):
    
    Class =[]
    
    for i in range(len(D.records)):
        if D.records[i].class_value not in Class:
            Class.append(D.records[i].class_value)
            
    if len(Class)==1:
        v.set_node(v.constraint, [], Class[0])
        Tree.append(v)
        
        return Tree
    if len(D.records)<minNum:
        v.set_node(v.constraint, [], d)
        Tree.append(v)
        
        return Tree
   
    G,n = Gini(A, D, v)

    u, w = node(), node()
    u.set_node(G[0], [])
    w.set_node(G[1], [])
    
    u.Gini(1-(G[4]/G[5])**2-((G[5]-G[4])/G[5])**2)
    
    w.Gini(1-(G[6]/G[7])**2-((G[7]-G[6])/G[7])**2)
    v.set_node(v.constraint, [u,w]) 
    
    Tree.append(v)
    
    Build(G[2], A, minNum, u, d)
    Build(G[3], A, minNum, w, d)

    
    
    
def Gini(Attributes, r, node):
    #Calcul le gini split node des noeuds fils du noeud courant
    Gain={}
    records = r.records
    n = len(records)
    c1=node.constraint.copy()
    
    for a in Attributes:
       
        if a == 'Sex' and len(node.constraint['Sex'])>1 : 
                D1,D2 = set_of_records(),set_of_records()
                nb_sexe1_survived, nb_sexe0_survived = 0,0
                nb_sexe0, nb_sexe1 = 0,0
            
                for r in records:
                    if r.attributes[0] == '1':
                        nb_sexe1+=1
                        if r.class_value == '1':
                            nb_sexe1_survived+=1
                        D1.set_records(r)
                    if r.attributes[0] == '0':
                        nb_sexe0+=1
                        if r.class_value == '1':
                            nb_sexe0_survived+=1
                        D2.set_records(r)
                
                g_sex= nb_sexe1/n*(1-(nb_sexe1_survived/nb_sexe1)**2 - ((nb_sexe1 - nb_sexe1_survived)/nb_sexe1)**2)+ (nb_sexe0)/n* (1-(nb_sexe0_survived/nb_sexe0)**2 - ((nb_sexe0-nb_sexe0_survived)/nb_sexe0)**2)
                
                c1=node.constraint.copy()
                c2=node.constraint.copy()
            
                c1['Sex']=[0]
                c2['Sex']=[1]

                Gain[g_sex]=[c1,c2,D2,D1,nb_sexe0_survived,nb_sexe0,nb_sexe1_survived,nb_sexe1]
            
        if a == 'Pclass' :
            if len(node.constraint['Pclass'])==3:
                D1_1,D2_1,D1_2,D2_2 = set_of_records(),set_of_records(),set_of_records(),set_of_records()
                nb12_survived,nb23_survived = 0,0
                nb12,nb23 = 0,0 
                nb3,nb1 = 0,0
                nb3_survived, nb1_survived = 0,0
                for r1 in records: 
                    if r1.attributes[1] == '1' or r1.attributes[1] == '2':
                        nb12+=1
                        if r1.class_value == '1':
                            nb12_survived+=1
                        D1_1.set_records(r1)
                    if r1.attributes[1] =='3':
                        nb3+=1
                        if r1.class_value =='1':
                            nb3_survived+=1
                        D2_1.set_records(r1)
                for r2 in records:
                    if r2.attributes[1] == '2' or r2.attributes[1] == '3':
                        nb23+=1
                        if r2.class_value == '1':
                            nb23_survived+=1
                        D1_2.set_records(r2)
                    if r2.attributes[1] =='1':
                        nb1+=1
                        if r2.class_value == '1':
                            nb1_survived+=1
                        D2_2.set_records(r2)
           
                g_pclass1, g_pclass2 = 1,1
            
                if nb12!=0 and nb3!=0:
                
                    g_pclass1 = nb12/n*(1-(nb12_survived/nb12)**2 - ((nb12 - nb12_survived)/nb12)**2) + ((nb3)/n)*(1-(nb3_survived/nb3)**2 -((nb3-nb3_survived)/nb3)**2)
                    
                if nb23!=0 and nb1!=0:
                
                    g_pclass2 = nb23/n*(1-(nb23_survived/nb23)**2 - ((nb23 - nb23_survived)/nb23)**2) + ((n-nb23)/n)*(1-(nb1_survived/nb1)**2 -((nb1-nb1_survived)/nb1)**2)

                c1=node.constraint.copy()
                c2=node.constraint.copy()

                if g_pclass1<g_pclass2:
            
                    c1['Pclass']=[1,2]
                    c2['Pclass']=[3]
 
                    Gain[g_pclass1]=[c1,c2,D1_1,D2_1,nb12_survived,nb12,nb3_survived,nb3]
                    
                else:
                    c1['Pclass']=[1]
                    c2['Pclass']=[2,3]
            
                    Gain[g_pclass2]=[c1,c2,D2_2,D1_2,nb1_survived,nb1,nb23_survived,nb23]

            if len(node.constraint['Pclass'])==2:
                L=node.constraint['Pclass']
                D1,D2 = set_of_records(),set_of_records()
                nb_pclass1_survived, nb_pclass0_survived = 0,0
                nb_pclass0, nb_pclass1 = 0,0
            
                for r in records:
                    if r.attributes[1] == L[0]:
                        nb_pclass1+=1
                        if r.class_value == '1':
                            nb_pclass1_survived+=1
                        D1.set_records(r)
                    if r.attributes[1] == L[1]:
                        nb_pclass0+=1
                        if r.class_value == '1':
                            nb_pclass0_survived+=1
                        D2.set_records(r)
                        
                if nb_pclass1!=0 and nb_pclass0!=0:
                    g_pclass= nb_pclass1/n*(1-(nb_pclass1_survived/nb_pclass1)**2 - ((nb_pclass1 - nb_pclass1_survived)/nb_pclass1)**2)+ (nb_pclass0)/n* (1-(nb_pclass0_survived/nb_pclass0)**2 - ((nb_pclass0-nb_pclass0_survived)/nb_pclass0)**2)
                
                    c1=node.constraint.copy()
                    c2=node.constraint.copy()
            
                    c1['Pclass']=[L[0]]
                    c2['Pclass']=[L[1]]

                    Gain[g_pclass]=[c1,c2,D1,D2,nb_pclass1_survived,nb_pclass1,nb_pclass0_survived,nb_pclass0]
        
        if a == 'Embarked':
            if len(node.constraint['Embarked'])==3:
                D1_1,D2_1,D1_2,D2_2 = set_of_records(),set_of_records(),set_of_records(),set_of_records()
                nb01_survived,nb12_survived = 0,0
                nb01,nb12 = 0,0 
                nb2,nb0 = 0,0
                nb2_survived, nb0_survived = 0,0
                for r1 in records: 
                    if r1.attributes[2] == '0' or r1.attributes[2] == '1':
                        nb01+=1
                        if r1.class_value == '1':
                            nb01_survived+=1
                        D1_1.set_records(r1)
                        
                    if r1.attributes[2] =='2':
                        nb2+=1
                        if r1.class_value =='1':
                            nb2_survived+=1
                        D2_1.set_records(r1)
                      
                for r2 in records:
                    if r2.attributes[2] == '1' or r2.attributes[2] == '2':
                        nb12+=1
                        if r2.class_value == '1':
                            nb12_survived+=1
                        D1_2.set_records(r2)
                    if r2.attributes[2] =='0':
                        nb0+=1
                        if r2.class_value == '1':
                            nb0_survived+=1
                        D2_2.set_records(r2)
            
                g_embarked1, g_embarked2 = 1,1
                
                if nb01!=0 and nb2!=0:
                
                    g_embarked1 = nb01/n*(1-(nb01_survived/nb01)**2 - ((nb01 - nb01_survived)/nb01)**2) + ((nb2)/n)*(1-(nb2_survived/nb2)**2 -((nb2-nb2_survived)/nb2)**2)
                    
                
                if nb12!=0 and nb0!=0:
                
                    g_embarked2 = nb12/n*(1-(nb12_survived/nb12)**2 - ((nb12 - nb12_survived)/nb12)**2) + ((nb0)/n)*(1-(nb0_survived/nb0)**2 -((nb0-nb0_survived)/nb0)**2)
                    
                c1=node.constraint.copy()
                c2=node.constraint.copy()

                if g_embarked1<=g_embarked2:

                    c1['Embarked']=[0,1]
                    c2['Embarked']=[2]
 
                    Gain[g_embarked1]=[c1,c2,D1_1,D2_1,nb01_survived,nb01,nb2_survived,nb2]

                else:
                    c1['Embarked']=[0]
                    c2['Embarked']=[1,2]
            
                    Gain[g_embarked2]=[c1,c2,D2_2,D1_2,nb0_survived,nb0,nb12_survived,nb12]
            
            if len(node.constraint['Embarked'])==2:
                L=node.constraint['Embarked']
                D1,D2 = set_of_records(),set_of_records()
                nb_em1_survived, nb_em0_survived = 0,0
                nb_em0, nb_em1 = 0,0
            
                for r in records:
                    if r.attributes[1] == L[0]:
                        nb_em1+=1
                        if r.class_value == '1':
                            nb_em1_survived+=1
                        D1.set_records(r)
                    if r.attributes[1] == L[1]:
                        nb_em0+=1
                        if r.class_value == '1':
                            nb_em0_survived+=1
                        D2.set_records(r)
                if nb_em1!=0 and nb_em0!=0:
                    g_em= nb_em1/n*(1-(nb_em1_survived/nb_em1)**2 - ((nb_em1 - nb_em1_survived)/nb_em1)**2)+ (nb_em0)/n* (1-(nb_em0_survived/nb_em0)**2 - ((nb_em0-nb_em0_survived)/nb_em0)**2)
                
                    c1=node.constraint.copy()
                    c2=node.constraint.copy()
            
                    c1['Embarked']=[L[0]]
                    c2['Embarked']=[L[1]]

                    Gain[g_em]=[c1,c2,D1,D2,nb_em1_survived,nb_em1,nb_em0_survived,nb_em0]
    if len(Gain)!=0:    
        for i in range(len(Gain)):
    
            if list(Gain.keys())[i]==min(list(Gain.keys())):
                
                return Gain[list(Gain.keys())[i]],n
    
    #renvoie l'attribut sur lequel on effectue le split et les C_1,...,C_k qui permettent le split k = 2 et D1


# In[598]:


T = BuildDecisionTree('./data/data.csv',6)


# ### PrintDecisionTree Function 

# In[599]:



def printDecisionTree(Tree):
    
    next_node = []
    next_node.append(Tree[-1])
    Level = 1 
    # faire le print du root 
    while next_node != []:
        node = next_node.pop(0)
        #we use '-' to split the "brothers nodes" of the other nodes
        if node == '-':
            Level +=1
            next_node = [node for node in next_node if node != '-']  
            print(" "*5)
        else:
            node_class = 0 
            Gini = 0 
            if node.constraint == {'Sex': [0, 1], 'Pclass': [1, 2, 3], 'Embarked': [0, 1, 2]}: # Root 
                
                print("Root \n Level 0 \n" + "Feature Sex 0\n Gini " + str(Gini)+"\n   ")
            elif node.class_value == None: # Intermediate 
                feature = node.childlist[0].constraint 
                
                Gini = node.gini
                 
                print("Intermediate \n Level "+ str(Level)+"\n Feature "+ str(feature)+"\n Gini "+str(Gini)+"\n ****")
            elif node.class_value != None : # Leaf 
                node_class = node.class_value
                
                Gini = node.gini 
               
                print("Leaf \n Level "+str(Level)+"\n Class "+str(node_class)+ "\n Gini "+str(Gini)+"\n ****")
            
            for child in node.childlist:
                next_node.append(child)
            next_node.append('-')
          
                


# In[600]:


printDecisionTree(T)


# In[601]:



def generalizationError(data, Tree, alpha):
    
    # return the generalization error i.e. : number of training errors + alpha*number of leaves 
    nb_error = trainingErrorDetection(data, Tree) 
    nb_leaves = 0 
    for n in Tree:
        if n.class_value !=None:
            nb_leaves+=1
    print(nb_leaves, nb_error)
    return nb_error + alpha*nb_leaves 
    
    
def trainingErrorDetection(data, Tree): # gives the number of training errors
    Nb_error = 0
    Leaf_list = []
    for n in Tree:
        if n.class_value != None:  #On teste la condition pour être une feuille 
            Leaf_list.append(n)
            
    df = csv.reader(open('./data/data.csv','r')) 
    Data = []
    i=0
    for row in df:
        if row != ['Sex', 'Pclass', 'Embarked', 'Survived'] and i<20:
            i+=1
            Data.append(row)

    # Si un element de Data a exactement les mêmes contraintes qu'une feuille mais pas la même classe, on a une erreur
    for d in Data:
        for leaf in Leaf_list:
            if int(d[0]) in leaf.constraint['Sex'] and int(d[1]) in leaf.constraint['Pclass'] and int(d[2]) in leaf.constraint['Embarked']:
                if int(leaf.class_value) != int(d[3]):
                    Nb_error +=1
    return Nb_error  


# ### PostPrune Function 

# In[606]:




def PostPrune(Tree,data,alpha,minNum):
    PostPruned_Tree = Tree
    level_set_up(PostPruned_Tree)
    #We get the max Level of the Tree 
    max_level = 0
    for n in Tree:
        if n.level > max_level:
            max_level = n.level
    
    for i in range(1,max_level):
        L = []
        #We create the list of nodes of level max_level -i (constructed like this because we go decreasingly)
        for n in PostPruned_Tree:
            if n.level == max_level-i: # we take max - i because we want to iterate in the decreasing levels order
                L.append(n)
       
        for node in L:
             
            # We create the leaf that will replace node in the algorithm 
            gen_error_P, gen_error_T = 0,0 
            gen_error_T = generalizationError(data, PostPruned_Tree,alpha)
            P = modifyTree(PostPruned_Tree, n, minNum)
            gen_error_P = generalizationError(data,P,alpha)
            if gen_error_P < gen_error_T: 
                    PostPruned_Tree = P 
    
    # We have an issue here due to our deepcopy in the modifyTree function 
    return PostPruned_Tree
            
            
# function that create the leaf that we want in the PostPrune algorithm            
def create_leaf_at_node(n, minNum):
    C = 0
    records = set_of_records_at_node(n) 
    leaf = node()
    leaf.set_records = records
            
    # Quelle est la défault classvalue ? 
    for record in records:
        if len(records)>minNum:
            if record[3] == 1: 
                C+=1
            else:
                C-=1
        else: 
            C = 0 # Défault value, est ce 0 ?? 
    if C>0:
        leaf.set_class_value(1)
    else:
        leaf.set_class_value(0)
            
    return leaf       

# Take a node v and gives the list of the records that satisfy the constraints at v
def set_of_records_at_node(node):
    set = []
    constraint = node.constraint
    df = csv.reader(open('./data/data.csv','r')) 
    Data = []
    i=0
    for row in df:
        if row != ['Sex', 'Pclass', 'Embarked', 'Survived'] and i <20:
            i+=1
            Data.append(row)
    for record in Data:
        if int(record[0]) in constraint['Sex']:
            if int(record[1]) in constraint['Pclass']:
                if int(record[2]) in constraint['Embarked']:
                    set.append(record)
    return set 


# This function will create the Three with the node replaced by a leaf 
# We have a construction problem here : we make a deepcopy which changes the address of each nodes 
#so we get when iterate over nodes in L that node is 
def modifyTree(T, node, minNum):
    P = deepcopy(T)
    leaf = create_leaf_at_node(node, minNum)
    index = T.index(node) # we keep this index so that we know where in T we can insert the leaf 
    ToDelete = [] # List of the nodes and of the leaf we must destroy (the childrens of the current node)
    ToDelete.append(P[index]) 
    n1 = P[index]
    while ToDelete != []:
        current_node = ToDelete.pop(0)
        index1 = P.index(current_node)
        del P[index1] # We delete the node from the tree
        for children in current_node.childlist: 
            ToDelete.append(children)
    for n in P: 
        if n1 in n.childlist:
            n.childlist[n.childlist.index(n1)] = leaf
    n1 = leaf #we replace the node by the leaf 
    return P

# Function that updates the level of the nodes 
def level_set_up(T):
    root = node()
    for n in T:
        if n.constraint == set_of_attributes:
            root = n
    to_update = []
    to_update.append(root)
    while to_update != []:
        v = to_update.pop(0)
        for child in v.childlist:
            child.set_level(v.level +1)
            to_update.append(child)


# In[608]:


P = PostPrune(T,'./data/data.csv',2, 6)

