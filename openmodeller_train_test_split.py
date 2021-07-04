# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 22:51:39 2021

@author: s93yo
"""
### 物種出現資料檔案批次取 10 次 75% 訓練點位
## 使用說明： for j 及最後面的 if 判斷式填入取樣次數數字，即可執行
# In[] 導入套件
import os # 批量顯示檔名、修改檔名
import pandas as pd # 資料處理
from sklearn.model_selection import train_test_split # 切分「訓練集、測試集」

## 指定匯入檔案 (inpath)、匯出檔案 (outpath) 路徑
# inpath = "D:/OneDrive/Research/SDM/species_data_openmodeller/出現資料txt原始檔/"
# outpath = "D:/OneDrive/Research/SDM/species_data_openmodeller/出現資料批次訓練集檔案/"

#inpath = "D:/OneDrive/Research/SDM/species_data_biomapper/出現資料csv原始檔/"

#outpath = "D:/OneDrive/Research/SDM/species_data_biomapper/出現資料批次訓練集csv檔案/"

## 新 SDM 物種資料切分
# inpath = "D:/OneDrive/Research/SDM_new/M0055_species_data/"

# outpath = "D:/OneDrive/Research/SDM_new/M0055_species_data/GARP_species_data/"

# # 臺灣 2x2 網格物種資料切分
# inpath = "D:/OneDrive/Research/SDM_new/M0053_species_data/"

# outpath = "D:/OneDrive/Research/SDM_new/M0053_species_data/GARP_species_data_2x2/"


# M0052 麝香貓 13 env 第 10 個切分檔案報錯
inpath = "D:/OneDrive/Research/SDM_13/sepcies_data/M0052_sepcies_data/"

outpath = "D:/OneDrive/Research/SDM_13/sepcies_data/M0052_sepcies_data/"
 

# 選擇要執行的檔案是 "csv" or "txt"
file_type = input("輸入欲執行切分檔案的副檔名:")


# In[] 批量讀取檔案名稱
# 讀取資料夾內的所有檔案名稱
filelist_original = os.listdir(inpath)


# In[] 按照 file_type 判斷匯出檔案的副檔名及 sep 參數、以及篩選資料夾內相符的檔案
# 創立一個空串列 filelist
filelist = []

# 按照 file_type 判斷匯出檔案的副檔名及 sep 參數、以及篩選資料夾內相符的檔案
if file_type == "csv":
    # 篩選名稱中有 .csv 的檔案
    for k in range(len(filelist_original)):
        if ".csv" in filelist_original[k]:
            filelist.append(filelist_original[k])
        else:
            None
    # 設定 sep 參數
    sep_format = ","

elif file_type == "txt":
    # 篩選名稱中有 .txt 的檔案
    for k in range(len(filelist_original)):
        if ".txt" in filelist_original[k]:
            filelist.append(filelist_original[k])
        else:
            None
    # 設定 sep 參數
    sep_format = "\t"



# In[] 匯入資料 & 切分「訓練集、測試集」
for i in range(len(filelist)):
    # 按照 file_type 選擇匯入檔案的 pd 函數
    if file_type == "csv":
        present_data = pd.read_csv(inpath + filelist[i]) 
    elif file_type == "txt":
        present_data = pd.read_table(inpath + filelist[i])     
    
    
    for j in range(10):
        # 切分「訓練集、測試集」(訓練集佔比 0.75，測試集佔比 0.25)
        present_train, present_test = train_test_split(present_data, test_size = 0.25, random_state = None)
        
        # 設定輸出檔案名稱
        outfile_name = filelist[i][:(len(filelist[i]) - 4)] + "_train75_" + str(j + 1) + "." + file_type
        # 匯出 75% 訓練集 present_train 的 txt 檔案
        present_train.to_csv(outpath + outfile_name, sep = sep_format, index = False)
        
        # 最後一次小迴圈，告知檔案原始資料筆數和 75% 訓練集資料筆數
        if (j + 1) == 10:
            print("{}原始資料筆數： {}".format(filelist[i][0:5], len(present_data)))
            print("{}訓練資料筆數： {}".format(filelist[i][0:5], len(present_train)))
            print()
    
  


      



