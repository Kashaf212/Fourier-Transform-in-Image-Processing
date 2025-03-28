import numpy as np

## fu is the frequency domain representation of the signal
## fx is the original signal
## FFT takes fx(time domain) and converts it into fu (frequqency domain)
### IFFT takes fu and converts it back to fx

def DFT_1D(fx):
    fx = np.asarray(fx, dtype=complex)
    M = fx.shape[0]
    fu = fx.copy()

    for i in range(M):
        u = i
        sum = 0
        for j in range(M):
            x = j
            tmp = fx[x]*np.exp(-2j*np.pi*x*u*np.divide(1, M, dtype=complex))   # FT Formula to extract Frequecy information:  e ^ (-2 ((pi)i) (xu/M))
            sum += tmp
        # print(sum)
        fu[u] = sum
    # print(fu)

    return fu


def inverseDFT_1D(fu):
    fu = np.asarray(fu, dtype=complex)
    M = fu.shape[0]
    fx = np.zeros(M, dtype=complex)

    for i in range(M):
        x = i
        sum = 0
        for j in range(M):
            u = j
            tmp = fu[u]*np.exp(2j*np.pi*x*u*np.divide(1, M, dtype=complex))  ## will wirte it in readme file
            sum += tmp ## this sum is for summation in the formula
        fx[x] = np.divide(sum, M, dtype=complex)  ## Divided by M to normalize the values

    return fx


def FFT_1D(fx):
    """ use recursive method to speed up"""
    fx = np.asarray(fx, dtype=complex)
    M = fx.shape[0]
    minDivideSize = 4

    if M % 2 != 0:  ## FFT works best when the input_size is of power of 2
        raise ValueError("the input size must be 2^n")

    if M <= minDivideSize:
        return DFT_1D(fx)
    else:
        fx_even = FFT_1D(fx[::2])  # compute the even part
        fx_odd = FFT_1D(fx[1::2])  # compute the odd part
        W_ux_2k = np.exp(-2j * np.pi * np.arange(M) / M)  ## Twiddle Factor: Complex exponential term used to adjust phase shifts while combining even and odd parts

        f_u = fx_even + fx_odd * W_ux_2k[:M//2]

        f_u_plus_k = fx_even + fx_odd * W_ux_2k[M//2:]

        fu = np.concatenate([f_u, f_u_plus_k])

    return fu


def inverseFFT_1D(fu):
    """ use recursive method to speed up"""
    fu = np.asarray(fu, dtype=complex)
    fu_conjugate = np.conjugate(fu)

    fx = FFT_1D(fu_conjugate)

    fx = np.conjugate(fx)
    fx = fx / fu.shape[0]

    return fx


def FFT_2D(fx):
    h, w = fx.shape[0], fx.shape[1] ## height and width of the input

    fu = np.zeros(fx.shape, dtype=complex) ## initialize an array, same size, but complex type

    if len(fx.shape) == 2:
        for i in range(h):
            fu[i, :] = FFT_1D(fx[i, :]) ## PErforms FFT to horizontal data

        for i in range(w):
            fu[:, i] = FFT_1D(fu[:, i]) ## Perform FFT along columns
    elif len(fx.shape) == 3: ## If image is RGB
        for ch in range(3):
            fu[:, :, ch] = FFT_2D(fx[:, :, ch]) ## Recursilvey apply FFT-2D to each color channel
    return fu


# def inverseDFT_2D(fu):
#     h, w = fu.shape[0], fu.shape[1]
#
#     fx = np.zeros(fu.shape, dtype=complex)
#
#     if len(fu.shape) == 2:
#         for i in range(h):
#             fx[i, :] = inverseDFT_1D(fu[i, :])
#
#         for i in range(w):
#             fx[:, i] = inverseDFT_1D(fx[:, i])
#
#     elif len(fu.shape) == 3:
#         for ch in range(3):
#             fx[:, :, ch] = inverseDFT_2D(fu[:, :, ch])
#
#     fx = np.real(fx)
#     return fx


def inverseFFT_2D(fu):
    h, w = fu.shape[0], fu.shape[1]

    fx = np.zeros(fu.shape, dtype=complex)

    if len(fu.shape) == 2:
        for i in range(h):
            fx[i, :] = inverseFFT_1D(fu[i, :])

        for i in range(w):
            fx[:, i] = inverseFFT_1D(fx[:, i])

    elif len(fu.shape) == 3:
        for ch in range(3):
            fx[:, :, ch] = inverseFFT_2D(fu[:, :, ch])

    fx = np.real(fx)
    return fx