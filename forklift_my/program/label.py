

import numpy as np

no = 97     #   frame number starting label
ma = 1285   #   frame number starting not label
al = 1319　　#    all frame number of video


#   generate label
res = [[0,1] for i in range(no-2)]
res2 = [[1,0] for i in range(no-1,ma-1)]
res3 = [[0,1] for i in range(ma-1,al)]


res = res + res2 + res3
res = np.array(res,dtype=int)
print(res.shape)

res.reshape((al-1,2)) # delete first line

#print(res)

np.savetxt('../E2/res/label/B2/b_3_2.csv',res,fmt="%.0f",delimiter=',')
