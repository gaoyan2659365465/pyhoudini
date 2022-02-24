from flask import Flask,request,send_file


n_version = '1.5.3'
app = Flask(__name__)

# 版本查询
@app.route('/version',methods=['GET'])
def freeze_vaersion():
    return n_version

# 获取最新文件
@app.route('/new/app',methods=['GET'])
def freeze_new_app():
    # 新版本文件路径
    file_path="pyhoudini{}.zip".format(n_version)
    return send_file(file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=False)