import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

app = typer.Typer()
console = Console()


def send_query_to_rag(query: str) -> str:
    """
    Send a query to the RAG system and return the answer.
    """
    payload = {"query": query}
    response = requests.post("http://localhost:8000/generate", json=payload)
    return response.json()["answer"]


@app.command()
def chat():
    """
    Enter an interactive chat session.
    """
    console.print(
        Panel.fit(
            "Chatbot Active. Type [bold red]'exit'[/bold red] to quit.",
            title="Fitness Assistant",
        )
    )

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")

        if user_input.lower() in ["exit", "quit", "bye"]:
            console.print(
                "[italic yellow]Goodbye! Have a productive day.[/italic yellow]"
            )
            break
        
        with console.status("[bold green]Assistant is thinking...", spinner="dots"):
            response = send_query_to_rag(user_input)

        console.print(f"[bold magenta]Assistant:[/bold magenta] {response}")


if __name__ == "__main__":
    app()
