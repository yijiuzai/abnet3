import torch
from torch.autograd import Variable
from torch.nn import functional as F
import numpy as np


def distance_matrix(A: Variable, B: Variable, distance='cos'):
    """
    :param A: matrix A
    :param B: matrix B
    :param distance: 'cos', or a callable(vector1, vector2).
    :return: the distance matrix D[i, j] = distance(A[i], B[j])
    
    Note : this function is differentiable
    """

    if distance == 'cos':
        distance = F.cosine_similarity
    elif callable(distance):
        distance = distance
    else:
        raise ValueError("This distance is not supported")
    n, l = A.size()
    m, _ = B.size()
    AA = A[:, None, :]  # n, 1, l
    AA = AA.expand(n, m, l)

    BB = B[None, :, :]  # 1, m, l
    BB = BB.expand(n, m, l)

    return distance(AA, BB, dim=2)


class SoftDTWDistance(torch.autograd.Function):
    """
    This class is an autograd function that computes forward and backward
    pass for the Soft DTW algorithm, given a distance matrix.
    """

    @staticmethod
    def softmin(a, b, c, gamma):
        """
        Softmin function as described in the Soft DTW paper.
        There is a trick here to get better precision (remove max value from vector
        before doing the exponentiation).
        """
        if gamma == 0:
            return min(a, b, c)

        a /= -gamma
        b /= -gamma
        c /= -gamma

        max_value = max(a, b, c)
        sum = (np.exp(a - max_value) +
               np.exp(b - max_value) +
               np.exp(c - max_value))
        return - gamma * (np.log(sum) + max_value)

    @staticmethod
    def forward(ctx, D, gamma):
        """
        :param ctx: pytorch context   
        :param gamma: Soft-DTW parameter (see paper)
        :param D: Distance matrix
        """
        print(type(D))
        n, m = D.size()

        R = np.full((n+2, m+2), np.inf)  # we index starting at 1 to facilitate the following loop
        R[0, 0] = 0
        # forward passs
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                R[i, j] = D[i-1, j-1] + SoftDTWDistance.softmin(R[i - 1, j], R[i - 1, j - 1], R[i, j - 1], gamma)

        # after this, we have to save some variables for the backward pass (mostly D and R)
        R = torch.from_numpy(R)
        ctx.R = R
        ctx.save_for_backward(D)
        print(R)
        return torch.Tensor([R[n, m]])

    @staticmethod
    def backward(ctx, grad_outputs):
        gamma = ctx.gamma
        R = ctx.R
        D, = ctx.saved_variables

        n, m = D.size()

        # add an extra row and column to D to deal with edge cases
        D = torch.stack([D, torch.zeros(1, n)], dim=0)
        D = torch.stack([D, torch.zeros(m, 1)], dim=1)

        E = torch.zeros(n+2, m+2)  # one indexed

        for j in reversed(range(1, m+1)):
            for i in reversed(range(1, n+1)):
                a = torch.exp(1/gamma * (R[i+1, j] - R[i, j] - D[i, j-1]))
                b = torch.exp(1/gamma * (R[i, j+1] - R[i, j] - D[i-1, j]))
                c = torch.exp(1/gamma * (R[i+1, j+1] - R[i, j] - D[i, j]))
                E[i, j] = E[i+1, j] * a + E[i, j+1] * b + E[i+1, j+1] * c
        return grad_outputs * E[1:n+1, 1:m+1], None


def soft_dtw(A, B, distance='cos', gamma=0.1):
    D = distance_matrix(A, B, distance=distance)
    r = SoftDTWDistance.apply(D, gamma)
    return r