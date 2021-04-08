// 注意1: sort函数的头文件是 <algorithm>
#include<algorithm>
#include<vector>
// 注意2: 输入输出流也需要头文件
#include<iostream>
// 注意3: 随机函数的头文件是 time.h 不是 rand
#include<time.h>


class Node{
public:
    int value;
    Node* next;
};

// 工具函数
void showArr(std::vector<int> in, std::string info = "");
std::vector<int> getRandomArr(int num, int start, int end);
void showList(Node* in, std::string info = "");
Node* getRandomList(int num, int start, int end);
// 注意4:
// sort排序默认是从小到大，
// 可以自定义排序函数。注意参数是值传递 不是引用。
bool myArrBiger(int i, int j);

// 冒泡排序
void myPopSort(std::vector<int> & arr);

// 快速排序
void myQuickSort(std::vector<int> & arr);

// 选择排序
void mySelectSort(std::vector<int> & arr);

// 插入排序
void myInsertSort(std::vector<int> & arr);

// 归并排序
void myMergeSort(std::vector<int> & arr);


// 链表归并排序
Node*  myMergeSort(Node* head);

// 堆排序
void myHeapSort(std::vector<int> & arr);

// 希尔排序


int main(){
    //seed();
    srand(time(0));
    std::vector<int> arr = getRandomArr(10, 0, 10);
    showArr(arr, "arr in:");

    // 注意5:
    // 参数是起始位置，终止位置，和比较函数；比较函数默认是从小到大
    std::sort(arr.begin(), arr.end());
    showArr(arr, "arr default out:");

    std::sort(arr.begin(), arr.end(), myArrBiger);
    showArr(arr, "arr myBigger out:");


    // 冒泡排序
    arr = getRandomArr(10, 0, 10);showArr(arr, "arr in:");
    myPopSort(arr);showArr(arr, "arr myPopSort out:");


    // 快速排序 bad
    arr = getRandomArr(20, 0, 10);showArr(arr, "arr in:");
    myQuickSort(arr);showArr(arr, "arr myQuickSort out:");

    // 选择排序 bad
    arr = getRandomArr(30, 0, 10);showArr(arr, "arr in:");
    mySelectSort(arr);showArr(arr, "arr mySelectSort out:");

    // 插入排序 ok
    arr = getRandomArr(30, 0, 10);showArr(arr, "arr in:");
    myInsertSort(arr);showArr(arr, "arr myInsertSort out:");

    // 归并排序 bad
    arr = getRandomArr(5, 0, 10);showArr(arr, "arr in:");
    myMergeSort(arr);showArr(arr, "arr myMergeSort out:");

    Node* list = getRandomList(5,0,10);showList(list, "list in");
}


// 注意，string也需要std
void showArr(std::vector<int> in, std::string info){
    if (info != ""){
        std::cout << info << "\n ";
    }
    for (auto ele : in){
        std::cout << ele << " ";
    }
    std::cout << "\n";
}

// 注意，string也需要std
void showList(Node* in, std::string info){
    if (info != ""){
        std::cout << info << "\n ";
    }
    while (in){
        std::cout << in->value << " ";
        in = in->next;
    }
    std::cout << "\n";
}


std::vector<int> getRandomArr(int num, int start, int end){
    std::vector<int> res(num, 0);
    for(int i = 0; i < num; i++){
        res[i] = rand()%(end - start + 1) + start;
    }
    return res;
}


Node* getRandomList(int num, int start, int end){
    if (num <= 0) return NULL;
    std::vector<int> res(num, 0);
    for(int i = 0; i < num; i++){
        res[i] = rand()%(end - start + 1) + start;
    }

    Node* head = new Node;
    head->value = res[0];
    Node* last = head;
    for(int i = 1; i < num; i++){
        Node* cur = new Node;
        cur->value = res[i];
        last->next = cur;
        last = last->next;
        std::cout << cur->value << " " ;
    }
    std::cout << head->value << " " ;
    return head;
}

bool myArrBiger(int i, int j){
    return i > j;
}

// 冒泡排序
void myPopSort(std::vector<int> & arr){
    int n = arr.size();
    bool isSwap = true;
    for(int i = 0; i < n; i++){
        if (!isSwap){
            break;
        }
        isSwap = false;
        for(int j = 0; j < n-i-1; j++){
            if (arr[j] > arr[j+1]){
                std::swap(arr[j], arr[j+1]);
                isSwap = true;
            }
        }
    }
}


