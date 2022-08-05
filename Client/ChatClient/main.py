from tkinter import simpledialog
from rich.console import Console
from Chat_Client import ChatClient
from rich.prompt import Prompt, IntPrompt, Confirm
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":
    console = Console()
    console.rule("[bold blue] Chat Client")
    username = Prompt.ask("What is your username?")
    client = ChatClient(username)
    client.username = username
    console.rule("[bold blue] Server Information")
    client.server_ip_addr = Prompt.ask("What is the IP address of the server?")
    client.server_port = IntPrompt.ask("What is the port of the server?")
    conn = None
    while True:
        try:
            with console.status("Connecting to server, please wait", spinner='material', speed=0.5):
                conn = ChatClient.connect(client)
                break
        except OSError as e:
            console.rule("[bold red] Error")
            console.print_exception(width=0)
            user_retry = Confirm.ask(f"Do you want to retry?")
            if not user_retry:
                exit(1)
