import platform


def get_os_version():
    """Gets the OS version."""
    return platform.platform()


def main():
    print("Hello from tcc-webapp!")
    os_version = get_os_version()
    print(f"Running on: {os_version}")


if __name__ == "__main__":
    main()
