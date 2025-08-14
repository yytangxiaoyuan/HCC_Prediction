# import all needed modules
import os
import numpy as np
import pandas as pd
import pingouin as pg
from sklearn.preprocessing import StandardScaler
from lifelines import CoxPHFitter

# 1- load the excel with all clinical features of all patients
all_feature = pd.read_excel('./DATA/AllPatients.xlsx', header=0)
c1_feature = all_feature[all_feature['center'] == 1].reset_index(drop=True)
c2_feature = all_feature[all_feature['center'] == 2].reset_index(drop=True)
c1_feature = c1_feature.drop(c1_feature.columns[1], axis=1)
c2_feature = c2_feature.drop(c2_feature.columns[1], axis=1)
# 2- release the initial all feature data
del all_feature
# 3- load the radiomics signatures
c1_rs = pd.read_excel('./RESULTS/LassoCoxRegress/Results.xlsx', 
                      sheet_name='c1_signatures', header=0)
c2_rs = pd.read_excel('./RESULTS/LassoCoxRegress/Results.xlsx', 
                      sheet_name='c2_signatures', header=0)
# 4- do univariable cox regression to find important features
cph = CoxPHFitter()
statistic = pd.DataFrame()
statistic['feature_name'] = c1_feature.columns[3:]
statistic['HR'] = None
statistic['HR_lower'] = None
statistic['HR_upper'] = None
statistic['p_value'] = None
for i in range(statistic.shape[0]):
    temp = pd.concat([c1_rs.iloc[:,:2], c1_feature.iloc[:, i+3]], axis=1)
    cph.fit(temp, duration_col='Time', event_col='Event')
    statistic.loc[i, 'HR'] = cph.summary['exp(coef)'][c1_feature.columns[i+3]]
    statistic.loc[i, 'HR_lower'] = cph.summary['exp(coef) lower 95%'][c1_feature.columns[i+3]]
    statistic.loc[i, 'HR_upper'] = cph.summary['exp(coef) upper 95%'][c1_feature.columns[i+3]]
    statistic.loc[i, 'p_value'] = cph.summary['p'][c1_feature.columns[i+3]]
# 8- save the results to excel files
statistic.to_excel('./RESULTS/ClinicalFeatureSelect/statistic.xlsx', index=False)
# 9- save the c1 and c2 clinical features
c1_feature['radiomics_signature'] = c1_rs['radiomics_signature']
c2_feature['radiomics_signature'] = c2_rs['radiomics_signature']
c1_feature.to_excel('./RESULTS/ClinicalFeatureSelect/C1_features.xlsx', index=False)
c2_feature.to_excel('./RESULTS/ClinicalFeatureSelect/C2_features.xlsx', index=False)
