
### BINARY SEARCH 


l = [2,3,5,6,7,8,9,12,21,32,45]
target = 32
low = 0 

high = len(l)-1


while low<=high : 
    print(low,high)
    mid = (low+high) // 2 
    print(mid,"element at mid " , l[mid])
    if l[mid] == target : 
        print(mid)
        break
    elif l[mid] > target : 
        high = mid -1
    else:
        low = mid + 1 
    
    