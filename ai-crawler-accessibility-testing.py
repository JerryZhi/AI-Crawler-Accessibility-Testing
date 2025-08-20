import requests
import time
import sys
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

def simulate_crawler(target_url, proxy, max_workers=10):
    """
    模拟爬虫，测试不同 User-Agent 的访问情况，支持代理和多线程并发。

    Args:
        target_url (str): 目标网址。
        proxy (dict): 代理设置（例如：{"http": "http://localhost:7897", "https": "http://localhost:7897"}）。
        max_workers (int): 最大并发线程数，默认为10。
    """
    # 1. 读取 User-Agent 列表
    user_agent_url = "https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt"
    try:
        response = requests.get(user_agent_url, proxies=proxy)
        response.raise_for_status()  # 检查 HTTP 状态码
        user_agents = [line.split(": ")[1].strip() for line in response.text.splitlines() if line.startswith("User-agent: ")]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user-agents: {e}")
        return

    # 2. 列出待测试的 User-Agent
    print(f"待测试的 User-Agent ({len(user_agents)} 个):")
    for i, ua in enumerate(user_agents, 1):
        print(f"{i:2d}. {ua}")

    print(f"\n开始并发测试 (并发数: {max_workers})...")
    print("-" * 50)

    # 3. 使用线程池并发测试
    rejected_user_agents = []
    results = []
    lock = threading.Lock()  # 用于线程安全的列表操作

    def test_user_agent(ua):
        """测试单个User-Agent的函数"""
        headers = {"User-Agent": ua}
        try:
            response = requests.get(target_url, headers=headers, proxies=proxy, timeout=10)
            status_code = response.status_code
            result = f"User-Agent: {ua[:50]}{'...' if len(ua) > 50 else ''}, HTTP 状态码: {status_code}"
            
            with lock:
                results.append((ua, status_code, None))
                if status_code >= 400:
                    rejected_user_agents.append(ua)
            
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"User-Agent: {ua[:50]}{'...' if len(ua) > 50 else ''}, 访问出错: {str(e)[:100]}"
            
            with lock:
                results.append((ua, None, str(e)))
                rejected_user_agents.append(ua)
            
            return error_msg

    # 使用ThreadPoolExecutor进行并发测试
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_ua = {executor.submit(test_user_agent, ua): ua for ua in user_agents}
        
        # 收集结果并实时显示进度
        completed = 0
        for future in as_completed(future_to_ua):
            try:
                result = future.result()
                completed += 1
                print(f"[{completed:3d}/{len(user_agents)}] {result}")
            except Exception as exc:
                ua = future_to_ua[future]
                completed += 1
                print(f"[{completed:3d}/{len(user_agents)}] User-Agent: {ua}, 发生异常: {exc}")

    # 4. 统计和显示结果
    print("\n" + "=" * 60)
    print("测试完成！统计结果:")
    print(f"总测试数量: {len(user_agents)}")
    print(f"正常访问: {len(user_agents) - len(rejected_user_agents)}")
    print(f"被拒绝/出错: {len(rejected_user_agents)}")
    
    # 5. 列出被拒绝访问的 User-Agent
    print("\n被拒绝访问或出错的 User-Agent:")
    if rejected_user_agents:
        for i, ua in enumerate(rejected_user_agents, 1):
            print(f"{i:2d}. {ua}")
    else:
        print("所有 User-Agent 均可正常访问。")

    # 6. 按状态码分类显示（可选，用于详细分析）
    if input("\n是否显示详细的状态码分析？(y/N): ").lower() == 'y':
        status_codes = {}
        errors = []
        
        for ua, status_code, error in results:
            if error:
                errors.append((ua, error))
            else:
                if status_code not in status_codes:
                    status_codes[status_code] = []
                status_codes[status_code].append(ua)
        
        print("\n按状态码分类:")
        for code in sorted(status_codes.keys()):
            print(f"\nHTTP {code} ({len(status_codes[code])} 个):")
            for ua in status_codes[code][:5]:  # 只显示前5个
                print(f"  - {ua}")
            if len(status_codes[code]) > 5:
                print(f"  ... 还有 {len(status_codes[code]) - 5} 个")
        
        if errors:
            print(f"\n网络错误 ({len(errors)} 个):")
            for ua, error in errors[:5]:  # 只显示前5个
                print(f"  - {ua}: {error[:100]}")
            if len(errors) > 5:
                print(f"  ... 还有 {len(errors) - 5} 个")

