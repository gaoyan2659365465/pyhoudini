#include "demo2.h"

void printString(void* value){
    //printf("PrintString\n");
    int node_num = (int)value;
    char* str = getValue(node_num,"2");
    printf("%s\n", str);
    
    // HMODULE module = LoadLibraryA("tanchuang.dll");
    // if (module == NULL) {
    //     system("error load");
    // }
    // void(*tanchuang)() = NULL;
    // tanchuang = (void(*)())GetProcAddress(module, "tanchuang1");
    // if (tanchuang != NULL) {
    //     tanchuang();
    // }
}

void beginPlay(void* value){
    //printf("BeginPlay\n");
}

void branch(void* value){
    //printf("Branch\n");
    int node_num = (int)value;
    char* str = getValue(node_num,"1");
    if (strcmp(str, "True") == 0) {
		setNewNode(node_num,2);//2��True��3��False
        //printf("True\n");
        return;
    }
    if (strcmp(str, "False") == 0){
        setNewNode(node_num,3);
        //printf("False\n");
        return;
    }
    return ;
}

void forLoop(void* value){
    //printf("ForLoop\n");
    int node_num = (int)value;
    char* str = getValue(node_num,"2");//LastIndex
    int a = atoi(str);
    setNewNode(node_num,3);//3��Loop Body

    Node* node_;
    for(int i=0;i<a;++i){
        nodes[node_num]->output = (void*)i;//���
        node_ = nodes[node_num]->new_node;
        while(1){
            if (node_ == NULL) {
			    break;
		    }
            node_->fun((void*)node_->node_num);
            node_ = node_->new_node;
        }
    }
    setNewNode(node_num,5);//5��Completed
    return ;
}

void intToString(void* value){

}

cJSON* getJson(){
    //���ļ���ȡjson
    FILE *f;//�����ļ�
    long len;//�ļ�����
    char *content;//�ļ�����
    f=fopen(JSON_PATH,"r");
    fseek(f,0,SEEK_END);
    len=ftell(f);
    fseek(f,0,SEEK_SET);
    content=(char*)malloc(len+1);
    if (!content) { return json; }
    if (sizeof(content) > len) { return json; }
    fread(content,1,len,f);
    fclose(f);

    json=cJSON_Parse(content);
    if (!json) {
        printf("Error before: [%s]\n",cJSON_GetErrorPtr());
    }
    return json;
}

int getNodeNum(){
    //��ȡ�ڵ�����
    cJSON* json2 = cJSON_GetObjectItem(json,"bp_data");
    if(json2 == NULL){
        return 0;
    }
    node_count=cJSON_GetObjectItem(json2,"node_num")->valueint;
    return node_count;
}

char* getNodeName(int i){
    //��ȡ�ڵ�����
    char ptr[10];
    itoa(i,ptr,10);//����ת�ַ���
    cJSON* json2 = cJSON_GetObjectItem(json,ptr);
    if(json2 == NULL){
        return NULL;
    }
    char *out=cJSON_GetObjectItem(json2,"class_name")->valuestring;
    return out;
}

void* getNodeFun(char* name){
    //����ڵ��������غ���ָ��
    if(strcmp(name, "BP_Node_BeginPlay") == 0){
        return beginPlay;
    }
    else if (strcmp(name, "BP_Node_Branch") == 0)
    {
        return branch;
    }
    else if (strcmp(name, "BP_Node_ForLoop") == 0)
    {
        return forLoop;
    }
    else if (strcmp(name, "BP_Node_PrintString") == 0)
    {
        return printString;
    }
    else if (strcmp(name, "BP_Node_IntToString") == 0)
    {
        return intToString;
    }
    return NULL;
}

int getNewNode(int num){
    //ͨ��edge_uuid��ȡ��һ��Node
    char ptr[10];
    itoa(num,ptr,10);//����ת�ַ���
    cJSON* json2 = cJSON_GetObjectItem(json,ptr);
    if(json2 == NULL){
        return -1;
    }
    json2=cJSON_GetObjectItem(json2,"bp_node");
    int new_socket_num=cJSON_GetObjectItem(json2,"new_socket_num")->valueint;
    //printf("%d\n",new_socket_num);
    json2=cJSON_GetObjectItem(json2,"data_edges");
    char ptr2[10];
    itoa(new_socket_num,ptr2,10);//����ת�ַ���
    json2=cJSON_GetObjectItem(json2,ptr2);
    if(json2 == NULL){
        return -1;
    }
    json2=cJSON_GetObjectItem(json2,"0");
    if (json2 == NULL) {
        return -1;
    }
    json2=cJSON_GetObjectItem(json2,"0");
    char *out=cJSON_GetObjectItem(json2,"edge_uuid")->valuestring;
    //printf("%s\n",out);

    for (int i=0; i<node_count; ++i){
        char ptr3[10];
        itoa(i,ptr3,10);//����ת�ַ���
        json2 = cJSON_GetObjectItem(json,ptr3);
        if(json2 == NULL){
            continue;
        }
        json2=cJSON_GetObjectItem(json2,"bp_node");
        json2=cJSON_GetObjectItem(json2,"data_edges");
        for(int n=0; n<10; ++n){
            //һ���ڵ����10�����
            char ptr4[10];
            itoa(n,ptr4,10);//����ת�ַ���
            cJSON* json3=cJSON_GetObjectItem(json2,ptr4);
            if(json3 == NULL){
                continue;
            }
            for(int m=0; m<10; ++m){
                //һ��������10����
                char ptr5[10];
                itoa(m,ptr5,10);//����ת�ַ���
                cJSON* json4=cJSON_GetObjectItem(json3,ptr5);
                if(json4 == NULL){
                    continue;
                }
                json4=cJSON_GetObjectItem(json4,"0");
                char *out1=cJSON_GetObjectItem(json4,"edge_uuid")->valuestring;
                if(strcmp(out, out1) == 0){
                    if(num == i){
                        continue;
                    }
                    //printf("%d��һ���ڵ��ţ�%d\n",num,i);
                    return i;
                }
            }
        }
    }
    return -1;
}

