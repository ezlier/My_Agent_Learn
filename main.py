import os

import logging
from dotenv import load_dotenv
from openai import OpenAI

import check

SYSTEM_MESSAGE = """
     "你是python学习助手",
     "请严格按照以下json格式返回内容，不要使用markdown",
     "除了最外层answer其他都可为None",
     "{
          "answer": "……",
          "topic": "……",
          "summary": "……",
          "key_points": [
            "……",
            "……"
          ],
          "quiz": [
            {
              "question": "……",
              "answer": "……"
            }
          ]
        }",
     """


def require_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"缺少环境变量 {name}，请检查项目根目录下的 .env 文件。"
        )

    return value


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )

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

    while True:
        try:
            user_message = input("请输入问题：").strip()
        except (KeyboardInterrupt, EOFError):
            logging.info("程序退出")
            return

        if not user_message:
            logging.warning("用户问题不能为空。")
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

        content = response.choices[0].message.content

        lesson = check.parse_json(content)

        logging.info("助手回答：" + lesson.answer)

        messages.append(
            {
                "role": "assistant",
                "content": lesson,
            }
        )


if __name__ == '__main__':
    main()
