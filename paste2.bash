#!bin/bash
home="$HOME/../../mnt/c/Users/forklift/Desktop/forklift"
for i in $(seq 1 15)
do
  for j in A B C
  do
    cd $home
    cd "E2/res"
    pwd
    #cat $name
    paste -d , "../${j}_res/3_3/${i}_e_3_3e2.csv" "../${j}_res/5_5/${i}_e_5_5e2.csv" "../${j}_res/7_7/${i}_e_7_7e2.csv" > "${j}/${i}e2.csv"
  done
done
