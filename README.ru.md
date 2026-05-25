# neuro-snake

![Python](https://img.shields.io/badge/-Python-0a0a0a?style=for-the-badge&logo=Python)
![Arduino](https://img.shields.io/badge/-Arduino-0a0a0a?style=for-the-badge&logo=Arduino)

[English version](README.md)

## О проекте

Классическая игра "Змейка", управляемая активностью мозга. Образовательный проект, исследующий BCI (Brain-Computer Interface) с использованием Arduino и аппаратуры ЭЭГ. Завершённый проект.

## Сборка оборудования

Соберите стенд на базе Arduino Uno + BitronicsLab EEG и загрузите скетч из папки `arduino-serial/` (предварительно установите требуемую библиотеку).

До | После
----- | ----
<img src="https://github.com/Mark1708/neuro-snake/raw/main/assets/photo1.jpg" width="300"> | <img src="https://github.com/Mark1708/neuro-snake/raw/main/assets/photo2.jpg" width="300">

## Стек

Python 3.9, pygame, Arduino Uno, BitronicsLab EEG, pySerial, numpy, scipy (обработка сигналов)

## Локальная разработка

1. Соберите стенд Arduino + EEG
2. Загрузите скетч из `arduino-serial/` (предварительно установите требуемую библиотеку)
3. `pip install -r python-game/requirements.txt`
4. Запустите игру из папки `python-game/`
5. После игры проверьте автоматически сгенерированный PDF-отчёт

## Демонстрация

![Demo](https://github.com/Mark1708/neuro-snake/raw/main/assets/demo.gif)

## Обработка сигналов

Игра захватывает сырые данные ЭЭГ и применяет обработку сигналов для преобразования активности мозга в управляющие команды. Пример отчёта: [PDF](https://github.com/Mark1708/neuro-snake/raw/main/assets/report-05.05.2022-20.00.40.pdf)

![](https://github.com/Mark1708/neuro-snake/raw/main/assets/interpolation.png)
![](https://github.com/Mark1708/neuro-snake/raw/main/assets/fourie.png)
![](https://github.com/Mark1708/neuro-snake/raw/main/assets/inverse_fourie.png)

## Возможности

- Игровой движок на pygame
- Последовательная связь с Arduino
- Сбор данных ЭЭГ
- Обработка сигналов в реальном времени (БПФ)
- Автоматическая генерация PDF-отчёта

## Статус

Завершённый образовательный проект.

[Mark Gurianov](https://mark1708.github.io/)
