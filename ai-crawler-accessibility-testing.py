import requests
import time

def simulate_crawler(target_url):
    """
    模拟爬虫，测试不同 User-Agent 的访问情况。

    Args:
        target_url (str): 目标网址。
    """
    # 1. 读取 User-Agent 列表
    user_agent_url = "https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt"
    try:
        response = requests.get(user_agent_url)
        response.raise_for_status()  # 检查 HTTP 状态码
        user_agents = [line.split(": ")[1].strip() for line in response.text.splitlines() if line.startswith("User-agent: ")]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user-agents: {e}")
        return

    # 2. 列出待测试的 User-Agent
    print("待测试的 User-Agent:")
    for ua in user_agents:
        print(ua)

    # 3. 使用每个 User-Agent 发送请求
    rejected_user_agents = []
    print("\n测试结果:")
    for ua in user_agents:
        headers = {"User-Agent": ua}
        try:
            response = requests.get(target_url, headers=headers)
            print(f"User-Agent: {ua}, HTTP 状态码: {response.status_code}")
            if response.status_code >= 400:
                rejected_user_agents.append(ua)
        except requests.exceptions.RequestException as e:
            print(f"User-Agent: {ua}, 访问出错: {e}")
            rejected_user_agents.append(ua) # 如果请求出现错误， 也加到拒绝列表中。

        time.sleep(1)  # 每次访问间隔 1 秒

    # 4. 列出被拒绝访问的 User-Agent
    print("\n被拒绝访问的 User-Agent:")
    if rejected_user_agents:
        for ua in rejected_user_agents:
            print(ua)
    else:
        print("所有 User-Agent 均可正常访问。")

# 测试
target_url = "https://www.hikvision.com/en/"
simulate_crawler(target_url)


#备注
"""
策划：JerryZhi
作者：Gemini Advanced 2.0 Flash 
"""
