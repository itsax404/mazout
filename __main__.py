"""This file serves as the entry point of the backend."""

from sys import argv


def main() -> None:
    """The actual entry point."""

    print("""
    ###################
    #                 #
    #  mazout.studio  #
    #                 #
    ###################

    """)

    from MazoutServer.server import app

    if "dev" in argv and argv[1] == "dev":
        app.run(port=9678, host="127.0.0.1")
        return

    from bjoern import run

    run(app, "0.0.0.0", 9678)


if __name__ == '__main__':
    main()
