# neuro-snake

![Python](https://img.shields.io/badge/-Python-0a0a0a?style=for-the-badge&logo=Python)
![Arduino](https://img.shields.io/badge/-Arduino-0a0a0a?style=for-the-badge&logo=Arduino)

[Русская версия](README.ru.md)

## Summary

Classic Snake game controlled by brain activity. An educational project exploring BCI (Brain-Computer Interface) with Arduino and EEG hardware. Finished project.

## Hardware setup

Assemble the Arduino Uno + BitronicsLab EEG unit and upload the sketch from `arduino-serial/` (install the required library first).

Before | After
----- | ----
<img src="https://github.com/Mark1708/neuro-snake/raw/main/assets/photo1.jpg" width="300"> | <img src="https://github.com/Mark1708/neuro-snake/raw/main/assets/photo2.jpg" width="300">

## Stack

Python 3.9, pygame, Arduino Uno, BitronicsLab EEG, pySerial, numpy, scipy (signal processing)

## Local development

1. Assemble the Arduino + EEG hardware
2. Upload sketch from `arduino-serial/` (install required library first)
3. `pip install -r python-game/requirements.txt`
4. Run the game from `python-game/`
5. After playing, check the auto-generated PDF report

## Demo

![Demo](https://github.com/Mark1708/neuro-snake/raw/main/assets/demo.gif)

## Signal processing

The game captures raw EEG data and applies signal processing to translate brain activity into game controls. Example report: [PDF](https://github.com/Mark1708/neuro-snake/raw/main/assets/report-05.05.2022-20.00.40.pdf)

![](https://github.com/Mark1708/neuro-snake/raw/main/assets/interpolation.png)
![](https://github.com/Mark1708/neuro-snake/raw/main/assets/fourie.png)
![](https://github.com/Mark1708/neuro-snake/raw/main/assets/inverse_fourie.png)

## Features

- pygame game engine
- Arduino serial communication
- EEG data acquisition
- Real-time signal processing (FFT)
- Auto-generated PDF report

## Status

Finished educational project.

By [Mark Gurianov](https://mark1708.github.io/)
