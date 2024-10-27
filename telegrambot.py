import pandas as pd
import plotly.express as px
from plotly.io import write_image
import requests
import os

# Шаг 1: Прочитать данные из Excel-файла
excel_file = 'products_data.xlsx'
sheet_name = 'Sheet'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Определение переменных для горизонтальных линий
resolve_price = 100  # Пример значения
ma = 150  # Пример значения
mi = 50  # Пример значения

# Шаг 2: Создать график на основе данных
columns = df.columns.tolist()

fig = px.line(df, x=columns[0], y=columns[1])
fig.add_hline(y=resolve_price)
fig.add_hline(y=ma)
fig.add_hline(y=mi)

# Шаг 3: Сохранить график в виде изображения
image_path = "plot.png"
fig.write_image(os.path.join(__file__, image_path))


# Шаг 4: Отправить изображение через HTTP-запрос в Telegram
bot_token = '7079315172:AAERG6-cJw1PU2wWGlE9h_FamgFKEy74Dww'
chat_id = '5116329209'
url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

with open(image_path, 'rb') as photo:
    files = {'photo': photo}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)

# Удаление временного файла изображения
os.remove(image_path)

print(response.json())