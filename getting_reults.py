import pandas as pd
import numpy as np
from scipy.special import expit  # сигмоида

def predict_proba(X, beta, add_intercept=True):
    """
    Возвращает вероятность класса 1 для каждой строки X.
    X — массив формы (n_samples, n_features) без столбца единиц.
    """
    if add_intercept:
        X = np.column_stack([np.ones(len(X)), X])
    linear = X @ beta
    return expit(linear)

result_r_plus1= list(pd.read_excel('coefs_plus1.xlsx').Coefficient)
result_r_minus1= list(pd.read_excel('coefs_minus1.xlsx').Coefficient)
X = pd.read_excel('X.xlsx')

#бутстрапинг
buts_std ={}
for col in X.columns[0:1]:
    integer_eff = []
    for i in range(100):
        X_66pr = X.sample(frac=2/3)
        integer_eff.append(
            (predict_proba(X_66pr.assign(**{col: 1}), result_r_plus1).mean() - predict_proba(X_66pr.assign(**{col: 1}), result_r_minus1).mean())
            -
            (predict_proba(X_66pr.assign(**{col: 0}), result_r_plus1).mean() - predict_proba(X_66pr.assign(**{col: 0}), result_r_minus1).mean())
        )

    buts_std[col] = np.array(integer_eff).std()
d = []
for col in  X.columns:
    mask =X[col]>0
    d.append({
        'Вопрос':col.split('_')[0],
        'Ответ':col.split('_')[1],
        'y_ср_plus_1 при x=1': predict_proba(X.assign(**{col: 1}), result_r_plus1).mean(),
        'y_ср_plus_1 при x=0': predict_proba(X.assign(**{col: 0}), result_r_plus1).mean(),
        'y_ср_minus_1 при x=1': predict_proba(X.assign(**{col: 1}), result_r_minus1).mean(),
        'y_ср_minus_1 при x=0': predict_proba(X.assign(**{col: 0}), result_r_minus1).mean()
    })

d= pd.DataFrame(d)
d['beta-коэффициент_plus1']=np.around(result_r_plus1[1:],6)
d['beta-коэффициент_minus1']=np.around(result_r_minus1[1:],6)
d['buts_std'] = (d['Вопрос']+'_'+d['Ответ']).map(buts_std)
d['Интегральный показатель'] = (d['y_ср_plus_1 при x=1']-d['y_ср_minus_1 при x=1'])-(d['y_ср_plus_1 при x=0']-d['y_ср_minus_1 при x=0'])
d.to_excel(f'Анализ оценки.xlsx',index=False)