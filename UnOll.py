import argparse
import requests
import json
from typing import List, Optional


class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.current_model = None
        self._validate_connection()

    def _api_url(self, endpoint: str) -> str:
        """构造完整的API地址"""
        return f"{self.host}{endpoint}"

    def _validate_connection(self):
        """验证服务可用性"""
        try:
            requests.get(self._api_url("/"), timeout=5)
        except requests.ConnectionError:
            print(f"无法连接到 Ollama 服务 ({self.host})")
            exit(1)

    def get_available_models(self) -> List[str]:
        """获取所有可用模型列表"""
        try:
            response = requests.get(self._api_url("/api/tags"), timeout=10)
            response.raise_for_status()
            return [model["name"] for model in response.json().get("models", [])]
        except Exception as e:
            print(f"获取模型列表失败: {str(e)}")
            return []

    def set_model(self, model_name: str) -> bool:
        """设置当前模型"""
        available = self.get_available_models()
        if model_name in available:
            self.current_model = model_name
            return True
        print(f"模型 '{model_name}' 不存在，可用模型：{available}")
        return False

    def generate_response(self, prompt: str, stream: bool = False) -> str:
        """生成对话响应"""
        if not self.current_model:
            print("未选择模型，请先使用 --model 参数指定")
            return ""

        payload = {"model": self.current_model, "prompt": prompt, "stream": stream}

        try:
            response = requests.post(self._api_url("/api/generate"), json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "").strip()

        except requests.HTTPError as e:
            print(f"请求失败: HTTP {e.response.status_code}")
            if e.response.status_code == 404:
                print(f"提示：请确认模型 {self.current_model} 是否已下载")
            return ""
        except Exception as e:
            print(f"请求异常: {str(e)}")
            return ""


def main():
    parser = argparse.ArgumentParser(description="Ollama 命令行客户端",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", help="Ollama 服务地址（例如：http://10.0.0.1:11434）", default="http://localhost:11434")
    parser.add_argument("-m", "--model", help="指定使用的模型")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用模型并退出")
    parser.add_argument("-p", "--prompt", help="直接执行提示并退出（非交互模式）")
    parser.add_argument("-s", "--stream", action="store_true", help="启用流式输出（仅非交互模式有效）")

    args = parser.parse_args()

    # 初始化客户端
    client = OllamaClient(host=args.host.rstrip('/'))

    # 处理列表模型请求
    if args.list:
        models = client.get_available_models()
        print("可用模型：")
        print("\n".join(f" - {m}" for m in models))
        return

    # 处理模型选择
    if args.model:
        if not client.set_model(args.model):
            exit(1)
    else:
        # 自动选择第一个可用模型
        available = client.get_available_models()
        if available:
            client.current_model = available[0]
            print(f"自动选择模型: {client.current_model}")
        else:
            print("没有可用模型，请先下载模型")
            exit(1)

    # 非交互模式处理
    if args.prompt:
        response = client.generate_response(args.prompt, args.stream)
        if args.stream:
            print("[流式输出未实现]")
        else:
            print(f"\n[响应] {response}")
        return

    # 交互模式
    print(f"Ollama 交互客户端 | 模型: {client.current_model} | 服务端: {args.host}")
    print("命令：/list - 列出模型 /switch <模型> - 切换模型 /exit - 退出")
    try:
        while True:
            prompt = input("You: ").strip()
            if not prompt:
                continue

            # 处理命令
            if prompt.startswith("/"):
                cmd = prompt[1:].split()
                if cmd[0] == "exit":
                    break
                elif cmd[0] == "list":
                    print("可用模型:", client.get_available_models())
                elif cmd[0] == "switch" and len(cmd) > 1:
                    client.set_model(cmd[1])
                continue

            # 生成响应
            response = client.generate_response(prompt)
            if response:
                print(f"\nBot: {response}\n")
    except KeyboardInterrupt:
        print("\n会话结束")


if __name__ == "__main__":
    main()
