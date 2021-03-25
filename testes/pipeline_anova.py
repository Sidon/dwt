# _*_ coding: utf-8 _*_
__author__ = 'sidon'
from sklearn import svm
from sklearn.datasets import samples_generator
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline

# Cria dados para a classificacao
X, y = samples_generator.make_classification(
    n_features=20, n_informative=3, n_redundant=0, n_classes=4,
    n_clusters_per_class=2)

print(('X shape: ',X.shape,'\ny Shape: ',y.shape))

# ANOVA SVM-C
# 1) anova filter, take 3 best ranked features
anova_filter = SelectKBest(f_regression, k=3)

###
# Utilizada a classe SelectKBest (http://goo.gl/r48omy)  com os parametros:
#    f_regression = Indicando que se trata de uma regressão e não de uma classificação
#    k = 3 Indicando para selecionar apenas 3 'top' atributos (ou seria scores?) (só 3???)

####
# Esta linha mostra os scores para cada atritubo, ou os melhores atributos?
print(('Anova Filter scores:\n ', anova_filter.pvalues_))
print(('\nShape do Anova Filter scores_: ',anova_filter.scores_.shape))

##
# Abaixo um tab após o ponto mostra os atributos do objeto (retire o sinal de comentario #)
# print anova_filter.

# 2) svm (http://goo.gl/ugK2mW)
clf = svm.SVC(kernel='linear')

# Diferente do link http://goo.gl/ouLbrs
anova_svm = Pipeline([('anova', anova_filter), ('svm', clf)])

f = anova_svm.fit(X, y)

print(('Predição:\n', anova_svm.predict(X)))
print(('\nDados reais:\n',y))
