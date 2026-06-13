import uvicorn


def main():
    """
    Entry point for running the Health Assistant chatbot.
    Usage: poetry run healthbot
    """
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