def get_system_proxy():
    """
    获取系统代理设置
    """
    try:
        proxy_handler = urllib.request.getproxies()
        if proxy_handler:
            return proxy_handler
        else:
            return None
    except:
        return None

def get_user_input():
    """
    交互式获取用户输入的目标URL和代理设置
    """
    print("AI爬虫可访问性测试工具")
    print("=" * 40)
    
    # 获取目标URL
    while True:
        target_url = input("请输入要测试的目标域名或URL: ").strip()
        if target_url:
            # 如果用户只输入了域名，自动添加http://协议
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            break
        else:
            print("URL不能为空，请重新输入。")
    
    # 获取代理设置
    print("\n代理设置选项:")
    print("1. 不使用代理")
    print("2. 使用系统代理")
    print("3. 自定义代理")
    
    while True:
        choice = input("请选择代理选项 (1-3，默认为2): ").strip()
        if not choice:
            choice = "2"
        
        if choice == "1":
            proxy = None
            print("已选择：不使用代理")
            break
        elif choice == "2":
            system_proxy = get_system_proxy()
            if system_proxy:
                proxy = system_proxy
                print(f"已选择：使用系统代理 {system_proxy}")
            else:
                proxy = None
                print("未检测到系统代理，将不使用代理")
            break
        elif choice == "3":
            proxy_port = input("请输入本地代理端口 (默认7897): ").strip()
            if not proxy_port:
                proxy_port = "7897"
            
            try:
                int(proxy_port)  # 验证端口号是否为数字
                proxy = {
                    "http": f"http://localhost:{proxy_port}", 
                    "https": f"http://localhost:{proxy_port}"
                }
                print(f"已选择：使用本地代理 localhost:{proxy_port}")
                break
            except ValueError:
                print("端口号必须是数字，请重新输入。")
        else:
            print("无效选择，请输入1、2或3。")
    
    # 获取并发数设置
    while True:
        concurrent_input = input("\n请输入并发线程数 (1-50，默认10): ").strip()
        if not concurrent_input:
            max_workers = 10
            break
        try:
            max_workers = int(concurrent_input)
            if 1 <= max_workers <= 50:
                break
            else:
                print("并发数必须在1-50之间，请重新输入。")
        except ValueError:
            print("并发数必须是数字，请重新输入。")
    
    print(f"已设置并发数: {max_workers}")
    
    return target_url, proxy, max_workers

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 没有命令行参数，使用交互式输入
        target_url, proxy, max_workers = get_user_input()
    elif len(sys.argv) == 2:
        # 有一个参数，使用命令行参数
        target_url = sys.argv[1]
        proxy = {"http": "http://localhost:7897", "https": "http://localhost:7897"}  # 默认代理
        max_workers = 10  # 默认并发数
    else:
        print("Usage: python ai-crawler-accessibility-testing.py [target_url]")
        print("如果不提供参数，将进入交互式模式")
        sys.exit(1)

    print(f"\n开始测试目标: {target_url}")
    if proxy:
        print(f"使用代理: {proxy}")
    else:
        print("不使用代理")
    print(f"并发线程数: {max_workers}")
    print("-" * 50)
    
    simulate_crawler(target_url, proxy, max_workers)


#备注
"""
策划：JerryZhi
作者：Gemini Advanced 2.0 Flash & Copilot@Claude Sonnet 4
"""
