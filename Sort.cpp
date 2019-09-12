#include<iostream>
using namespace std;

//swap
//
void swap(int & a, int & b){
	int c = a ;
	a = b;
	b = c;
}

// 冒泡排序 O(n^2) 稳定
//
void bubble_sort(int a[], int m, int n){
	for(int i = 0; i < n-1 ;i++)
	       for(int j = n -1; j > i ; j--){
	       		if(a[j] < a[j-1])
		 		swap(a[j],a[j-1]);
	       }	
}


//选择排序 O(n^2) 不稳定
//
void select_sort(int a[], int m ,int n){
	for(int i = 0 ; i < n-1 ; i++){
		int num = i;
		int j ;
		for(j = i + 1 ; j < n ;j++){
			if(a[num] > a[j])
				num  = j;
		}
		swap(a[num],a[i]);
	} 
}

//插入排序 O(n^2) 稳定
//
void insert_sort(int a[], int m , int n){
	for(int i = 1; i < n ; i++){
		int num  = a[i];
		int j ;
		for(j = i-1 ;j >= 0 && num < a[j];j--)
			swap(a[j] , a[j+1]);
	}
}


//希尔排序 O(1^(1~2) 不稳定
//
void shell_sort(int a[] ,int m ,int n){
	int h = 1;
	while(h < n / 3)
		h = h*3 + 1;
	
	while(h>=1){
		for(int i = h ; i < n ; i++){
			int num = a[i];
			int j ;
			for(j = i ; j >= h && num < a[j-h]; j -= h)
				a[j] = a[j-h];
			a[j] = num;
		}
		h /= 3;
	}
}


//归并排序 O(nlogn) 稳定
//
void merge(int a[] ,int m ,int n){
	int * cont = new int[n-m+1];
	int mid = (m + n) / 2;
	int ss = m;
	int sb = mid ;
	int k = 0;

	while(ss < mid && sb < n){

		if(a[ss] < a[sb])	
			cont[k++] = a[ss++];
		else
			cont[k++] = a[sb++];
	}

	while(ss < mid)
		cont[k++] = a[ss++];
	while(sb <= n) 
		cont[k++] = a[sb++];

	for(int j = 0 ; j < k  ;j++)
		a[m+j] = cont[j];
	delete [] cont;
}
//
void merge_sort(int a[], int m, int n){
	if(n -1 > m){
		int mid = (m + n) / 2 ;
		merge_sort(a , m , mid);
		merge_sort(a , mid, n);
		merge(a , m , n);
	}
}

//快速排序 O(nlogn) 不稳定
//
void quick_sort(int a[] , int m ,int n){
	if(n > m){
		int s = m;
		int e = n - 1;
		
		int num = a[m];
		while(e > s){
			while(e > s && a[e] > num)
				e--;
			swap(a[e],a[s++]);
		    while(e > s && a[s] < num)
			   s++;
		    swap(a[s] , a[e--]);
		} 
			
		a[s] = num;
		quick_sort(a,m,s);
		quick_sort(a,s+1,n);

	}
}

//堆排序 O(nlogn) 不稳定
//

void adjust(int a[] ,int m ,int n){
	int left = 2*m+1;
	int right = 2*m+2;
	int Max = m;
	if(left < n && a[Max] < a[left])
		Max = left;
	if(right < n && a[Max] < a[right])
		Max = right;
	
	if(Max != m){
		swap(a[Max], a[m]);
		adjust(a,Max,n);
	}
}

//
void heap_sort(int a[] ,int m , int n){
        for(int i = m / 2 ; i>= 0 ; i--)
                adjust(a, i , n);

        for(int j = n -1 ;j > 0 ; j--){
                swap(a[0] , a[j]);
                adjust(a,0,j);
        }

}



//计数排序 O(n + k) 稳定
//

void counting_sort(int a[] ,int m ,int n){

	int minNum = 1 << 30;
	int maxNum = -(1<<30);

	for(int i = 0 ; i < n ; i++){
		if(a[i] > maxNum)
			maxNum = a[i];
		if(a[i] < minNum)
			minNum = a[i];
	}
	
	int * cont = new int[maxNum - minNum + 1];
	for(int i = 0 ; i < maxNum - minNum + 1 ;i++)
		cont[i] = 0;

	for(int i = 0 ; i < n ; i++)
		cont[a[i] - minNum]++;

	for(int i = 1 ; i < maxNum - minNum + 1 ; i++)
		cont[i] += cont[i-1];
	
	int *res = new int[n];
	
	for(int i = n -1 ; i >= 0 ; i--){
		res[cont[a[i]] -1] = a[i];
		cont[a[i]]--;
	}

	for(int i = 0 ; i < n ; i++)
		a[i] = res[i];

}


int main(){
	int a[10] = {4,58,92, 0,444, 1, 87 ,6,444,9};
	//bubble  select  insert  shell  merge  quick  heap  counting
	merge_sort(a,0,10);

	for(int i = 0; i < 10; i++)
		cout << a[i] << endl;
	return 0;

}
