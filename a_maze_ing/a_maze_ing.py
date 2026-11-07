from parse import parser


def main() -> None:
    config = parser()
    print(config)


if __name__ == '__main__':
    main()
