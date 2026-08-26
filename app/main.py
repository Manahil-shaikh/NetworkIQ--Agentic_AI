from networkiq.config import APP_NAME, ENVIRONMENT


def main() -> None:
    print(f"{APP_NAME} starting...")
    print(f"Environment: {ENVIRONMENT}")


if __name__ == "__main__":
    main()