import numpy as np
cimport numpy as np
cimport cython

# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
DTYPE = np.float32
ctypedef np.float32_t DTYPE_t


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef jenks_matrices_init(np.ndarray[DTYPE_t, ndim=1] data, Py_ssize_t n_classes):
    cdef Py_ssize_t n_data = data.shape[0]

    cdef np.ndarray[DTYPE_t, ndim=2] lower_class_limits
    cdef np.ndarray[DTYPE_t, ndim=2] variance_combinations

    lower_class_limits = np.zeros((n_data+1, n_classes+1), dtype=DTYPE)
    lower_class_limits[1, 1:n_classes+1] = 1.0

    inf = float('inf')
    variance_combinations = np.zeros((n_data+1, n_classes+1), dtype=DTYPE)
    variance_combinations[2:n_data+1, 1:n_classes+1] = inf

    return lower_class_limits, variance_combinations
   
@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
@cython.nonecheck(False)
cdef jenks_matrices(np.ndarray[DTYPE_t, ndim=1] data, Py_ssize_t n_classes):
    cdef np.ndarray[DTYPE_t, ndim=2] lower_class_limits
    cdef np.ndarray[DTYPE_t, ndim=2] variance_combinations
    lower_class_limits, variance_combinations = jenks_matrices_init(data, n_classes)

    cdef Py_ssize_t l, sl = 2, nl = data.shape[0] + 1
    cdef Py_ssize_t m
    cdef Py_ssize_t j, jm1
    cdef Py_ssize_t i4
    cdef Py_ssize_t lower_class_limit
    cdef float sum = 0.0
    cdef float sum_squares = 0.0
    cdef float w = 0.0
    cdef float val
    cdef float variance = 0.0

    for l in range(2, nl):
        sum = 0.0
        sum_squares = 0.0
        w = 0.0
   
        for m in range(1, l+1):
            # `III` originally
            lower_class_limit = l - m + 1
            i4 = lower_class_limit - 1

            val = data[i4]

            # here we're estimating variance for each potential classing
            # of the data, for each potential number of classes. `w`
            # is the number of data points considered so far.
            w += 1.0

            # increase the current sum and sum-of-squares
            sum += val
            sum_squares += val * val

            # the variance at this point in the sequence is the difference
            # between the sum of squares and the total x 2, over the number
            # of samples.
            variance = sum_squares - (sum * sum) / w

            if i4 != 0:
                for j in range(2, n_classes+1):
                    jm1 = j - 1
                    if variance_combinations[l, j] >= (variance + variance_combinations[i4, jm1]):
                        lower_class_limits[l, j] = lower_class_limit
                        variance_combinations[l, j] = variance + variance_combinations[i4, jm1]

        lower_class_limits[l, 1] = 1.
        variance_combinations[l, 1] = variance

    return lower_class_limits, variance_combinations


def jenks(data, n_classes):
    if n_classes > len(data):
        return

    data = np.array(data, dtype=DTYPE)
    data.sort()

    lower_class_limits, _ = jenks_matrices(data, n_classes)

    k = data.shape[0] - 1
    kclass = [0.] * (n_classes+1)
    countNum = n_classes

    kclass[n_classes] = data[len(data) - 1]
    kclass[0] = data[0]

    while countNum > 1:
        elt = int(lower_class_limits[k][countNum] - 2)
        kclass[countNum - 1] = data[elt]
        k = int(lower_class_limits[k][countNum] - 1)
        countNum -= 1

    return kclass

