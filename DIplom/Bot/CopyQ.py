# import sqlite3

# # Подключение к исходной базе данных
# source_conn = sqlite3.connect('questions.db')
# source_c = source_conn.cursor()

# # Подключение к целевой базе данных
# target_conn = sqlite3.connect('test_questions.db')
# target_c = target_conn.cursor()

# # Запрос на выборку данных из исходной таблицы
# source_c.execute("SELECT * FROM questions WHERE id BETWEEN 1215 AND 1890")

# # Получение всех строк
# rows = source_c.fetchall()

# # Обновление строк в целевой таблице
# for i, row in enumerate(rows, start=1252):
#     target_c.execute("UPDATE questions SET question = ? WHERE id = ?", (row[1], i))

# # Сохранение изменений
# target_conn.commit()

# # Закрытие соединения с базами данных
# source_conn.close()
# target_conn.close()

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('test_questions.db')
c = conn.cursor()

# Запрос на удаление строк
c.execute("DELETE FROM questions WHERE id > 2115")

# Сохранение изменений
conn.commit()

# Закрытие соединения с базой данных
conn.close()
