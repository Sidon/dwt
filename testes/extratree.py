__author__ = 'Sidon'

def extratree(exp):

    print ('\nObtendo os dados (minha lib classutil)')
    X, y = getdata(exp, agrupado=True)

    print ('\nCriando o classificador')
    t0 = time.time()
    clf = ExtraTreesClassifier()
    X_new = clf.fit(X, y).transform(X)
    custo_tempo_tree = (time.time() - t0)

    t0 = time.time()
    print ('\nCriando o score:')
    score = clf.score(X,y)
    custo_tempo_score = (time.time() - t0)

    print(('Custo tempo tree: ', custo_tempo_tree))
    print(('Custo tempo score:', custo_tempo_score))

    print(('Scores:\n ', score))

    print('Criando o score do teste...')
    t0 = time.time()
    X_test, y_test = gettest(exp,'wmcl')
    score_test = clf.score(X_test,y_test)
    custo_tempo_score_test = (time.time() - t0)

    print(('Custo do score teste: ', custo_tempo_score_test))
    print(('Score do teste: ', score_test))

    print(('\nPredict: \n',clf.predict(X_test)))
    print(('\nDados Reais:\n', y_test))

    return
