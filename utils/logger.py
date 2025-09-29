def log_result(text):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
