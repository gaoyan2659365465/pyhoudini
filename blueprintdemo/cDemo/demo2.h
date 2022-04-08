#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <windows.h>
#include "cJSON.h"
//#define JSON_PATH "C:/Users/26593/Desktop/BlueprintDemo/test.json"
#define JSON_PATH "./test.json"

typedef struct Node{
    //表示一个节点
    int node_num;//节点编号
    char* node_name;//节点名字
    struct Node* new_node;//下一个节点指针
    void (*fun)(void* value);//节点函数指针
    void* value;//函数参数
    int new_nodes[20];//节点编号组-对应此节点连接的其他节点
    void* output;//函数输出
}Node;

cJSON* json = {0};//全局变量
int node_begin=-1;//BeingPlay节点的编号
int node_count=0;
Node** nodes;
cJSON* getJson();//获取json文件
int getNodeNum();//获取节点数量
void setNodes();
char* getNodeName(int i);//根据编号获取节点名
void setNodes();
void* getNodeFun(char* name);
int getNewNode(int num);
cJSON* getNodeSocket(int num);
char* getValue(int num,char* s_num);
void getNewNodes(int num);
void setNewNode(int num,int socket_num);
void runFuns();