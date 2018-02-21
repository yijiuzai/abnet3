from abnet3.soft_dtw import SoftDTWDistance, distance_matrix
import torch
from torch.nn.functional import cosine_similarity
from torch.autograd import Variable
import numpy as np
import pytest

def compute_distance_matrix(A, B):
    n = A.size()[0]
    m = B.size()[0]

    D = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            D[i, j] = cosine_similarity(A[i], B[j], dim=0).data[0]

    return D


def test_softmin():
    a, b, c = 1, 2, 3
    sm = SoftDTWDistance.softmin(a, b, c, 0.1)
    print(sm)
    assert abs(sm - min(a, b, c)) <= 0.1  # softmin is close to min


def test_soft_dtw():


    A = Variable(torch.randn(3, 3), requires_grad=True)
    B = Variable(torch.randn(2, 3), requires_grad=True)
    D = distance_matrix(A, B)
    print(type(D))

    R = SoftDTWDistance.apply(D, 0.1)
    print(R)


def test_distance_matrix():

    A = Variable(torch.randn(3, 3), requires_grad=True)
    B = Variable(torch.randn(2, 3))

    D = distance_matrix(A, B)
    assert (D.data.numpy() == compute_distance_matrix(A, B)).all()

    s = torch.sum(D)

    # ** check derivative by applying a small gaussian perturbation**
    s.backward()
    dA = Variable(torch.randn(3, 3))
    dA *= 0.0001

    A2 = A + dA  # so S(A2) = S(A) + dA * d(S(A))

    D2 = distance_matrix(A2, B)
    s2 = torch.sum(D2)
    assert s2.data[0] == pytest.approx((s + torch.sum(dA * A.grad)).data[0])