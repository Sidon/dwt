__author__ = 'Sidon'

def gettest(exp, target='wcll'):

    store = pd.HDFStore(exp['store'])

    key = exp['key']+'/excedentes/'+target+'/'+exp['detalhe']

    print(('\nCarregando atributos: ', key))

    features_list = (store[key]).tolist()

    if target=='wcll':
        label = 0
    elif target=='wfl':
        label = 1
    elif target=='wmcl':
        label = 2

    targets = np.empty(len(features_list))
    targets[:] = label

    return np.array(features_list), targets

