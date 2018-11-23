#!bin/bash
home="$HOME/mnt/c/Users/forklift/Desktop/forklift"
for i in $(seq 1 15)
do
  for j in 3 5 7
  do
    cd home
    cd "E2/res"
    name = "{$j}_e_{$i}_{$i}e2.csv"
    cat name
    paste -d , "A_res/$name" "B_res/$name" "C_res/$name" > $name
  done
done
