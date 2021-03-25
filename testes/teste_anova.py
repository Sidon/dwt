# -*- coding: utf-8 -*-
__author__ = 'Sidon'
import numpy as np

from sklearn.feature_selection import SelectKBest, f_classif


X = np.array(([5.5, 2.2, 5.5, 4, 5.5],[6.1, 2.3, 6.1, 4, 6.1], [5.9, 2.2, 5.9, 4, 5.9],
 [5.3,	2.2, 5.3, 4, 5.3], [6, 2.3, 6, 4,	6], [5.5, 2.1, 5.5, 4, 5.5], [2.2, 2.2, 2.2, 4, 2.2],
 [2.3, 2.3, 2.3, 4, 2.3], [4.2, 2.1, 4.2, 4, 4.2], [2.2, 2.2, 2.2, 4, 2.2],
 [2, 2.3, 2, 4, 2],  [2.3, 2.3, 2.3, 4, 2.3]))

y = np.array([0,0,0,0,0,0,1,1,1,1,1,1])

sk = SelectKBest(f_classif, k=all)
sk.fit(X,y)

# Cria e executa o filtro anova
sk = SelectKBest(f_classif, k=all)
sk.fit(X,y)

# Pretty print
np.set_printoptions(suppress=True, precision=7)

# Apresenta os pvalues
print((sk.pvalues_))