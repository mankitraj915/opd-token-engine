import asyncio
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .engine import AllocationEngine
from .models import Slot, Priority

# Initialize Rich Console for "Hacker" UI
console = Console()

async def run_opd_simulation():
    engine = AllocationEngine()
    
    # 1. Setup
    console.print(Panel.fit("[bold cyan]OPD Simulation System v2.0 (Fairness Enabled)[/bold cyan]", border_style="blue"))
    doctors = ["Dr. Smith"]
    
    with console.status("[bold green]Initializing Doctor Schedules...[/bold green]"):
        for doc in doctors:
            # Create a slot with capacity 5
            slots = [Slot(slot_id="S1", start_time="09:00", end_time="10:00", max_capacity=5)]
            engine.add_doctor(doc, slots)
        await asyncio.sleep(1)

    # 2. Add Patients
    console.print("[yellow]➜ Booking Standard Patient 'Alice' (Standard)[/yellow]")
    engine.allocate_token("Dr. Smith", "S1", "Alice", Priority.ONLINE)
    
    console.print("[yellow]➜ Booking Standard Patient 'John' (Walk-in)[/yellow]")
    engine.allocate_token("Dr. Smith", "S1", "John", Priority.WALK_IN)

    # 3. Emergency Event (Pushes John to the back)
    console.print("[bold red]🚨 EMERGENCY ALERT: Patient 'Bob' Incoming![/bold red]")
    engine.allocate_token("Dr. Smith", "S1", "Bob", Priority.EMERGENCY)
    
    # 4. Another Priority Patient (Pushes John further back)
    console.print("[bold red]🚨 PAID PRIORITY: Patient 'Charlie' Incoming![/bold red]")
    engine.allocate_token("Dr. Smith", "S1", "Charlie", Priority.PAID_PRIORITY)

    # 5. Trigger Fairness Algorithm
    console.print("\n[bold magenta]--- Checking for Starvation ---[/bold magenta]")
    # John is now last. This function should detect that and upgrade him.
    engine.prevent_starvation("Dr. Smith", "S1")

    # 6. Render the Final Queue Table
    table = Table(title="Dr. Smith's Live Queue (Final State)")

    table.add_column("Pos", justify="right", style="cyan", no_wrap=True)
    table.add_column("Token ID", style="magenta")
    table.add_column("Patient Name", style="white")
    table.add_column("Priority", justify="center")
    
    # Fetch and display
    tokens = engine.doctor_schedules["Dr. Smith"][0].tokens
    for idx, t in enumerate(tokens, 1):
        # Color code the priority text
        p_color = "red" if t.priority == Priority.EMERGENCY else "blue"
        if t.patient_name == "John": p_color = "green" # Highlight our upgraded patient
        
        table.add_row(
            str(idx), 
            t.token_id, 
            t.patient_name, 
            f"[{p_color}]{t.priority.name}[/{p_color}]"
        )

    console.print("\n")
    console.print(table)
    console.print("\n[dim]Simulation Complete. Notice 'John' was upgraded from WALK_IN to PAID_PRIORITY.[/dim]")

if __name__ == "__main__":
    asyncio.run(run_opd_simulation())