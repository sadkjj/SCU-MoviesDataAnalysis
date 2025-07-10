from flask import Blueprint, request, jsonify, session
import os
from openai import OpenAI
AI_bp= Blueprint('AI', __name__)
@AI_bp.route('/dialog', methods=['GET'])
def AIDialog():
    """
    AI对话接口
    GET /AIDialog

    
    请求参数: {
        "question": "你能告诉我关于电影的什么信息？"
    }
    """
    message=request.args.get('message', type=str)
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-d47891adcc8e428384d476a5032e098d",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {'role': 'user', 'content': message}
        ]
    )
    print(completion.choices[0].message.content)
    response = {
        "message": completion.choices[0].message.content
    }
    return jsonify(response), 200