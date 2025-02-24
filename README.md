
# UnOll - Ollama 未授权工具

如果 Ollama 服务部署在开放网络（如公网）且未设置身份验证，攻击者可能通过其 API 直接访问模型，导致：

- 模型被恶意滥用（如生成有害内容）。
- 消耗本地计算资源（如 GPU/CPU）。
- 窃取敏感数据（若模型经过微调或包含业务信息）

## 主要功能 ✨

- 🚦 自动连接验证与服务检测
- 📋 实时列出可用模型
- 💬 交互式对话模式（支持命令操作）
- ⚡ 快速单次查询模式
- 🔄 动态切换对话模型
- 🌐 远程服务器连接支持

## 快速开始

### 基本使用
```bash
# 列出所有可用模型
python UnOll.py --list

# 单次查询（自动选择第一个可用模型）
python UnOll.py --prompt "你好"

# 指定远程服务器和模型
python UnOll.py --host http://10.0.0.1:11434 --model mistral

```

## 交互模式
```bash
$ python UnOll.py
Ollama 交互客户端 | 模型: llama2 | 服务端: http://localhost:11434
命令：
/list    - 列出所有模型
/switch  - 切换模型
/exit    - 退出

You: /list
可用模型: ['llama2', 'codellama', 'mistral']

You: /switch mistral
已切换到模型: mistral

You: 写一个Python递归函数示例
Bot: 以下是计算阶乘的递归实现...

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
```

## 参数说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--host` | 无 | Ollama 服务地址 | `--host http://remote:11434` |
| `--model` | `-m` | 指定使用的模型 | `-m codellama` |
| `--list` | `-l` | 列出可用模型 | `python UnOll.py -l` |
| `--prompt` | `-p` | 单次查询模式 | `-p "你好"` |


### Ollama 端口安全修复建议
```bash
# 1. 防火墙严格管控（Ubuntu示例）
sudo ufw allow from 192.168.1.0/24 to any port 11434
sudo ufw deny 11434

# 2. 服务绑定本地接口（修改Ollama启动参数）
OLLAMA_HOST=127.0.0.1 ollama serve

# 3. 修改默认端口（需要同步修改客户端）
export OLLAMA_HOST="http://localhost:11555"
ollama serve --address ":11555"

# 4. Docker安全配置
docker run -d \
  --name ollama-secure \
  -p 127.0.0.1:11434:11434 \  # 仅绑定本地
  --read-only \               # 只读文件系统
  --cap-drop=ALL \            # 删除所有权限
  ollama/ollama
```

## 法律与合规警告 ⚠️‼️

### 禁止使用此工具进行未授权测试
```diff
- 严禁在未获得明确书面授权的情况下：
- • 扫描公网暴露的Ollama服务
- • 访问非自有基础设施
- • 进行压力测试或漏洞利用

+ 合法使用示例：
+ ✓ 访问自己部署的本地服务
+ ✓ 测试已获书面授权的实验环境

