#generate labels which is no dengerous case

import numpy as np
while(True):
    print("input frame number:")
    al = int(raw_input())       # number of all frame
    print("input file number:")
    num = raw_input()           # file number
    res = [[0,1] for i in range(al-1)]

    res = np.array(res,dtype=int)
    print(res.shape)
    res.reshape((al-1,2))       # delete frist line
    #print(res)
    name = '../E2/res/label/B/b_' + str(num) + '_2.csv'
    np.savetxt(name,res,fmt="%.0f",delimiter=',')
