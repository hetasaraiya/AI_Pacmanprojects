#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation

def BT(L, M):
    "*** YOUR CODE HERE ***"
    " To find position of marks for length L and number of marks M we first assign first mark at 0 and last mark at L"
    Marks=[0]*M
    Assigned=[False]*M
    Assigned[0]=True
    Assigned[M-1]=True
    Marks[M-1]=L
    " Value of M is checked because if M<2 we can get values directly."
    if M>2:
        " All the marks which have not been assigned value have [1,..L-1] in their domain."
        Domain=[0]*M
        for i in range(1,M-1):
            Domain[i]=[]
            for j in range(1,L):
                Domain[i].append(j)
        " We check for given M and L does Golomb ruler exists, if yes then BackTracking function will return 1."
        if BackTracking(Marks,Assigned,M,L,1,Domain)==1:
            """ For finding optimal Golomb ruler we iterate for all lengths 
            from L-1 to M such that if we find golomb ruler for lesser length then that will be the ruler we return."""
            L1=L-1
            while(L1>M):
                Marks1=[0]*M
                Assigned1=[False]*M
                Marks1[M-1]=L1
                Assigned1[0]=True
                Assigned1[M-1]=True
                Domain=[0]*M
                for i in range(1, M-1):
                    Domain[i] = []
                    for j in range(1, L1):
                        Domain[i].append(j)
                if BackTracking(Marks1,Assigned1,M,L1,1,Domain)==1:
                    Marks=Marks1
                    L=L1
                    L1=L1-1
                else:
                    L1=L1-1
            return L,Marks
        else:
            return -1,[]
    elif M==2 and L>0:
        " If we have only 2 marks and L>0 then golomb ruler will exist and the optimum ruler will be of length 1."
        Marks[M-1]=1
        return 1,Marks
    else:

        if M==1 and L==0:
            return 0,[0]
        return -1,[]

def BackTracking(Marks,Assigned,M,L,No_Mark,Domain):
    """ If we are trying to assign again to first mark then it is not valid and so we return -1. But when we try for
    last assignment then all marks will have valid assignments, so we return 1.
    """
    if No_Mark==0:
        return -1
    if No_Mark==M-1:
        return 1
    for value in Domain[No_Mark]:
        " For all values in domain of current mark if the value is less than previously assigned mark, then ignore it."
        if value<Marks[No_Mark-1]:
            continue
        Marks[No_Mark]=value
        Assigned[No_Mark]=True
        OK=True
        "  We check if given assignment will give different differences or not."
        if all_difference(Marks,Assigned,M):
            OK=True
        else:
            OK=False
        if OK:
            " If this assignment doesn't violate constraints, then we find solution for next mark."
            t=BackTracking(Marks,Assigned,M,L,No_Mark+1,Domain)
            if t==-1:
                " If next mark cannot have value for current assignment then we backtrack."
                Assigned[No_Mark]=False
                continue
            else:
                return t
    Assigned[No_Mark]=False
    return -1

def all_difference(Marks,Assigned,M):
    difference=[]
    """ Take all marks which have been already assigned value and find differences between them,
    if we get same difference for any two pairs of marks then return False else return True."""
    for i in range(M):
        for j in range(i+1,M):
            if Assigned[i] and Assigned[j]:
                dif=abs(Marks[j]-Marks[i])
                if dif in difference:
                    return False
                difference.append(dif)
    return True

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    " To find position of marks for length L and number of marks M we first assign first mark at 0 and last mark at L"
    Marks = [0] * M
    Assigned = [False] * M
    Assigned[0] = True
    Assigned[M - 1] = True
    Marks[M - 1] = L
    " Value of M is checked because if M<2 we can get values directly."
    if M > 2:
        " All the marks which have not been assigned value have [1,..L-1] in their domain."
        Domain = [0] * M
        for i in range(1, M-1):
            Domain[i] = []
            for j in range(1, L):
                Domain[i].append(j)
        " We check for given M and L does Golomb ruler exists, if yes then BackTracking_FC function will return 1."
        if BackTracking_FC(Marks, Assigned, M, L, 1, Domain) == 1:
            """ For finding optimal Golomb ruler we iterate for all lengths 
            from L-1 to M such that if we find golomb ruler for lesser length then that will be the ruler we return."""
            L1 = L - 1
            while (L1 > M):
                Marks1 = [0] * M
                Assigned1 = [False] * M
                Marks1[M - 1] = L1
                Assigned1[0] = True
                Assigned1[M - 1] = True
                Domain = [0] * M
                for i in range(1, M-1):
                    Domain[i] = []
                    for j in range(1, L1):
                        Domain[i].append(j)
                if BackTracking_FC(Marks1, Assigned1, M, L1, 1, Domain) == 1:
                    Marks = Marks1
                    L = L1
                    L1 = L1 - 1
                else:
                    L1=L1-1
            return L,Marks
        else:
            return -1, []
    elif M == 2 and L>0:
        " If we have only 2 marks and L>0 then golomb ruler will exist and the optimum ruler will be of length 1."
        Marks[M - 1] = 1
        return 1, Marks
    else:
        if M == 1 and L == 0:
            return 0, [0]
        return -1, []


def BackTracking_FC(Marks, Assigned, M, L, No_Mark, Domain):
    """ If we are trying to assign again to first mark then it is not valid and so we return -1. But when we try for
        last assignment then all marks will have valid assignments, so we return 1.
    """
    if No_Mark == 0:
        return -1
    if No_Mark == M - 1:
        return 1
    for value in Domain[No_Mark]:
        " For all values in domain of current mark if the value is less than previously assigned mark, then ignore it."
        if value < Marks[No_Mark - 1]:
            continue
        Marks[No_Mark] = value
        Assigned[No_Mark] = True
        OK = True
        "  We check if given assignment will give different differences or not."
        if all_difference(Marks, Assigned, M):
            OK = True
        else:
            OK = False
        if OK:
            """ If this assignment doesn't violate constraints, then we first do forward checking for remaining marks.
             If we find a mark which doesn't have any legal values after this assignment, then we backtrack."""
            Domain_Updated=Domain[:]
            no_legal_values=False
            for j in range(No_Mark+1,M-1):
                Domain_Updated[j]=forward_checking(Marks,Assigned,M,Domain_Updated[j])
                if len(Domain_Updated[j])==0:
                    no_legal_values=True
                    break
            if no_legal_values:
                Assigned[No_Mark]=False
                continue
            t = BackTracking_FC(Marks, Assigned, M, L, No_Mark + 1, Domain_Updated)
            if t == -1:
                " If next mark cannot have value for current assignment then we backtrack."
                Assigned[No_Mark] = False
                continue
            else:
                return t
    Assigned[No_Mark] = False
    return -1


def forward_checking(Marks,Assigned,M,Domain):
    """ Take all marks which have been already assigned value and find differences between them.
    Once we find the differences we check that for we check which values of domain satisfy the constraint. We return
    this values. """
    difference=[]
    delete=[]
    for i in range(M):
        for j in range(i+1,M):
            if Assigned[i] and Assigned[j]:
                dif=abs(Marks[j]-Marks[i])
                difference.append(dif)
    for i in range(M):
        if Assigned[i]:
            for value in Domain:
                dif=abs(Marks[i]-value)
                if dif in difference:
                    if value not in delete:
                        delete.append(value)

    for value in delete:
        Domain=[x for x in Domain if x!=value]
    return Domain


#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

#sol,mar=BT(6,4)
sol,mar=FC(6,4)


if sol==-1:
    print "No Solution"
else:
    print "Minimum length:",sol
    print "Marker Position",mar