# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 11:52:48 2021

@author: s93yo
"""
### 13環境因子 SDM 結果 - 決策樹模型
# In[] 設定程式路徑及檔案名稱
# 設定程式路徑
import os
os.chdir("D:\OneDrive\Research\SDM_13env_Decision_Tree")

# 設定匯入檔案、匯出圖片名稱
csv_name = "M0026_獼猴_O_T_SDM_join_13env_欄位結合圖層.csv"

png_name = "M0026_獼猴_O_T_13env_SDM_km_decisionTree_CART_depth10_KBest_off.png"


# In[] 資料前處理
import HappyML.preprocessor as pp

# 匯入資料檔案
os.chdir("D:/OneDrive/Research/SDM_13env_Decision_Tree/13env_join_species_SDM_layer_csv")

SDM_env_data = pp.dataset(csv_name)

# 改回 HappyML 所在路徑
os.chdir("D:\OneDrive\Research\SDM_13env_Decision_Tree")

## 查看是整合檔案 or 單一物種檔案
## 切分自變數、應變數 (Decomposition)，3 個 D2 因子單位用公里 (km)
# 取出 "Species_ID" 欄第一列的數值 (index = 0)
Species_ID = SDM_env_data.at[0, "Species_ID"]

# 如 Species_ID 只有字母 (代表為整體檔案)，依照整體檔案欄位排列方式切分
if Species_ID.isalpha():
    X, Y = pp.decomposition(SDM_env_data, x_columns = [i for i in range(16) if i > 2], y_columns= [21])
# 如 Species_ID 有字母及數字 (代表為單一物種檔案)，依照單一物種檔案欄位排列方式切分
else:
    X, Y = pp.decomposition(SDM_env_data, x_columns = [i for i in range(16) if i > 2], y_columns= [19])

# # Decomposition 3 個 D2 因子單位用公尺 (m)
# X, Y = pp.decomposition(SDM_env_data, x_columns = [i for i in range(13)], y_columns= [19])

# # Dummy Variables (主要是取得 y 0, 1 對照表) (不需要，0, 1 就是照順序的 0, 1)
# Y, Y_mapping = pp.label_encoder(Y, mapping = True)

# 特徵選擇
from HappyML.preprocessor import KBestSelector

selector = KBestSelector(best_k = "auto")
X = selector.fit(x_ary = X, y_ary = Y, verbose = True, sort = True).transform(x_ary = X)

# 切分訓練集、測試集
X_train, X_test, Y_train, Y_test = pp.split_train_test(x_ary = X, y_ary = Y) 

# # 特徵縮放 (為了讓決策樹圖保持特徵數值，不縮放)
# X_train, X_test = pp.feature_scaling(fit_ary = X_train, transform_arys = (X_train, X_test))


# In[] 決策樹模型 ID3 演算法 「快樂版」
from HappyML.classification import DecisionTree

classifier = DecisionTree()
Y_pred = classifier.fit(X_train, Y_train).predict(X_test)


# # 決策樹模型 CART 演算法 「一般版」
# # 使用此算法，後面的模型驗證要從 classifier.classifier 改為 classifier
# from sklearn.tree import DecisionTreeClassifier
# import time

# classifier = DecisionTreeClassifier(criterion = "gini", max_depth = 10, random_state = int(time.time()))
# classifier.fit(X_train, Y_train)
# Y_pred = classifier.predict(X_test)



# 決策樹效能檢測
from HappyML.performance import KFoldClassificationPerformance

K = 10
kfp = KFoldClassificationPerformance(x_ary = X, y_ary = Y, classifier = classifier.classifier, k_fold = K)

print("----- SDM Decision Tree Classification -----")
print("{} Folds Mean Accuracy: {:.2f}".format(K, kfp.accuracy()))
print("{} Folds Mean Recall: {:.2f}".format(K, kfp.recall()))
print("{} Folds Mean Precision: {:.2f}".format(K, kfp.precision()))
print("{} Folds Mean macro-F1-Score: {:.2f}".format(K, kfp.f_score()))

# 計算 micro F1-score
from sklearn.model_selection import cross_val_score

micro_F1 = cross_val_score(estimator = classifier.classifier, X = X, y = Y,scoring = 'f1_micro', cv = K, n_jobs = 1)

print("{} Folds Mean micro-F1-Score: {:.2f}".format(K, micro_F1.mean()))


## 混淆矩陣、AUC、Kappa 計算
# 計算混淆矩陣
from sklearn.metrics import confusion_matrix
print("Confusion Matrix:\n", confusion_matrix(y_true = Y_test, y_pred = Y_pred))

# 用 K-fold 計算 AUC (10-fold)
AUC = cross_val_score(estimator = classifier.classifier, X = X, y = Y,scoring = 'roc_auc', cv = K, n_jobs = 1)

print("{} Folds Mean AUC: {:.2f}".format(K, AUC.mean()))

# 計算 Kappa 值 (Y_test, Y_pred 對調不影響結果)
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(Y_test, Y_pred, labels = None, weights = None, sample_weight = None)

print("cohen kappa:{:.2f}".format(kappa))


# In[] Visualization 決策樹視覺化並輸出圖片
GRAPHVIZ_INSTALL = "C:/Program Files (x86)/Graphviz/bin"

# 決策數繪圖 「快樂版」
import HappyML.model_drawer as md
from IPython.display import Image, display

# 將 Y 應變數 0 顯示成 absent, 1 顯示成 present
cls_name = ["absent", "present"]

# 生成點陣圖
graph = md.tree_drawer(classifier = classifier.classifier, feature_names = X_test.columns, target_names = cls_name, graphviz_bin = GRAPHVIZ_INSTALL)
# 點陣圖轉換為 PNG
#graph_final = display(Image(graph.create_png()))

# 設定程式路徑 (輸出 CART 決策樹圖片用)
#os.chdir("D:\OneDrive\Research\SDM_13env_Decision_Tree\決策樹圖_CART")
# 輸出圖片到當前資料夾
graph.write_png(png_name)


# # In[] Visualization 決策樹繪圖 「標準版」
# GRAPHVIZ_INSTALL = "C:/Program Files (x86)/Graphviz/bin"

# # 決策數繪圖 「標準版」
# from sklearn import tree
# import pydotplus
# from IPython.display import Image, display
# import os

# # 保險用，避免出現錯誤訊息 （沒有這行還是可以跑）
# os.environ["PATH"] += os.pathsep + GRAPHVIZ_INSTALL


# dot_data = tree.export_graphviz(classifier.classifier, filled = True, feature_names = X_test.columns, class_names = cls_name, rounded = True, special_characters = True)

# pydot_graph = pydotplus.graph_from_dot_data(dot_data)
# #自訂圖形大小 (還是有最大上限)
# pydot_graph.set_size('"1000000,1000000!"')
# pydot_graph.write_png('resized_tree_100萬.png')



# # graph = pydotplus.graph_from_dot_data(dot_data)
# # display(Image(graph.create_png()))



