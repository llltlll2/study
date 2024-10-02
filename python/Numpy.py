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

py_list1 = [0, 1]
py_list2 = py_list1[:]
py_list2[0] = 2
print(py_list1)
print(py_list2)

np_array1 = np.array([0,1])
np_array2 = np_array1[:]
np_array2[0] = 2
print(np_array1)
print(np_array2)

print(np.arange(1, 10 , 2))

#ランダム
rng = np.random.default_rng(123)
f = rng.random((3,2))
print(f)
print(rng.integers(1,10, size = (3,3)))
print(rng.uniform(0.0,5.0,size = (2,3)))
print(rng.uniform(size = (2,3)))#デフォルトは０～１の範囲
#平均、標準偏差、sizeを引数にして正規分布の乱数を獲得できる
print(rng.standard_normal(size = (4,2)))
print(np.zeros(3))#０．０が入った引数の要素数の配列の取得
print(np.ones(2))#１．０が入った配列の取得