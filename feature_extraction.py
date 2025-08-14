# import all modeuls
import os
import numpy as np
import radiomics.featureextractor as FEE
import cv2
import SimpleITK as sitk
import pandas as pd

# %% set initial path
basepath = './DATA/'
para_path = './CODE/param.yaml'

# %% extract Center 1 and Center 2 data features
centerlist = ['C1', 'C2']
sequencelist = ['A', 'D', 'NE', 'P']
for center in centerlist:
    for sequence_type in sequencelist:
        datalist = sorted(os.listdir(os.path.join(basepath, center, sequence_type, 'image')))
        extractor = FEE.RadiomicsFeatureExtractor(para_path)
        df = pd.DataFrame()
        for i in datalist:
            image = sitk.ReadImage(os.path.join(basepath, center, sequence_type, 'image', i))
            mask = sitk.ReadImage(os.path.join(basepath, center, sequence_type, 'mask', i))
            features = extractor.execute(image, mask)     
            datadict = features.copy()
            for k in features.keys():
                if 'diagnostics' in k:
                    del datadict[k]
            features = {}
            for k in datadict.keys():
                features[sequence_type+'_'+k] = datadict[k]
            df_add = pd.DataFrame.from_dict(features.values()).T
            df_add.columns = features.keys()
            df_add.insert(0, 'patient_num', i[:-7])
            df = pd.concat([df,df_add])
        df.to_excel(os.path.join(basepath,  center+'_'+sequence_type+'_features.xlsx'))
