import requests
import time
import sys
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

def simulate_crawler(target_url, proxy, max_workers=10):
    """
    Simulate crawler to test access with different User-Agents, supporting proxy and multi-threading.

    Args:
        target_url (str): Target URL.
        proxy (dict): Proxy settings (e.g., {"http": "http://localhost:7897", "https": "http://localhost:7897"}).
        max_workers (int): Maximum concurrent threads, default is 10.
    """
    # 1. Read User-Agent list
    user_agent_url = "https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/refs/heads/main/robots.txt"
    try:
        response = requests.get(user_agent_url, proxies=proxy)
        response.raise_for_status()  # Check HTTP status code
        user_agents = [line.split(": ")[1].strip() for line in response.text.splitlines() if line.startswith("User-agent: ")]
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving user-agents: {e}")
        return

    # 2. List User-Agents to be tested
    print(f"User-Agents to test ({len(user_agents)} total):")
    for i, ua in enumerate(user_agents, 1):
        print(f"{i:2d}. {ua}")

    print(f"\nStarting concurrent testing (concurrency: {max_workers})...")
    print("-" * 50)

    # 3. Use thread pool for concurrent testing
    rejected_user_agents = []
    results = []
    lock = threading.Lock()  # For thread-safe list operations

    def test_user_agent(ua):
        """Function to test a single User-Agent"""
        headers = {"User-Agent": ua}
        try:
            response = requests.get(target_url, headers=headers, proxies=proxy, timeout=10)
            status_code = response.status_code
            result = f"User-Agent: {ua[:50]}{'...' if len(ua) > 50 else ''}, HTTP Status: {status_code}"
            
            with lock:
                results.append((ua, status_code, None))
                if status_code >= 400:
                    rejected_user_agents.append(ua)
            
            return result
        except requests.exceptions.RequestException as e:
            error_msg = f"User-Agent: {ua[:50]}{'...' if len(ua) > 50 else ''}, Access Error: {str(e)[:100]}"
            
            with lock:
                results.append((ua, None, str(e)))
                rejected_user_agents.append(ua)
            
            return error_msg

    # Use ThreadPoolExecutor for concurrent testing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_ua = {executor.submit(test_user_agent, ua): ua for ua in user_agents}
        
        # Collect results and show real-time progress
        completed = 0
        for future in as_completed(future_to_ua):
            try:
                result = future.result()
                completed += 1
                print(f"[{completed:3d}/{len(user_agents)}] {result}")
            except Exception as exc:
                ua = future_to_ua[future]
                completed += 1
                print(f"[{completed:3d}/{len(user_agents)}] User-Agent: {ua}, Exception occurred: {exc}")

    # 4. Statistics and display results
    print("\n" + "=" * 60)
    print("Testing completed! Summary:")
    print(f"Total tests: {len(user_agents)}")
    print(f"Successful access: {len(user_agents) - len(rejected_user_agents)}")
    print(f"Rejected/Error: {len(rejected_user_agents)}")
    
    # 5. List rejected or errored User-Agents
    print("\nRejected or errored User-Agents:")
    if rejected_user_agents:
        for i, ua in enumerate(rejected_user_agents, 1):
            print(f"{i:2d}. {ua}")
    else:
        print("All User-Agents can access normally.")

    # 6. Show detailed status code analysis (optional)
    if input("\nShow detailed status code analysis? (y/N): ").lower() == 'y':
        status_codes = {}
        errors = []
        
        for ua, status_code, error in results:
            if error:
                errors.append((ua, error))
            else:
                if status_code not in status_codes:
                    status_codes[status_code] = []
                status_codes[status_code].append(ua)
        
        print("\nGrouped by status code:")
        for code in sorted(status_codes.keys()):
            print(f"\nHTTP {code} ({len(status_codes[code])} items):")
            for ua in status_codes[code][:5]:  # Show only first 5
                print(f"  - {ua}")
            if len(status_codes[code]) > 5:
                print(f"  ... and {len(status_codes[code]) - 5} more")
        
        if errors:
            print(f"\nNetwork errors ({len(errors)} items):")
            for ua, error in errors[:5]:  # Show only first 5
                print(f"  - {ua}: {error[:100]}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more")

def get_system_proxy():
    """
    Get system proxy settings
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
    Interactive input for target URL and proxy settings
    """
    print("AI Crawler Accessibility Testing Tool")
    print("=" * 40)
    
    # Get target URL
    while True:
        target_url = input("Please enter the target domain or URL to test: ").strip()
        if target_url:
            # If user only entered domain name, automatically add http:// protocol
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            break
        else:
            print("URL cannot be empty, please enter again.")
    
    # Get proxy settings
    print("\nProxy options:")
    print("1. No proxy")
    print("2. Use system proxy")
    print("3. Custom proxy")
    
    while True:
        choice = input("Please choose proxy option (1-3, default is 2): ").strip()
        if not choice:
            choice = "2"
        
        if choice == "1":
            proxy = None
            print("Selected: No proxy")
            break
        elif choice == "2":
            system_proxy = get_system_proxy()
            if system_proxy:
                proxy = system_proxy
                print(f"Selected: Use system proxy {system_proxy}")
            else:
                proxy = None
                print("No system proxy detected, will not use proxy")
            break
        elif choice == "3":
            proxy_port = input("Please enter local proxy port (default 7897): ").strip()
            if not proxy_port:
                proxy_port = "7897"
            
            try:
                int(proxy_port)  # Validate port number is numeric
                proxy = {
                    "http": f"http://localhost:{proxy_port}", 
                    "https": f"http://localhost:{proxy_port}"
                }
                print(f"Selected: Use local proxy localhost:{proxy_port}")
                break
            except ValueError:
                print("Port number must be numeric, please enter again.")
        else:
            print("Invalid choice, please enter 1, 2, or 3.")
    
    # Get concurrency settings
    while True:
        concurrent_input = input("\nPlease enter number of concurrent threads (1-50, default 10): ").strip()
        if not concurrent_input:
            max_workers = 10
            break
        try:
            max_workers = int(concurrent_input)
            if 1 <= max_workers <= 50:
                break
            else:
                print("Concurrency must be between 1-50, please enter again.")
        except ValueError:
            print("Concurrency must be numeric, please enter again.")
    
    print(f"Concurrency set to: {max_workers}")
    
    return target_url, proxy, max_workers

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No command line arguments, use interactive input
        target_url, proxy, max_workers = get_user_input()
    elif len(sys.argv) == 2:
        # One argument, use command line parameter
        target_url = sys.argv[1]
        proxy = {"http": "http://localhost:7897", "https": "http://localhost:7897"}  # Default proxy
        max_workers = 10  # Default concurrency
    else:
        print("Usage: python ai-crawler-detector-en.py [target_url]")
        print("If no parameters provided, interactive mode will start")
        sys.exit(1)

    print(f"\nStarting test on target: {target_url}")
    if proxy:
        print(f"Using proxy: {proxy}")
    else:
        print("Not using proxy")
    print(f"Concurrent threads: {max_workers}")
    print("-" * 50)
    
    simulate_crawler(target_url, proxy, max_workers)


# Notes
"""
Planner: JerryZhi
Author: Gemini Advanced 2.0 Flash & Copilot@Claude Sonnet 4
"""