# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 17:02:25 2021

@author: s93yo
"""
### 13環境因子 SDM 結果 - 隨機森林
# 設定程式路徑
import os
os.chdir("D:\OneDrive\Research\SDM_13env_Decision_Tree")

# In[] 設定匯入檔案、匯出圖片名稱
csv_name = "M0026_獼猴_SDM_join_13env_欄位結合圖層.csv"

png_name = "M0026_獼猴_13env_SDM_decisionTree_km_select10.png"

# In[] 資料前處理
import HappyML.preprocessor as pp

# 匯入資料檔案
os.chdir("D:/OneDrive/Research/SDM_13env_Decision_Tree/13env_join_species_SDM_layer_csv")

SDM_env_data = pp.dataset(csv_name)

# 改回 HappyML 所在路徑
os.chdir("D:\OneDrive\Research\SDM_13env_Decision_Tree")


# 更改欄位名稱

# # 3 個 D2 因子單位用公尺 (m)
# X, Y = pp.decomposition(SDM_env_data, x_columns = [i for i in range(13)], y_columns= [19])

# 3 個 D2 因子單位用公里 (km)
X, Y = pp.decomposition(SDM_env_data, x_columns = [i for i in range(16) if i > 2], y_columns= [19])


# # Dummy Variables (主要是取得 y 0, 1 對照表)
# Y, Y_mapping = pp.label_encoder(Y, mapping = True)

# 特徵選擇
from HappyML.preprocessor import KBestSelector

selector = KBestSelector(best_k = "auto")
X = selector.fit(x_ary = X, y_ary = Y, verbose = True, sort = True).transform(x_ary = X)

# 切分訓練集、測試集
X_train, X_test, Y_train, Y_test = pp.split_train_test(x_ary = X, y_ary = Y) 

# 特徵縮放 (為了看決策樹，不縮放)


# In[] 隨機森林
from HappyML.classification import RandomForest

classifier = RandomForest(n_estimators = 10, criterion = "entropy")
Y_pred = classifier.fit(X_train, Y_train).predict(X_test)

# 決策樹效能檢測
from HappyML.performance import KFoldClassificationPerformance

K = 10
kfp = KFoldClassificationPerformance(x_ary = X, y_ary = Y, classifier = classifier.classifier, k_fold = K)

print("----- SDM Random Forest Classification -----")
print("{} Folds Mean Accuracy: {:.2f}".format(K, kfp.accuracy()))
print("{} Folds Mean Recall: {:.2f}".format(K, kfp.recall()))
print("{} Folds Mean Precision: {:.2f}".format(K, kfp.precision()))
print("{} Folds Mean F1-Score: {:.2f}".format(K, kfp.f_score()))

# In[] 混淆矩陣、AUC、Kappa 計算
# 計算混淆矩陣
from sklearn.metrics import confusion_matrix
print("Confusion Matrix:\n", confusion_matrix(y_true = Y_test, y_pred = Y_pred))

# 用 K-fold 計算 AUC (10-fold)
from sklearn.model_selection import cross_val_score

AUC = cross_val_score(estimator = classifier.classifier, X = X, y = Y,scoring = 'roc_auc', cv = K, n_jobs = 1)

print("{} Folds Mean AUC: {:.2f}".format(K, AUC.mean()))

# 計算 Kappa 值 (Y_test, Y_pred 對調不影響結果)
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(Y_test, Y_pred, labels = None, weights = None, sample_weight = None)

print("cohen kappa:{:.2f}".format(kappa))
