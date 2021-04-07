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

// 冒泡排序
void myPopSort(vector<int> & arr);

// 快速排序
void myQuickSort(vector<int> & arr);

// 选择排序
void mySelectSort(vector<int> & arr);

// 插入排序
void myInsertkSort(vector<int> & arr);

// 归并排序
void myMergeSort(vector<int> & arr);

class Node{

};
// 链表归并排序
void myMergeSort(Node* ptr);

// 堆排序
void myHeapSort(vector<int> & arr);

// 希尔排序


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

// 冒泡排序
void myPopSort(vector<int> & arr){
    int n = arr.size();
    bool isSwap = true;
    for(int i = 0; i < n; i++){
        if (!isSwap){
            break;
        }
        isSwap = false;
        for(int j = 0; j < n-i-1; j++){
            if (arr[j] > arr[j+1]){
                swap(arr[j], arr[j+1]);
                isSwap = true;
            }
        }
    }
}

int getMid(vector<int>& arr, int start, int end/*不包含 */){
    int curIndex = rand() % (end - start) + start;
    swap(arr[start], arr[curIndex]);

    int i = start;
    int j = end-1;
    while(i <= j){
        while(i <= j && arr[i] <= arr[j]){
            j--;
        }
        if (i <= j){
            swap(arr[i], arr[j]);
            i++;
        }
        while(i <= j && arr[i] <= arr[j]){
            i++;
        }
        if (i <= j){
            wap(arr[i], arr[j]);
            j--;
        }
    }
    return i;
}


void myQuickSortSub(vector<int>& arr, int start, int end/*不包含 */){
    if (start < 0 || end > arr.size() || start >= end-1) return;
    int mid = getMid(arr, start, end);
    myQuickSortSub(arr, start, mid);
    myQuickSortSub(arr, mid, end);
}
// 快速排序
void myQuickSort(vector<int> & arr){
    int mid = select(arr);


}

// 选择排序
void mySelectSort(vector<int> & arr);

// 插入排序
void myInsertkSort(vector<int> & arr);

// 归并排序
void myMergeSort(vector<int> & arr);


// 链表归并排序
void myMergeSort(Node* ptr);

// 堆排序
void myHeapSort(vector<int> & arr);

