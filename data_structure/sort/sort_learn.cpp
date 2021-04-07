// 注意1: sort函数的头文件是 <algorithm>
#include<algorithm>
#include<vector>
// 注意2: 输入输出流也需要头文件
#include<iostream>
// 注意3: 随机函数的头文件是 time.h 不是 rand
#include<time.h>

// 工具函数
void showArr(std::vector<int> in, std::string info = "");
std::vector<int> getRandonArr(int num, int start, int end);

// 注意4:
// sort排序默认是从小到大，
// 可以自定义排序函数。注意参数是值传递 不是引用。
bool myArrBiger(int i, int j);





int main(){
    //seed();
    std::vector<int> arr = getRandonArr(10, 0, 10);
    showArr(arr, "arr in:");

    // 注意5:
    // 参数是起始位置，终止位置，和比较函数；比较函数默认是从小到大
    std::sort(arr.begin(), arr.end());
    showArr(arr, "arr default out:");

    std::sort(arr.begin(), arr.end(), myArrBiger);
    showArr(arr, "arr myBigger out:");

}


// 注意，string也需要std
void showArr(std::vector<int> in, std::string info){
    if (info != ""){
        std::cout << info << "\n";
    }
    for (auto ele : in){
        std::cout << ele << " ";
    }
    std::cout << "\n";
}


std::vector<int> getRandonArr(int num, int start, int end){
    std::vector<int> res(num, 0);
    for(int i = 0; i < num; i++){
        res[i] = rand()%(end - start + 1) + start;
    }
    return res;
}

bool myArrBiger(int i, int j){
    return i > j;
}