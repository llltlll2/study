import numpy as np

a = np.array([1,2,3])
print(a)
print(type(a))
print(a.shape)#要素数の確認

b = np.array([[1,2,3],[4,5,6]])
print(b)
print(b.shape)
#この場合は(2, 3)が出力されて２次元配列の３要素の配列であることがわかる

c1 = np.array([0,1,2,3,4,5])
#配列を２×３のものに変える
c2 = c1.reshape(2,3)
print(c2)
#配列を１次元配列にする(参照を返す)
c3 = c2.ravel()
print(c3)
#コピーを返す(コピーを返す)
c4 = c2.flatten()
print(c4)

#Numpy配列はdtypeで属性を確認できる
#Numpy由来の要素は一つのデータ型に統一され、Numpy由来の型になる
print(a.dtype)#int64っていう型名が出力される

d = np.array([1,2],dtype=np.int16)
print(d.dtype)
print(d.astype(np.float16))

#スライスは普通にできるっぽい？？？？
#arrayに対して