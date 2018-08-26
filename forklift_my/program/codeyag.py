import sys
import time
sys.path.append(".")

import cv2
import numpy as np

cap = cv2.VideoCapture('8data.m4v')
if not cap.isOpened():
	print("not open")
	sys.exit()

fourcc = cv2.VideoWriter_fourcc(*'XVID') # ? 動画ファイルとして保存する。第１引数＝動画名、第２〜４引数＝fourcc_code,最後の引数＝isColor(true=color,false=gray)
#out1 = cv2.VideoWriter('output1.avi',fourcc, 19.0, (1280,720))
#out2 = cv2.VideoWriter('output2.avi',fourcc, 19.0, (1280,720))

#out3 = cv2.VideoWriter('output3.avi',fourcc, 19.0, (1280,720))
prev = None
curr = None
count = 1
li = [[[0 for i3 in range(8)]for i2 in range(3)]for i in range(3)]
li2 = [[[0 for i3 in range(16)]for i2 in range(3)]for i in range(3)]

inte1 = int(800 / 3)
inte2 = int(480 / 3)

f = open('result.txt','w')

while(True): #無限ループ
	ret, frame = cap.read() #フレームの読み込みが正しく行われるかによってTrueかFalseを返す。この関数の返戻値によって動画ファイルの最後まで到達したかどうかを確認できます．
	# retは画像を取得成功フラグ
	#print("frame = ",frame.shape)
	# Calculate 2 Frame OpticalFlow
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #色空間の変換。第１引数＝入力画像、返り値＝出力画像、第２引数＝変換方法　これはグレースケールに変換
	hsv = np.zeros_like(frame)   #hsv色空間を表すnumpy
	hsv[:,:,1] = 255 #saturationは使わないので255で固定
	bgr = frame
	dst2 = frame
	if prev is None:
		prev = gray
	else:
		curr = gray;
		# Optical Flow
		flow = cv2.calcOpticalFlowFarneback(prev,curr,None,0.5, 3, 15, 3, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
		# 第１引数＝前の画像　第２引数＝次の画像　返り値＝計算されたフロー画像　第４引数＝ピラミッドの各層における比　第５引数＝ピラミッドの層数
		# 第６引数＝平均化窓サイズ　第７引数＝各層におけるアルゴリズムの反復数　第８引数＝ピクセル近傍領域のサイズ　第９引数＝ガウス分布の標準偏差　第１０引数＝ガウシアンフィルタの利用
		# bestな数値は画像によって違うので、色々試しながらやってみる

		edge = cv2.Canny(curr, 300, 300) #エッジ抽出　　第１引数＝入力画像　第２、３引数＝ヒステリシスminVal,maxVal　
		# Change to Magnitude and Angle
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])  #2次元ベクトルの角度と大きさを求める。　flow[...,0] = x座標　flow[...,1] = y座標
		#第１引数＝ｘ座標の配列。必ず浮動小数点型　第２引数＝ｙ座標の配列。ｘと同じサイズ同じ型　
		#第1返り値＝大きさの出力配列、ｘと同じサイズ同じ型　第２返り値＝角度の出力配列、ｘと同じサイズ、同じ型　第３引数＝角度の表記にラジアン（デフォルト）、または度のどちらを使うか指定するフラグ

		hsv[:,:,0] = ang*180/np.pi/2  # hsv[:,:,0] = hue（移動方向） ここではhueの値をangを弧度法から度数法に変換して代入
		hsv[:,:,2] = cv2.min(mag*30,255)  # magの値が9以上の場合は255で固定
		g = hsv[:,:,2] #便宜上、代入
		hsv[:,:,2] = cv2.max(g,edge) #edgeの可能性が高ければ代入
		hsv[:,:,1] = 255-edge;  # edgeの成分が強いほど、白くなる

		#print("ang = ",ang.shape)
		for i in range(0,3) :
			for j in range(0,3) :
				print(i,j)
				for k in range(i * inte1,(i + 1) * inte1) :
					for l in range(j * inte2,(j + 1) * inte2) :
							#print("j = ",j,inte2,l)
							a = np.floor(ang[l,k]*16/(np.pi*2))
							a = int(a)
							if a > 15:
								a = 15

							#print("k = ",k,l,a,ang[l,k])
							li2[i][j][a] += mag[l,k]
#							f.write('list2[' + str(i) +'][' + str(j) + '][' + str(a) + '] = ' + str(li2[i][j][a]) + '\n')
#							#print(li2[i][j][a])
				for m in range(1,15) :
							mm = (m+1)/2
							mm = int(mm)
							li[i][j][mm] = li2[i][j][m]
#							f.write('list[' + str(i) +'][' + str(j) + '][' + str(mm) + '] = ' + str(li[i][j][mm]) + '\n')
			li[i][j][0] += (li2[i][j][0] + li2[i][j][15])


		for i in range(0,3):
			for j in range(0,3):
				for mm in range(0,8):
					f.write(str(li[i][j][mm]) + ', ')
					#print(li[i][j][mm])
		f.write('\n')
		f.flush()
		#hsv[:,:,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
		bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)  # hsvをbgrに変換
		#cv2.imshow('test',bgr)
		prev = curr

		print(count)
		cnt_pad = '%04d' % count
#   cv2.imwrite("1/img"+cnt_pad+".png", img) #画像の保存
#   cv2.imwrite("1/res"+cnt_pad+".png", res)
#   cv2.imwrite("1/dst"+cnt_pad+".png", dst2)
#	out1.write(img)
#	out2.write(res)
#	out3.write(dst2)
#   cv2.imshow('frame',img)
#   cv2.imshow('bgr',res)
#    cv2.imshow('dst2',dst2)

	count = count + 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

f.close()
cap.release()
#out1.release()
#out2.release()
#out3.release()
cv2.destroyAllWindows()
