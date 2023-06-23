import asyncio
import click
import hn.download
import hn.extract


@click.group()
def commands():
    pass


@click.command()
@click.argument("thread_id")
def download(thread_id):
    """Download comments for the given thread"""

    coroutine = hn.download.coroutine(thread_id)
    asyncio.run(coroutine)


@click.command()
@click.argument("thread_id")
def extract(thread_id):
    """Analyze downloaded comments for the given thread"""

    hn.extract.main(thread_id)


commands.add_command(download)
commands.add_command(extract)
