import code

from tests.utils.fakers import StoryFactory


def interactive_shell():
    """Starts an interactive shell with pre-imported modules."""

    story_factory = StoryFactory()

    banner = "FastAPI Interactive Shell"
    variables = globals().copy()
    variables.update(locals())  # Ensure preloaded imports are available

    code.interact(banner=banner, local=variables)


if __name__ == "__main__":
    interactive_shell()
