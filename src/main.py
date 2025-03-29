import os
import time
import json
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.syntax import Syntax
from requests.exceptions import RequestException
from time import sleep
from requests.auth import HTTPBasicAuth

console = Console()

class APITester:
    def __init__(self):
        self.base_url = ""
        self.auth = None
        self.headers = {}
        self.timeout = 10
        self.retry_count = 3
        self.retry_delay = 2
        self.log_file = "api_test_log.txt"
        self.cookies = {}
        self.cache = {}
        self.mock_responses = {}

    def set_base_url(self):
        self.base_url = Prompt.ask("Enter the base URL of the API", default="https://jsonplaceholder.typicode.com")

    def choose_method(self):
        methods = ["GET", "POST", "PUT", "DELETE"]
        method_choice = Prompt.ask(
            "[bold green]Choose the HTTP method[/bold green]",
            choices=methods,
            default="GET"
        )
        return method_choice

    def choose_auth(self):
        auth_choice = Prompt.ask(
            "[bold yellow]Does the API require authentication?[/bold yellow]", choices=["Yes", "No"], default="No"
        )
        if auth_choice == "Yes":
            auth_type = Prompt.ask("[bold cyan]Choose Authentication type[/bold cyan]", choices=["Basic", "Bearer", "OAuth2"])
            if auth_type == "Basic":
                username = Prompt.ask("[bold magenta]Enter your username[/bold magenta]")
                password = Prompt.ask("[bold magenta]Enter your password[/bold magenta]", password=True)
                self.auth = (username, password)
            elif auth_type == "Bearer":
                token = Prompt.ask("[bold magenta]Enter your Bearer token[/bold magenta]")
                self.headers["Authorization"] = f"Bearer {token}"
            elif auth_type == "OAuth2":
                client_id = Prompt.ask("[bold magenta]Enter OAuth client ID[/bold magenta]")
                client_secret = Prompt.ask("[bold magenta]Enter OAuth client secret[/bold magenta]", password=True)
                self.headers["Authorization"] = f"Bearer {client_id}:{client_secret}"

    def set_custom_headers(self):
        add_headers = Prompt.ask("[bold yellow]Would you like to add custom headers?[/bold yellow]", choices=["Yes", "No"], default="No")
        if add_headers == "Yes":
            while True:
                header_key = Prompt.ask("[bold cyan]Enter header key (or type :exit to stop)[/bold cyan]")
                if header_key == ":exit":
                    break
                header_value = Prompt.ask("[bold cyan]Enter header value[/bold cyan]")
                self.headers[header_key] = header_value

    def set_timeout(self):
        timeout = Prompt.ask("[bold magenta]Enter the timeout in seconds (default 10)", default="10")
        self.timeout = int(timeout) if timeout.isdigit() else 10

    def retry_request(self, method, url, data=None):
        retries = 0
        while retries < self.retry_count:
            try:
                if method == "GET":
                    return requests.get(url, headers=self.headers, auth=self.auth, timeout=self.timeout, cookies=self.cookies)
                elif method == "POST":
                    return requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=self.timeout, cookies=self.cookies)
                elif method == "PUT":
                    return requests.put(url, json=data, headers=self.headers, auth=self.auth, timeout=self.timeout, cookies=self.cookies)
                elif method == "DELETE":
                    return requests.delete(url, headers=self.headers, auth=self.auth, timeout=self.timeout, cookies=self.cookies)
            except RequestException as e:
                retries += 1
                if retries < self.retry_count:
                    console.print(f"[bold red]Error: {e}. Retrying...[/bold red]")
                    sleep(self.retry_delay)
                else:
                    console.print(f"[bold red]Error: {e}. No more retries.[/bold red]")
                    return None
        return None

    def handle_pagination(self, method, endpoint, data=None):
        page = 1
        while True:
            response = self.retry_request(method, f"{endpoint}?page={page}", data)
            if response and response.status_code == 200:
                self.show_response(response)
                if 'next' not in response.links:
                    break
                page += 1
            else:
                console.print("[bold red]No more pages or error occurred.[/bold red]")
                break

    def send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"

        if method == "GET" and url in self.cache:
            console.print(f"[bold yellow]Using cached response for {url}[/bold yellow]")
            self.show_response(self.cache[url])
            return

        if url in self.mock_responses:
            console.print(f"[bold yellow]Using mock response for {url}[/bold yellow]")
            self.show_response(self.mock_responses[url])
            return

        response = self.retry_request(method, url, data)
        if response:
            self.log_response(response)
            self.show_response(response)

            if method == "GET":
                self.cache[url] = response

    def show_response(self, response):
        status_text = f"Status Code: [bold green]{response.status_code}[/bold green]"
        console.print(Panel(status_text, style="bold blue"))

        try:
            if response.headers.get("Content-Type") == "application/json":
                json_data = response.json()
                syntax = Syntax(json.dumps(json_data, indent=4), "json", theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title="Response Body", style="bold cyan"))
            elif "text/html" in response.headers.get("Content-Type", ""):
                console.print(f"[bold yellow]HTML Response Body[/bold yellow]:\n{response.text}")
            elif "application/xml" in response.headers.get("Content-Type", ""):
                console.print(f"[bold yellow]XML Response Body[/bold yellow]:\n{response.text}")
            else:
                console.print(f"[bold yellow]Response Body:[/bold yellow]\n{response.text}")
        except ValueError:
            console.print("[bold yellow]Response Body is not in JSON format:[/bold yellow]")
            console.print(response.text)

    def log_response(self, response):
        with open(self.log_file, "a") as log:
            log.write(f"URL: {response.url}\n")
            log.write(f"Status Code: {response.status_code}\n")
            log.write(f"Response Headers: {json.dumps(response.headers, indent=4)}\n")
            log.write(f"Response Body: {response.text}\n")
            log.write("-" * 80 + "\n")

    def mock_api_response(self, endpoint, response_data, status_code=200, headers=None):
        self.mock_responses[endpoint] = requests.Response()
        self.mock_responses[endpoint].status_code = status_code
        self.mock_responses[endpoint]._content = json.dumps(response_data).encode('utf-8')
        self.mock_responses[endpoint].headers = headers or {"Content-Type": "application/json"}

    def scripting(self):
        language_choice = Prompt.ask("[bold green]Choose a language for the script[/bold green]", choices=["Python", "JavaScript"], default="Python")
        console.print("[bold cyan]Setting up a file for you 🎨🖌️[/bold cyan]")
        time.sleep(2)
        filename = Prompt.ask("[bold magenta]Enter the filename (with extension)[/bold magenta]")
        file_content = ""
        while True:
            line = Prompt.ask("[bold yellow]Write content for the script or type :exit to save[/bold yellow]")
            if line == ":exit":
                break
            file_content += line + "\n"

        with open(filename, "w") as file:
            file.write(file_content)

        console.print(f"[bold blue]File saved as {filename}[/bold blue]")
        self.execute_script(filename, language_choice)

    def execute_script(self, filename, language_choice):
        if language_choice == "Python":
            os.system(f"python3 {filename}")
        elif language_choice == "JavaScript":
            os.system(f"node {filename}")
        console.print("[bold green]Script executed successfully[/bold green]")

    def run(self):
        while True:
            console.print(Panel("[bold cyan]Welcome to the Advanced Terminal API Tester[/bold cyan]", style="bold green"))
            self.set_base_url()
            self.choose_auth()
            self.set_custom_headers()
            self.set_timeout()
            method = self.choose_method()
            endpoint = Prompt.ask("[bold yellow]Enter the endpoint[/bold yellow]", default="/posts")
            data = None
            if method in ["POST", "PUT"]:
                data_input = Prompt.ask("[bold magenta]Enter the request body as JSON[/bold magenta]", default="{}")
                try:
                    data = json.loads(data_input)
                except json.JSONDecodeError:
                    console.print("[bold red]Invalid JSON. Please try again.[/bold red]")
                    continue

            if method == "GET":
                pagination = Prompt.ask("[bold cyan]Does the API have pagination?[/bold cyan]", choices=["Yes", "No"], default="No")
                if pagination == "Yes":
                    self.handle_pagination(method, endpoint, data)
                else:
                    self.send_request(method, endpoint, data)
            else:
                self.send_request(method, endpoint, data)

            test_script = Prompt.ask("[bold yellow]Do you want to test with scripting?[/bold yellow]", choices=["Yes", "No"], default="No")
            if test_script == "Yes":
                self.scripting()

            another_request = Prompt.ask("[bold green]Do you want to make another request?[/bold green]", choices=["Yes", "No"], default="No")
            if another_request == "No":
                console.print("[bold green]Goodbye![/bold green]")
                break

if __name__ == "__main__":
    tester = APITester()
    tester.run()
