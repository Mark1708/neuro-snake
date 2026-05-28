# neuro-snake

> Лабораторное исследование по нейротехнологиям: EEG-подобный биосигнал с Arduino передается в игру Snake, более высокая активность увеличивает скорость игры, а по итогам сессии генерируется PDF-отчет с интерполяцией сигнала и FFT-анализом ритмов мозга.

![Python](https://img.shields.io/badge/runtime-python%203-111827?style=for-the-badge&labelColor=111827&color=5b5ef4)
![Arduino](https://img.shields.io/badge/hardware-arduino%20uno-111827?style=for-the-badge&labelColor=111827&color=5b5ef4)
![Status](https://img.shields.io/badge/status-finished%20demo-111827?style=for-the-badge&labelColor=111827&color=5b5ef4)

[English version](README.md)

| Поле | Значение |
|---|---|
| Статус | Завершенная учебная демонстрация |
| Тип | Игра с аппаратным вводом / эксперимент по обработке сигнала |
| Основной стек | Python 3, pygame, pySerial, pandas, NumPy, SciPy, Plotly, FPDF, Arduino Uno |
| Управление | Направление змейки с клавиатуры |
| Опциональный вход | Serial-поток Arduino с аналоговых пинов `A0` и `A1` |
| Runtime-выходы | Игра Snake; подключенные сессии могут сохранять CSV-сэмплы, графики и PDF-отчет |

## Цель

Проект был выполнен в рамках лабораторного исследования по нейротехнологиям. В нем изучались ключевые показатели активности мозга и применялись для динамической игровой симуляции Snake: более высокая измеренная активность увеличивает скорость игры.

Направление в игре по-прежнему задается с клавиатуры. Проект не реализует прямое управление мыслью и не делает медицинских или диагностических заявлений. Если Arduino подключена, Python-игра читает EEG-подобный биосигнал из последовательного порта, использует второе значение как отображаемое и текущее значение задержки движения, записывает это значение во время игры и генерирует PDF-отчет после завершения подключенной игровой сессии.

Итоговый отчет показывает показатели активности мозга за время игровой сессии. Он включает интерполяцию сигнала, преобразование Фурье, обратное преобразование Фурье и представление EEG-диапазонов Delta, Theta, Alpha, Beta и Gamma.

## Аппаратная часть

| Компонент | Подтверждение / ожидание |
|---|---|
| Плата | Arduino Uno или совместимая плата |
| Источник сигнала | Аналоговый EEG-подобный сенсор/источник, подключенный к Arduino |
| Аналоговые пины | `A0`, `A1` в `arduino-serial/eeg_reader/eeg_reader.ino` |
| Arduino-библиотека | `TimerOne` из `arduino-serial/lib/TimerOne.zip` |
| Serial-формат | Два значения через запятую, преобразованные из analog reads Arduino в диапазон `0..255` |
| Значение, используемое игрой | Python сейчас использует второе serial-значение (`A1`) для отображения скорости, задержки движения и сэмплов CSV/report |
| Скорость serial | `115200` baud |
| Порт по умолчанию | `/dev/cu.usbmodem1411301`, можно изменить на экране настроек Arduino |

Фотографии аппаратной части:

<img src="assets/photo1.jpg" width="300" alt="Neuro Snake hardware photo 1"> <img src="assets/photo2.jpg" width="300" alt="Neuro Snake hardware photo 2">

## Настройка ПО

Репозиторий не фиксирует и не документирует проверенную patch-версию Python. В `requirements.txt` закреплен `pygame==2.1.2`, поэтому для установки этой версии pygame может потребоваться более старая среда Python 3.

```sh
cd python-game
python -m pip install -r requirements.txt
python main.py
```

Для режима с Arduino:

1. Установите Arduino-библиотеку `TimerOne`.
2. Загрузите `arduino-serial/eeg_reader/eeg_reader.ino` на плату.
3. Подключите источник сигнала к аналоговым пинам `A0` и `A1`.
4. Запустите Python-игру и откройте экран настроек Arduino.
5. Укажите serial-порт и скорость (`115200` по умолчанию), затем подключитесь.

Игра может открываться без Arduino. В этом режиме `Listener.read_data()` возвращает hard-coded fallback value, но запись CSV и генерация отчета запускаются только когда игра находится в connected-состоянии.

## Структура репозитория

- `python-game/main.py` - entrypoint pygame-игры.
- `python-game/requirements.txt` - manifest Python-зависимостей.
- `python-game/snake_game/snake.py` - timing движения, значение speed display и запись данных в connected-сессиях.
- `python-game/service/com_listener.py` - pySerial-подключение и чтение serial-сэмплов.
- `python-game/service/data_service.py` - жизненный цикл записи CSV.
- `python-game/service/report_service.py` - interpolation, FFT, inverse FFT, графики и генерация PDF-отчета.
- `arduino-serial/eeg_reader/eeg_reader.ino` - Arduino sketch, который читает `A0`/`A1` и пишет serial samples.
- `arduino-serial/lib/TimerOne.zip` - архив Arduino-библиотеки TimerOne.
- `assets/` - README/demo-фото, GIF, изображения обработки сигнала и sample report.
- `python-game/assets/` - runtime-графика, шрифт, звук и assets визуализации отчета, используемые игрой.

## Демонстрация

![Demo](assets/demo.gif)

## Обработка сигнала и outputs

Подключенная игровая сессия записывает пары time/value и создает отчет после game over.

| Вход / выход | Путь | Примечания |
|---|---|---|
| Arduino sketch | `arduino-serial/eeg_reader/eeg_reader.ino` | Читает `A0`/`A1`, пишет serial-значения на `115200` baud каждые `3000` микросекунд |
| Runtime entrypoint | `python-game/main.py` | Запускайте из `python-game/`, чтобы относительные runtime asset paths разрешались корректно |
| Captured CSV | `python-game/resourcedata_<timestamp>.csv` | Фактический текущий путь в коде; `RESOURCE_PATH` конкатенируется без разделителя |
| Generated PDF | `python-game/resourcereport-<timestamp>.pdf` | Фактический текущий путь в коде; создается после завершения подключенной игровой сессии |
| Generated plots | `python-game/assets/visualization/interpolation.png`, `fourie.png`, `inverse_fourie.png` | Создаются/перезаписываются при генерации отчета |
| Sample PDF | `assets/report-05.05.2022-20.00.40.pdf` | Сохраненный пример output |
| README sample images | `assets/interpolation.png`, `assets/fourie.png`, `assets/inverse_fourie.png` | Статические изображения, используемые в этом README |

Пример отчета: [PDF](assets/report-05.05.2022-20.00.40.pdf)

![Interpolation plot](assets/interpolation.png)
![Fourier transform plot](assets/fourie.png)
![Inverse Fourier transform plot](assets/inverse_fourie.png)

## Возможности

- pygame Snake game engine.
- Управление направлением с клавиатуры.
- Опциональное Arduino serial-подключение через pySerial.
- Получение serial-сэмплов с аналоговых пинов Arduino.
- Значение задержки движения берется из второго serial channel, когда Arduino подключена.
- Interpolation и FFT-based frequency analysis для connected-сессий.
- Генерация PDF-отчета с графиками после game over в connected-сессии.

## Допущения и ограничения

- Это учебная демонстрация, а не медицинское или диагностическое устройство.
- В проекте нет wiring diagram или заново проверенных hardware setup notes.
- Качество сигнала зависит от расположения сенсора, wiring платы, шума и runtime environment.
- Направление остается keyboard-based; serial-значения влияют на movement timing/speed display и samples для отчета.
- Default serial port специфичен для macOS и должен быть изменен под конкретную машину.
- Запуск с железом не повторялся во время обновления README.
- Версии Python-зависимостей закреплены частично: `pygame` закреплен, остальные нет.
- Output paths содержат историческую особенность конкатенации пути: generated CSV/PDF сейчас получают префикс `resource`, а не помещаются внутрь директории `resource/`.


## Статус

Исследовательский/учебный проект. Результаты, зависимости, hardware assumptions и runtime notes описаны для воспроизводимости, но репозиторий не поддерживается как packaged product.
