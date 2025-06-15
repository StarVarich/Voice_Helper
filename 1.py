text = "Привет, Никита!\n"

# Без with — нужно вручную закрывать:
file = open("log.txt", "w")
file.write(text)
file.close()  # Если забудешь — файл может остаться "занятым"

# С with — всё закроется само:
with open("log.txt", "w") as f:
    f.write(text)
# Здесь файл уже закрыт

