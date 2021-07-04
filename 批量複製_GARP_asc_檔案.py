# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 10:42:58 2021

@author: s93yo
"""
# In[] 批量把路徑內 (包含所有子資料夾) 的指定檔案複製到另一個資料夾
import os # 檔案處理
import shutil # 複製貼上檔案

# 指定要列出所有檔案的路徑
mypath = input("要複製的檔案最大路徑：")
# 貼上的路徑 (不包含資料夾)
save_dir = input("貼上的檔案路徑(不包含存放檔案的資料夾)：")
# 貼上的資料夾 (第一次貼上前會新增此資料夾)
dir_name = "GARP_原始輸出網格"

# 重新命名時貼在檔名末端的數字 (訓練集 1 ~ 10)
train_number = 0

# 遞迴列出所有檔案的絕對路徑 = 列出此目立下的所有檔案及資料夾 (包含全部子資料夾)
for root, dirs, files in os.walk(mypath):
    # 迴圈提取這個路徑下的檔案名稱
    for f in files:
        # 如檔案名稱包含 ".asc.aux"
        if ".asc.aux" in f:
            # 取出目前徑作為 file_path (root = 目前讀取到的路徑)
            file_path = root 

            
            # 檔名末端的數字 + 1，並印出數字
            train_number += 1
            print(train_number)
            
            # 取得所有檔案與子資料夾名稱
            files = os.listdir(file_path)
            
            # file_path 下的所有檔案名稱 (filename)
            for filename in files:
                # 濾出要複製的檔案 (ascii raster 總共由 3 個檔案組成)
                if ("projection.prj" in filename) or ("projection.asc"  in filename) or ("projection.asc.aux" in filename): 
                    # 印出複製的檔案    
                    print(filename) 
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
                    newname = filename.replace("projection", "projection" + str(train_number))
                    # 重新命名貼上的檔案
                    os.rename(to_path + filename, to_path + newname)

# 參考網站1：https://blog.gtwang.org/programming/python-list-all-files-in-directory/
# 參考網站2：https://blog.csdn.net/duan19920101/article/details/105004691



### 以上由下面兩部份組成
# part1：取出指定檔案的資料夾絕對路徑
# part2：使用此路徑複製指定檔案到指定資料夾下

# # In[] 印出指定 or 全部檔案的絕對路徑
# import os

# # 指定要列出所有檔案的目錄
# mypath = "D:\\python_test"

# # 遞迴列出所有檔案的絕對路徑
# for root, dirs, files in os.walk(mypath):
#   for f in files:
#       # 如檔案名稱包含 ".asc.aux"
#       if ".asc.aux" in f:
#           # 印出檔案絕對路徑 (包含檔名)
#           #fullpath = os.path.join(root, f)
#           # 印出檔案所在資料夾絕對路徑 (不包含檔名)
#           fullpath = root
#           print(fullpath)

# # 參考網站：https://blog.gtwang.org/programming/python-list-all-files-in-directory/
                    
                    
# # In[] 批量把檔案複製到另一個資料夾
# import os
# import shutil

# file_path = "D:/python_test"
# save_dir = "D:/python_copy"
# dir_name = "GARP_原始輸出網格"

# # 取得所有檔案與子資料夾名稱
# files = os.listdir(file_path)

# for filename in files: # file_path 下的所有檔案名稱 (filename)
#     if ("projection.prj" in filename) or ("projection.asc"  in filename) or ("projection.asc.aux" in filename): # 濾出要複製的檔案
#         print(filename) # 印出複製的檔案
#         # 舊檔案的絕對路徑 (包含副檔名)
#         from_path = os.path.join(file_path, filename) 
#         # 新檔案的絕對路徑
#         to_path = save_dir + "/" + dir_name + "/"        
        
#         # 如果 to_path 路徑不存在，則新增此路徑
#         if not os.path.isdir(to_path):
#          	# 新增路徑 (資料夾)
#             os.makedirs(to_path) 
        
#         # 複製檔案並貼上
#         shutil.copy(from_path, to_path)
#         # 產生新檔案名稱 (檔名末端加上 1 ~ 10)
#         newname = filename.replace("projection", "projection" + str(1))
#         # 重新命名貼上的檔案
#         os.rename(to_path + filename, to_path + newname)

# # 參考網站：https://blog.csdn.net/duan19920101/article/details/105004691



