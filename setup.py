from funpypi import setup


setup(
    name="funpypi",
    entry_points={
        "console_scripts": [
            "funpypi = funpypi.script:funpypi",
        ]
    },
)
