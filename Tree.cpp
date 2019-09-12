#include<iostream>
#include<stack>

using namespace std;

void pre_order(TreeNode * root){
	if(!root)
		return ;
	stack<TreeNode * > Q;
	while(root || !Q.empty()){
		if(root){
			cout << root -> val << endl;
			Q.push(root);
			root = root -> left;
		}
		else{
			root = Q.top();
			Q.pop();
			root = root -> right;
		}
	}

}



void in_order(TreeNode * root){
	
	if(!root)
		return ;
	stack<TreeNode *> Q;
	while(root || !Q.empty()){
		if(root){
			Q.push(root);
			root = root -> left;
		}
		else {
			root = Q.top();
			cout << root -> val << endl;
			Q.pop();
			root = root -> left
		}
	}
}

void post_order(TreeNode * root){
	if(!root)
		return ;
	stack<TreeNode *> Q;
	TreeNode * pre = nullptr;
	while(root || !Q.empty()){
		if(root){
			Q.push(root);
			root = root -> val;
		}
		else{
			root = Q.top();
			if(root -> right == nullptr || root -> right == pre){
				Q.pop();
				cout << root -> val << endl;
				pre = root ;
				root = nullptr;
			}
			else
				root = root -> right;
		}
	}

			
}
