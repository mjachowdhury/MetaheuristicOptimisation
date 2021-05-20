
import sys

def readInstance(fName):
    file        = open(fName, 'r')
    tVariables  = -1
    tClauses    = -1
    clause      = []
    variables   = []

    current_clause = []

    for line in file:
        data = line.split()

        if len(data) == 0:
            continue
        if data[0] == 'c':
            continue
        if data[0] == 'p':
            tVariables  = int(data[2])
            tClauses    = int(data[3])
            continue
        if data[0] == '%':
            break
        if tVariables == -1 or tClauses == -1:
            print ("Error, unexpected data")
            sys.exit(0)

        ##now data represents a clause
        for var_i in data:
            literal = int(var_i)
            if literal == 0:
                clause.append(current_clause)
                current_clause = []
                continue
            var = literal
            if var < 0:
                var = -var
            if var not in variables:
                variables.append(var)
            current_clause.append(literal)

    if tVariables != len(variables):
        print ("Unexpected number of variables in the problem")
        print ("Variables", tVariables, "len: ",len(variables))
        print (variables)
        sys.exit(0)
    if tClauses != len(clause):
        print ("Unexpected number of clauses in the problem")
        sys.exit(0)
    file.close()
    return [variables, clause]

def readSolution(fName):
    file = open(fName, 'r')
    my_vars = {}
    for line in file:
        data = line.split()

        #print data
        if len(data) == 0:
            continue
        if data[0] == 'c':
            continue
        if data[0] == 'v':
            del data[0]
        for literal in data:
            literal = int(literal)
            if literal == 0:
                break
            var = literal
            if var < 0:
                my_vars[-var] = 0
            else:
                my_vars[var] = 1
    file.close()
    return my_vars

def solutionStatus(instance, sol):
    clause = instance[1]
    unsat_clause = 0
    for clause_i in clause:
        cStatus = False
        tmp = []
        for var in clause_i:
            if var < 0:
                if (1 - sol[-var]) == 1:
                    cStatus = True
                tmp.append([var, sol[-var]])
            else:
                tmp.append([var, sol[var]])
                if sol[var] == 1:
                    cStatus = True
        if not cStatus:
            unsat_clause+=1
    if unsat_clause > 0:
        print ("UNSAT Clauses: ",unsat_clause)
        return False
    return True


#usage
#python ParseInstance.py [instance-file] [sol-file]
#python ParseInstance.py uf20-01.cnf 1.txt

print ("File: ",sys.argv[1])
print ("Sol File: ",sys.argv[2])
sat = readInstance(sys.argv[1])

print ("Total Clauses: ",len(sat[1]))
sol = readSolution(sys.argv[2])
print (sol)

print ("Status: ",solutionStatus(sat, sol) )


