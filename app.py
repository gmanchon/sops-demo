import click

@click.group()
def app():
    """Main application group"""
    pass

@app.group()
def instance():
    """Instance management commands"""
    pass

@instance.command()
def start():
    """Start the application instance"""
    click.echo("Starting application instance...")
    # Add a confirmation that the command was executed
    click.echo("Command executed successfully!")

if __name__ == '__main__':
    app()
