# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 10:42:58 2021

@author: s93yo
"""
# In[] biomapper 輸出 HS map 複製到指定資料夾，並在檔名末端加上編號 (1 ~ 10)
import os # 檔案處理
import shutil # 複製貼上檔案

# 指定要列出所有檔案的路徑
file_path = "D:/OneDrive/Research/SDM_13/a_13env_SDM_2x2_polygon_point/x_ENFA_13nev_2x2_result/ENFA_2x2_2species_result/M0050_lab_2x2_13env_train75_ENFA_result/"

# 貼上的路徑 (不包含資料夾)
save_dir = "D:/OneDrive/Research/SDM_13/a_13env_SDM_2x2_polygon_point/x_ENFA_13nev_2x2_result/ENFA_2x2_2species_result/M0050_lab_2x2_13env_train75_ENFA_result/"

# 貼上的資料夾 (第一次貼上前會新增此資料夾)
dir_name = "M0050_lab_2x2_env13_Suitability_map"

# 訓練集編號，貼上的檔案改名
train_number = input("訓練集編號數字 (新增到 HS map 檔名)：")

print("貼上檔案名稱：")

# 取得所有檔案與子資料夾名稱
files = os.listdir(file_path)

# file_path 下的所有檔案名稱 (filename)
for filename in files:
    # 濾出要複製的檔案 (ascii raster 總共由 3 個檔案組成)
    if ("M_FQ.rdc" in filename) or ("M_FQ.rst"  in filename): 
        # 印出複製的檔案
        #print(filename) 
        # 舊檔案的絕對路徑 (包含副檔名)
        from_path = os.path.join(file_path, filename) 
        # 新檔案的絕對路徑
        to_path = save_dir + "/" + dir_name + "/"        
        
        # 如果 to_path 路徑不存在，則新增此路徑
        if not os.path.isdir(to_path):
         	# 新增路徑 (資料夾)
            os.makedirs(to_path) 
        
        # 複製檔案並貼上
        shutil.copy(from_path, to_path)
        # 產生新檔案名稱 (檔名末端加上 1 ~ 10)
        newname = filename.replace("13env_ENFA", "13env_ENFA" + "_" + train_number)
        # 重新命名貼上的檔案
        os.rename(to_path + filename, to_path + newname)
        # 印出重新命名的檔案名稱
        print(newname)
    
print()

