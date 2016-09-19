import os, sys
import json
import numpy as np
from sklearn import naive_bayes

def fit(train_mat, train_lbl, force=False):
    clf = naive_bayes.GaussianNB()
    clf.fit(train_mat, train_lbl)

    return clf

def predict(clf, test_mat):
    return clf.predict(test_mat)

def make_train_data():
    min_val = -999
    raw_data = np.genfromtxt('../../Data/WRM/RAW/LS.csv', delimiter=',')
    train_mat = raw_data[1:,3:]
    train_mat[np.isnan(train_mat)] = min_val
    train_mat[np.isinf(train_mat)] = min_val
    train_lbl = raw_data[1:,:3]

    return train_mat, train_lbl

def make_test_data():
    min_val = -999
    test_data = np.genfromtxt('../../Data/WRM/RAW/TS.csv', delimiter=',')
    test_mat = test_data[1:,3:]
    test_mat[np.isnan(test_mat)] = min_val
    test_mat[np.isinf(test_mat)] = min_val
    test_lbl = test_data[1:,:3]

    return test_mat, test_lbl

def make_train_data2(inName, vocaName):
    inPath = '../../../Data/WRM/RAW/' + inName
    vocaPath = '../APVOCA/VOCAS/' + vocaName
    min_val = -999

    vocaIdxMap = {}
    with open(vocaPath) as f:
        vocaList = f.read().split(',')
        for idx, val in enumerate(vocaList):
            vocaIdxMap[val] = idx

    res_mat = []
    res_lbl = []

    with open(inPath) as f:
        rawList = f.read().split('\n')
        rawList.pop()
        for line in rawList:
            row = json.loads(line)
            matItem = [min_val for x in range(len(vocaIdxMap))]
            lblItem = []

            # make rssi matrix
            for rssi in row['rssi']:
                idx = vocaIdxMap[rssi['sid']]
                matItem[idx] = rssi['dbm']
            res_mat.append(matItem)

            # make label(x,y,z) array
            lblItem.append(row['x'])
            lblItem.append(row['y'])
            lblItem.append(row['z'])
            res_lbl.append(lblItem)

    return np.array(res_mat), np.array(res_lbl)

if __name__ == '__main__':
    inName = sys.argv[1]
    vocaName = sys.argv[2]
    outName = sys.argv[3]
    train_mat, train_lbl = make_train_data2(inName, vocaName)

    clf_x = fit(train_mat, train_lbl[:,0].ravel())
    clf_y = fit(train_mat, train_lbl[:,1].ravel())
#    clf_z = fit(train_mat, train_lbl[:,2].ravel()) # z has variance 0 issue

    import pickle
    # now you can save it to a file
    with open('bin/' + outName + '_gnb_x_0.pkl', 'wb') as f:
        pickle.dump(clf_x, f)
    with open('bin/' + outName + '_gnb_y_0.pkl', 'wb') as f:
        pickle.dump(clf_y, f)
'''
    # test data load
    train_mat, train_lbl = make_train_data()
    test_mat, test_lbl = make_test_data()

    # label x,y to mapped area (each 3m)
    divide_val = 1
    train_lbl[:, :2] = (train_lbl[:, :2] / divide_val).astype('int')
    test_lbl[:, :2] = (test_lbl[:, :2] / divide_val).astype('int')

    # fitting
    clf_x = fit(train_mat, train_lbl[:,0].ravel())
    clf_y = fit(train_mat, train_lbl[:,1].ravel())
#    clf_z = fit(train_mat, train_lbl[:,2].ravel()) # z has variance 0 issue

    import pickle
    # now you can save it to a file
    with open('bin/gnb_x_0.pkl', 'wb') as f:
        pickle.dump(clf_x, f)
    with open('bin/gnb_y_0.pkl', 'wb') as f:
        pickle.dump(clf_y, f)
    # predict
    preds_x = predict(clf_x, test_mat)
    preds_y = predict(clf_y, test_mat)
#    preds_z = predict(clf_z, test_mat) # z has variance 0 issue

    # show result
    print("div value: %lf" % (divide_val))
    distances_x = [(abs(preds_x[i] - test_lbl[:,0][i])) for i in range(len(test_lbl))]
    print("error distance(x): %lf m" % (np.mean(distances_x) * divide_val))

    distances_y = [(abs(preds_y[i] - test_lbl[:,1][i])) for i in range(len(test_lbl))]
    print("error distance(y): %lf m" % (np.mean(distances_y) * divide_val))

#    distances_z = [(abs(preds_z[i] - test_lbl[:,2][i])) for i in range(len(test_lbl))]
#    print("error distance(z): %lf" % (np.mean(distances_z)))
'''

