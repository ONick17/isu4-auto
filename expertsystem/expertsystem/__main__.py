try:
    from .main import main
except ImportError:
    from expertsystem.main import main

if __name__ == '__main__':
    main()
