import numpy as np
import matplotlib.pyplot as plt
import sys
from GUI import file_select

file_name=file_select()

NX=100
NY=100
#[.txt]ファイルからデータを読み取
Phi = np.loadtxt(file_name, skiprows=1, unpack=True)[2,:].reshape(NX,NY)
x = np.linspace(0, 1, NX) #x軸の描画範囲の生成。
y = np.linspace(0, 1, NY) #y軸の描画範囲の生成。
X, Y = np.meshgrid(x, y)

# 等高線図の生成。
cont=plt.contour(X,Y,Phi,  colors=['black']) #alpha:透過度
cont.clabel(fmt='%1.1f', fontsize=8)

#カラー等高線図の生成。
plt.pcolormesh(X, Y, Phi, cmap='Spectral_r') #cmapで色付けの規則を指定する。
#plt.pcolor(X, Y, Z, cmap='hsv') # 等高線図の生成。cmapで色付けの規則を指定する。

pp=plt.colorbar (orientation="vertical") # カラーバーの表示
pp.set_label("Phi", fontname="Arial", fontsize=24) #カラーバーのラベル

plt.xlabel('X', fontsize=24)
plt.ylabel('Y', fontsize=24)

plt.show()
print("終了")
