import os

from dotenv import load_dotenv
from openai import OpenAI
from openai import BadRequestError

SYSTEM_MESSAGE = "你是python学习助手"


def require_env(name: str) -> str:
    """读取必需环境变量。"""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"缺少环境变量 {name}，"
            "请检查项目根目录下的 .env 文件。"
        )

    return value


def main():
    load_dotenv()

    api_key = require_env("LLM_API_KEY")
    base_url = require_env("LLM_BASE_URL")
    model_id = require_env("LLM_MODEL_ID")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE,
        },
    ]

    try:
        user_message = input("请输入问题：").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n程序退出。")
        return

    if not user_message:
        print("用户问题不能为空。")
        return

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
    )

    answer = response.choices[0].message.content

    print(answer)


if __name__ == '__main__':
    main()