int getMid(std::vector<int>& arr, int start, int end/*不包含 */){
    int curIndex = rand() % (end - start) + start;
    std::swap(arr[start], arr[curIndex]);

    int i = start;
    int j = end-1;
    while(i < j){
        while(i < j && arr[i] <= arr[j]){
            j--;
        }
        if (i < j){
            std::swap(arr[i], arr[j]);
            i++;
        }
        while(i < j && arr[i] <= arr[j]){
            i++;
        }
        if (i < j){
            std::swap(arr[i], arr[j]);
            j--;
        }
    }
    return i;
}


void myQuickSortSub(std::vector<int>& arr, int start, int end/*不包含 */){
    if (start < 0 || end > arr.size() || start >= end-1) return;
    int mid = getMid(arr, start, end);
    myQuickSortSub(arr, start, mid);
    myQuickSortSub(arr, mid+1, end); // 这里不能是mid，不然对于[8,8]会死循环
}
// 快速排序
void myQuickSort(std::vector<int> & arr){
    myQuickSortSub(arr, 0, arr.size());
}


/*
9 1 4
*/
// 选择排序
void mySelectSort(std::vector<int> & arr){
    int n = arr.size();
    for(int i = 0; i < n; i++){
        int min = arr[i];
        int minIndex = i;
        for(int j = i+1; j < n; j++){
            if (arr[j] < min){
                minIndex = j;
                min = arr[j]; // 注意：不要忘了这句
            }
        }
        if (minIndex != i) std::swap(arr[i], arr[minIndex]);
    }
}

// 插入排序
void myInsertSort(std::vector<int> & arr){
    int n = arr.size();
    for(int i = 1; i < n; i++){
        for(int j = i-1; j >= 0; j--){
            if (arr[j+1] < arr[j]){
                std::swap(arr[j+1], arr[j]);
            }else{
                break;
            }
        }
    }
}

void myMergeSortSub(std::vector<int> & arr, int start, int end){
    if (start < 0 || end > arr.size() || start >= end - 1) return;
    int n = end - start;
    int mid = n/2 + start;
    myMergeSortSub(arr, start, mid);
    myMergeSortSub(arr, mid, end);

    // merge
    std::vector<int> buff(arr.begin(), arr.end());

    int i = start;
    int j = mid;
    int buffI = start;

    while(i < mid || j < end){
        while(i < mid && (j >= end || arr[i] <= arr[j])){
            buff[buffI] = arr[i];
            buffI++;
            i++;
        }
        // j
        while(j < end && (i >= mid || arr[j] < arr[i])){ //todo <= ?
            buff[buffI] = arr[j];
            buffI++;
            j++;
        }
    }
    arr = buff; // 注意：别忘了 赋值回去
}
// 归并排序
void myMergeSort(std::vector<int> & arr){
     myMergeSortSub(arr, 0, arr.size());
}


int getListLen(Node* head){
    int res = 0;
    while(head){
        res += 1;
        head = head->next;
    }
    return res;
}

// 3 5 6; 1
Node* cut(Node* head, int len){
    Node* last = head;
    while(last!= NULL && len > 1){
        last = last->next;
        len -= 1;
    }
    Node* res = NULL;
    if (last) {
        Node* res = last->next;
        last->next = NULL;
    }
    return res;
}

// 链表归并排序,
// 5 3 1 10 2
Node* myMergeSort(Node* head){
    int listLen = getListLen(head);
    if (listLen <= 1) return head;
    int mid = listLen/2;

    Node* midHead = cut(head, mid);
    myMergeSort(head);
    myMergeSort(midHead);
    Node* res = new Node;
    Node* resCur = res;
    Node* headCur = head;
    Node* midHeadCur = midHead;
    /*
    1
    7
    */
    while(headCur != NULL|| midHeadCur != NULL){
        while(headCur != NULL && (midHeadCur == NULL || headCur->value <= midHeadCur->value)){
            resCur->next = headCur;
            resCur = resCur->next;
            headCur = headCur->next;
        }
        while(midHeadCur != NULL && (headCur == NULL || headCur->value > midHeadCur->value)){
            resCur->next = midHeadCur;
            resCur = resCur->next;
            midHeadCur = midHeadCur->next;
        }
    }
    return res->next;
}

// 堆排序
void myHeapSort(std::vector<int> & arr){
}

