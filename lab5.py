import copy
import collections
import itertools

class Formula(object):
    def __init__(self):
        self.clauses = []
        self.model = []

    ## Read formula in DIMACS CNF format
    def readcnf(self,fp):
        raw = fp.readlines()
        lines = []
        for line in raw:
            line = line.strip()
            if line != "" and line[0] != 'c':
                lines.append(line);

        _,_,n,m = lines[0].split()
        n, m = int(n), int(m)
        del lines[0]
        
        self.clauses = [[]]*m

        for i in range(m):
            self.clauses[i] = map(int,lines[i].split(" ")[:-1]);

    ## Assign a variable to make lit true
    def assign(self,lit):
        ## Remove clauses satisfied when lit = true
        self.clauses = filter(lambda clause: lit not in clause,self.clauses)

        ## Remove false literals where -lit = false
        for i in range(len(self.clauses)): self.clauses[i] = [l for l in self.clauses[i] if l != -lit]

        ## Add lit to model
        self.model.append(lit);

    ## Find a unit clause
    def unit(self):
        if 1 in map(len,self.clauses):
            return self.clauses[map(len,self.clauses).index(1)][0];        
        else: return None

    ## Find a pure literal
    def pure(self):
        lits = set([lit for clause in self.clauses for lit in clause])
        for lit in lits:
            if -lit not in lits: return lit
        return None

    ## Is this formula a tautology? 
    def istrue(self):
        return len(self.clauses) == 0

    ## Is this formula a contradiction?
    def isfalse(self):
        return [] in self.clauses


class Solver(object):
    def __init__(self):
        self.nodes = 0

    ## Unit propagation
    def unit_propagation(self,F):
        ### ... YOU FILL THIS IN ...
        one=F.unit()
        if one!=None: 
            F.assign(one) #if unit value is not found then assign a valut to the literal
        
        while F.unit() !=None: #Assign values to the unit literals that have yet not been assigned values
            self.unit_propagation(F)
        
    ## Pure literal rule        
    def solve_pure_literals(self,F):
        ### ... YOU FILL THIS IN ...
        pure_literal=F.pure()
        if pure_literal!=None:
            F.assign(pure_literal)
        
        while F.pure()!=None:
            self.solve_pure_literals(F) #Assign values to the pure literals that have yet not been assigned values

    ## Pick literal to branch
    def dpll_branch(self,F):
        ### ... YOU FILL THIS IN ...
        #a=F.clauses()
        flatten_list=list(itertools.chain(*F.clauses))
        counter=collections.Counter(flatten_list)
        #print(counter)
        #print(counter.values())
        #print(counter.keys())
        max_val=counter.most_common(1)
        #print(max_val[0][0])
        return max_val[0][0]
        
    ## Main DPLL routine
    def dpll(self,F):
        ## Add this call to search node counter
        self.nodes = self.nodes+1

        ## YOU FILL THE FOLLOWING IN        
        ## 1. Perform unit propagation
        self.unit_propagation(F)
        ## 2. Apply pure literal rule
        self.solve_pure_literals(F)
        ## 3. Check for satisfiability or contradiction (and return if necessary)
        if F.istrue():
            return True
        if F.isfalse():
           return False
        ## 4. Pick the branching literal
        lit=self.dpll_branch(F)
        ## 5. Make recursive calls on branches (hint: make copies of F)
        F_copy1=Formula()
        F_copy2=Formula()
        F_copy1.clauses=list(F.clauses)
        F_copy2.clauses=list(F.clauses)
        F_copy1.clauses.append([lit])
        F_copy2.clauses.append([-lit])
        return self.dpll(F_copy1) or self.dpll(F_copy2)

    def solve(self,filename):
        ## Open file and read into formula structure
        fp = open(filename,'r')
        F = Formula()
        F.readcnf(fp)
        fp.close()
        
        ## Reset node counter
        self.nodes = 0

        ## Solve formula
        status = self.dpll(F)

        ## Output result
        print filename,"\t",status,"\t",self.nodes

s = Solver()
s.solve("Formulas/formula01.cnf")