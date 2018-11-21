import numpy as np
import pandas as pd

no = 1
ma = 930
al = 949
res = [[0,0,0,1] for i in range(no)]
res2 = [[0,1,0,0] for i in range(no,ma)]
res3 = [[0,0,0,1] for i in range(ma,al)]
res = res + res2 + res3
res = np.array(res,dtype=int)
print(res.shape)
res.reshape((al,4))
#print(res)

np.savetxt('../E2/res/label/a_3.csv',res,fmt="%.0f",delimiter=',')
