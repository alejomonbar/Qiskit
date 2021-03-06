import numpy as np
from numpy import kron
def binN(ii,n):
    return bin(ii)[2:].zfill(n)

def binList(binN):
    return [int(d) for d in binN]

def listBin(lista):
    bina = ''
    for i in lista:
        bina +=str(i)
    return bina
def ptrace(p,pos):
    """
    Based on the work of Mark S. Tame.
    
    Return the partial trace of p array in position pos 

    Args:
        p(nxn): density matrix of the composite system
        pos(array): subsytems of the density matrix needed
                 Ex: p = kron(p_a,p_b)

                     p_a = ptrace(p,[1])
                     p_b = ptrace(p,[0])

                Ex: p = kron(p_a,kron(p_b,p_c))
                    p_a = ptrace(p,[1,2])
                    p_b = ptrace(p,[0,2])
                    p_c = ptrace(p,[0,1])
                    p_ab = ptrace(p,[2])

        return:
            Matrix(2,2) with the information of subsystem pos
    """
    Qubits = pos[::-1]
    TrkM = p
    z = len(pos)
    for q in range(z):
        n = int(np.log2(len(TrkM)))
        M = np.column_stack(TrkM)
        k = Qubits[q]
        if k == n-1:
            TrkM = []
            for i in range(0,2**n,2):
                TrkM.append(M[i,:][range(0,2**n,2)]+M[i+1,:][range(1,2**n,2)])
        else:
            for j in range(n-k-1):
                b = []
                for ii in range(2**n):
                    if (int(binN(ii,n)[n-1]) + int(binN(ii,n)[n-j-2])+1)%2 == 0 and b.count(ii) == 0:
                        c = [l for l in range(2**n)]
                        b.append(int(listBin(swapPos(binList(binN(ii,n)),n-1,n-j-2)),2))
                        perm = swapPos(c,ii,int(listBin(swapPos(binList(binN(ii,n)),n-1,n-j-2)),2))
                        M = M[perm,:]
                        M = M[:,perm]
            TrkM = []
            for i in range(0,2**n,2):
                TrkM.append(M[i,:][range(0,2**n,2)]+M[i+1,:][range(1,2**n,2)])
    return np.column_stack(TrkM)
