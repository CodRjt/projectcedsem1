#include<stdio.h>
int check(int n;int arr[n]){
    for(int i=0;i<n+1;i++){
        if (arr[i]==n){
            return 1;
        }
        else
            return 0;
    }
}
int recman(int n){
    int arr[n],c=0;
     if (n==0){
        arr[c++]=0;
       return 0;
    }
    else {
        if(n>0 &&  check(n)){
            return recman(n-1)-n
        } 
        else {
            return recman(n-1)+n;
        }
    }
}