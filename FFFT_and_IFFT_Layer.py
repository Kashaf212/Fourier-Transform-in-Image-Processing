import cmath
from math import log, ceil
import numpy as np

## Utils

def omega(p, q):
    ''' The omega term in DFT and IDFT formulas'''
    return cmath.exp((2.0 * cmath.pi * 1j * q) / p)

def pad(lst):
    '''padding the list to next nearest power of 2 as FFT implemented is radix 2'''
    k = 0
    while 2**k < len(lst):
        k += 1
    return np.concatenate((lst, ([0] * (2 ** k - len(lst)))))

def pad2(x):
    m, n = np.shape(x)
    M, N = 2 ** int(ceil(log(m, 2))), 2 ** int(ceil(log(n, 2)))
    F = np.zeros((M,N), dtype = x.dtype)
    F[0:m, 0:n] = x
    return F, m, n

                         ### FAST FOURIER TRANSFORM  ###

### FFT-1D
def fft(x):
    ''' FFT of 1-d signals
    usage : X = fft(x)
    where input x = list containing sequences of a discrete time signals
    and output X = dft of x '''

    n = len(x)
    if n == 1:
        return x
    Feven, Fodd = fft(x[0::2]), fft(x[1::2])
    combined = [0] * n
    for m in range(n//2):
        combined[m] = Feven[m] + omega(n, -m) * Fodd[m]
        combined[m + n//2] = Feven[m] - omega(n, -m) * Fodd[m]
    return combined

## FFT-2D

def fft2(f):
    '''FFT of 2-d signals/images with padding
    usage X, m, n = fft2(x), where m and n are dimensions of original signal'''

    f, m, n = pad2(f)
    return np.transpose(fft(np.transpose(fft(f)))), m, n

                        ### INVERSE FAST FOURIER TRANSFORM  ###

### IFFT-1D
def ifft(X):
    ''' IFFT of 1-d signals
    usage x = ifft(X)
    unpadding must be done implicitly'''

    x = fft([x.conjugate() for x in X])
    return [x.conjugate()/len(X) for x in x]

### IFFT-2D
def ifft2(F, m, n):
    ''' IFFT of 2-d signals
    usage x = ifft2(X, m, n) with unpaded,
    where m and n are odimensions of original signal before padding'''

    f, M, N = fft2(np.conj(F))
    f = np.matrix(np.real(np.conj(f)))/(M*N)
    return f[0:m, 0:n]


### FFT-SHIFT

def fftshift(F):
    ''' this shifts the centre of FFT of images/2-d signals'''
    M, N = F.shape
    R1, R2 = F[0: M//2, 0: N//2], F[M//2: M, 0: N//2] ## top left, bottom left
    R3, R4 = F[0: M//2, N//2: N], F[M//2: M, N//2: N] ## top right, bottom right
    sF = np.zeros(F.shape,dtype = F.dtype)
    sF[M//2: M, N//2: N], sF[0: M//2, 0: N//2] = R1, R4 ## Swap top-left ↔ bottom-right
    sF[M//2: M, 0: N//2], sF[0: M//2, N//2: N]= R3, R2 ## Swap top-right ↔ bottom-left
    return sF

def ifftshift(F):
    ''' This reverses the FFT shift operation (moves low frequencies back to corners) '''
    M, N = F.shape
    p, q = M // 2, N // 2  # Compute the midpoint

    # Swap quadrants back to original positions
    sF = np.zeros_like(F, dtype=F.dtype)
    sF[:p, :q] = F[p:, q:]  # Move bottom-right to top-left
    sF[p:, q:] = F[:p, :q]  # Move top-left to bottom-right
    sF[:p, q:] = F[p:, :q]  # Move bottom-left to top-right
    sF[p:, :q] = F[:p, q:]  # Move top-right to bottom-left

    return sF





