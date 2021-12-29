"""This file serves as the entry point of the backend."""

from sys import argv
import platform


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

    if platform.system() == "Windows":
        from waitress import serve
        serve(app,host="0.0.0.0", port=9678)
    elif platform.system() == "Linux" or platform.system() == "Darwin": # Maybe test with "Java" for the compatibilty of bjoern
        from bjoern import run

        run(app, "0.0.0.0", 9678)


if __name__ == '__main__':
    main()