cJSON* getNodeSocket(int num){
    //��ȡ�ڵ��۵�ָ��
    char ptr[10];
    itoa(num,ptr,10);//����ת�ַ���
    cJSON* json2 = cJSON_GetObjectItem(json,ptr);
    if(json2 == NULL){
        return NULL;
    }
    json2 = cJSON_GetObjectItem(json2,"bp_node");
    json2 = cJSON_GetObjectItem(json2,"w_node");
    json2 = cJSON_GetObjectItem(json2,"node_data");
    return json2;
}

char* getValue(int num,char* s_num){
    //��ȡָ��socket��ֵ
    cJSON* json2 = nodes[num]->value;
    if(!json2){
        printf("��\n");
    }
    json2 = cJSON_GetObjectItem(json2,s_num);
    char* out = cJSON_GetObjectItem(json2,"input_value")->valuestring;
    return out;
}

void getNewNodes(int num){
    //��ȡ�ڵ�ı����
    //printf("��ǰ��%d�Žڵ�", num);
    char ptr[10];
    itoa(num,ptr,10);//����ת�ַ���
    cJSON* json6 = cJSON_GetObjectItem(json,ptr);
    if(json6 == NULL){
        return;
    }
    json6=cJSON_GetObjectItem(json6,"bp_node");
    json6=cJSON_GetObjectItem(json6,"data_edges");
    for(int a=0; a<20; ++a){
        char ptr2[10];
        itoa(a,ptr2,10);//����ת�ַ���
        cJSON* json5=cJSON_GetObjectItem(json6,ptr2);
        if(json5 == NULL){
            continue;
        }
        json5=cJSON_GetObjectItem(json5,"0");
        if (json5 == NULL) {
            continue;
        }
        json5=cJSON_GetObjectItem(json5,"0");
        char *out=cJSON_GetObjectItem(json5,"edge_uuid")->valuestring;
        //printf("%s\n", out);
        for (int i=0; i<node_count; ++i){
            char ptr3[10];
            itoa(i,ptr3,10);//����ת�ַ���
            cJSON* json2 = cJSON_GetObjectItem(json,ptr3);
            if(json2 == NULL){
                continue;
            }
            json2=cJSON_GetObjectItem(json2,"bp_node");
            json2=cJSON_GetObjectItem(json2,"data_edges");
            for(int n=0; n<20; ++n){
                //һ���ڵ����20�����
                char ptr4[10];
                itoa(n,ptr4,10);//����ת�ַ���
                cJSON* json3=cJSON_GetObjectItem(json2,ptr4);
                if(json3 == NULL){
                    continue;
                }
                for(int m=0; m<20; ++m){
                    //һ��������20����
                    char ptr5[10];
                    itoa(m,ptr5,10);//����ת�ַ���
                    cJSON* json4=cJSON_GetObjectItem(json3,ptr5);
                    if(json4 == NULL){
                        break;
                    }
                    json4=cJSON_GetObjectItem(json4,"0");
                    char *out1=cJSON_GetObjectItem(json4,"edge_uuid")->valuestring;
                    if(strcmp(out, out1) == 0){
                        if(num == i){
                            break;
                        }
                        //printf("%d��һ���ڵ��ţ�%d\n",num,i);
                        nodes[num]->new_nodes[a] = i;
                    }
                }
            }
        }
    }
    return;
}

void setNewNode(int num,int socket_num){
    //������һ���ڵ�
    int new_node_num = nodes[num]->new_nodes[socket_num];
    //���ݽڵ��Ż�ȡ��������
    if (new_node_num == -1) {
        nodes[num]->new_node = NULL;
        return;
    }
    nodes[num]->new_node = nodes[new_node_num];
}

void setNodes(){
    //����������
    int nodes_size = sizeof(Node) * node_count;
    nodes=(Node**)malloc(nodes_size);
    if (!nodes) { return; }
    memset(nodes, 0, nodes_size);

    for (int i=0; i<node_count; ++i){
        char* name = getNodeName(i);
        if(strlen(name) == 0){
            break;
        }
        if (nodes_size < sizeof(Node)) { return; }
        nodes[i]=(Node*)malloc(sizeof(Node));
        if (!nodes[i]) { return; }
        nodes[i]->node_num = i;
        nodes[i]->node_name = name;
        nodes[i]->new_node = NULL;
        nodes[i]->fun = getNodeFun(name);
        nodes[i]->value = getNodeSocket(i);
        if(strcmp(name, "BP_Node_BeginPlay") == 0){
            node_begin = i;
            //printf("��ʼ�ڵ��ţ�%d\n",node_begin);
        }
        
        for(int n=0; n<20; ++n){
            nodes[i]->new_nodes[n] = -1;
        }
        getNewNodes(i);
    }

    for (int i=0; i<node_count; ++i){
        int newnum = getNewNode(i);
        if(newnum == -1){continue;}
        nodes[i]->new_node = nodes[newnum];
    }
}

void runFuns(){
    //�������庯����
    Node* node_0 = nodes[node_begin];
    node_0->fun((void*)node_0->node_num);
	while (1)
	{
		if (node_0->new_node == NULL) {
			break;
		}
		node_0->new_node->fun((void*)node_0->new_node->node_num);
		node_0 = node_0->new_node;
		if (node_0 == NULL) {
			break;
		}
	}
}

int main(){
    getJson();
    getNodeNum();
    setNodes();
    runFuns();
}