from python_ai.main import main


def test_main(capsys) -> None:
    main()
    assert capsys.readouterr().out == "Hello from python-ai\n"
