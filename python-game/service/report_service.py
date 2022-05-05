import pandas as pd
import numpy as np
from fpdf import FPDF
from scipy import interpolate
from scipy.fft import rfft, fftfreq, irfft
from statistics import mean
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from config import RESOURCE_PATH


class ReportService:
    def __init__(self, data_service, score):
        self.data_service = data_service
        self.bounds = [
            {'start': 0.5, 'end': 4, 'name': 'Delta', 'color': 'Turquoise'},
            {'start': 4, 'end': 8, 'name': 'Theta', 'color': 'PaleTurquoise'},
            {'start': 8, 'end': 13, 'name': 'Alpha', 'color': 'Turquoise'},
            {'start': 13, 'end': 25, 'name': 'Beta-1', 'color': 'PaleTurquoise'},  # Low Frequency Beta (beta-1)
            {'start': 25, 'end': 30, 'name': 'Beta-2', 'color': 'Turquoise'},  # High Frequency Beta (beta-2)
            {'start': 30, 'end': 70, 'name': 'Gamma', 'color': 'PaleTurquoise'}
        ]
        self.SAMPLING_FREQUENCY = self.bounds[-1]['end'] * 2  # Гц по условию теоремы Котельникова

        self.score = score
        self.average_speed = 0

    def read_and_fix_data(self):
        df = pd.read_csv(self.data_service.name, sep=',', names=['Time', 'Signal']).astype('float64')
        df = df.drop_duplicates(keep='last', subset=['Time'], ignore_index=True)
        df['Time'] -= df['Time'].min()
        df = df.sort_values(by="Time")
        self.average_speed = df['Signal'].mean()
        return df

    def interpolation(self, df):
        DURATION = df['Time'].max()
        N = int(self.SAMPLING_FREQUENCY * DURATION)
        time = np.linspace(0, DURATION, N)

        signal = interpolate.interp1d(df['Time'].to_numpy(), df['Signal'].to_numpy(), kind='cubic')(time)
        return {
            'time': time,
            'signal': signal,
            'N': N
        }

    def fourie(self, data):
        N = data['N']
        yf = rfft(data['signal'])[1:N // 2]
        xf = fftfreq(N, 1 / self.SAMPLING_FREQUENCY)[1:N // 2]
        # Фильтрация сигнала от электрического шума (шум в диапазоне 50 Гц)
        for i in range(len(yf)):
            if 49.8 < xf[i] < 50.2:
                yf[i] = 0
        return {
            'x': xf,
            'y': yf
        }

    def inverse_fourie(self, y):
        inv = irfft(y)
        x = np.linspace(0, len(inv), len(inv))
        return {
            'x': x,
            'y': inv
        }

    def make_segment(self, x, y, start, end):
        return [(y[i] if (x[i] >= start) & (x[i] <= end) else 0) for i in range(len(x))]

    def draw_interp(self, signal, interp_data, title, scatter1, scatter2, LIMIT=200):
        fig = make_subplots(
            rows=1, cols=1
        )
        old = signal[signal['Time'] <= LIMIT]
        interp = pd.DataFrame({'time': interp_data['time'], 'signal': interp_data['signal']})
        interp = interp[interp['time'] <= old['Time'].max()]

        old_data = go.Scatter(
            x=old['Time'], y=old['Signal'], name=scatter1.format(str(signal.shape[0])), mode='markers',
            marker=dict(size=6)
        )

        interp_values = go.Scatter(
            x=interp['time'], y=interp['signal'], name=scatter2.format(str(len(interp_data['time'])))
        )
        fig.add_trace(
            old_data, row=1, col=1
        )
        fig.add_trace(
            interp_values, row=1, col=1
        )
        fig.update_layout(legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,

        ))

        fig.update_xaxes(range=[0, LIMIT])

        fig.update_layout(title_text=title, height=300, showlegend=True)
        fig.write_image('assets/visualization/interpolation.png')

    def draw_fourie(self, furie, title):
        fig = make_subplots(
            rows=1, cols=1
        )

        # Список зоны для каждого графика
        shapes = []
        # Название зон
        text_trace = go.Scatter(
            x=[wave['start'] + (wave['end'] - wave['start']) / 2 for wave in self.bounds],
            y=[0.075] * len(self.bounds),
            text=[wave['name'] for wave in self.bounds],
            mode="text",
        )

        # Преобразуем комплексные числа
        df = pd.DataFrame({'x': furie['x'], 'y': 2 / len(furie['x']) * np.abs(furie['y'])})
        fig.add_trace(
            go.Scatter(
                x=df.x, y=df.y, name="EEG", line=dict(width=1)
            ), row=1, col=1
        )
        fig.add_trace(
            text_trace, row=1, col=1
        )
        fig.update_xaxes(range=[self.bounds[0]['start'], self.bounds[-1]['end']], row=1, col=1)
        fig.update_yaxes(range=[0, 0.1], row=1, col=1)
        # Создаём зоны
        for k in range(len(self.bounds)):
            shapes.append(
                dict(
                    type="rect",
                    y0=0, y1=0.1,
                    x0=self.bounds[k]['start'], x1=self.bounds[k]['end'],
                    xref="x" + str(1), yref="y" + str(1),
                    fillcolor=self.bounds[k]['color'], opacity=0.4, line_width=0, layer="below"
                )
            )

        fig.update_layout(title_text=title, height=300, shapes=shapes, showlegend=False)
        fig.write_image('assets/visualization/fourie.png')

    def draw_inverse_fourie(self, interp, fourie, title):
        m = mean(interp['signal'])

        fig = make_subplots(
            rows=len(self.bounds) + 1, cols=1, subplot_titles=(['All data'] + [wave['name'] for wave in self.bounds])
        )

        interp_df = pd.DataFrame(
            {'x': np.linspace(0, len(interp['signal']), len(interp['signal'])), 'y': interp['signal'] - m})
        fig.add_trace(
            go.Scatter(
                x=interp_df['x'], y=interp_df['y'], name="EEG", line=dict(width=1)
            ), row=1, col=1
        )
        fig.update_yaxes(range=[-2, 2], row=1, col=1)

        row = 1
        for wave in self.bounds:
            row += 1
            segment = self.make_segment(fourie['x'], fourie['y'], wave['start'], wave['end'])
            inverse_fourie_df = pd.DataFrame(self.inverse_fourie(segment))
            fig.add_trace(
                go.Scatter(
                    x=inverse_fourie_df['x'], y=inverse_fourie_df['y'], name="EEG", line=dict(width=1)
                ), row=row, col=1
            )
            fig.update_yaxes(range=[-1, 1], row=row, col=1)

        fig.update_layout(title_text=title, height=1000, showlegend=False)
        fig.write_image('assets/visualization/inverse_fourie.png')

    def create_title(self, time, pdf):
        pdf.set_font('Arial', '', 24)
        pdf.ln(60)
        pdf.write(5, f"EEG Game Report")
        pdf.ln(10)
        pdf.set_font('Arial', '', 16)
        pdf.write(4, f'{time}')
        pdf.ln(10)
        pdf.write(4, f'Score: {self.score} \tAverage speed: {round(self.average_speed, 3)}')
        pdf.ln(5)

    def create_analytics_report(self, filename="report.pdf"):
        pdf = FPDF()  # A4 (210 by 297 mm)
        time = self.data_service.time

        ''' First Page '''
        pdf.add_page()
        pdf.image("assets/visualization/header.png", 0, 0, 210)
        self.create_title(
            f'{time.strftime("%d.%m.%Y-%H:%M:%S")} - {self.data_service.last_time.strftime("%d.%m.%Y-%H:%M:%S")}',
            pdf
        )

        pdf.image("assets/visualization/interpolation.png", 5, 100, 200)
        pdf.image("assets/visualization/fourie.png", 5, 190, 200)

        ''' Second Page '''
        pdf.add_page()
        pdf.image("assets/visualization/inverse_fourie.png", 5, 5, 200)
        pdf.output(filename, 'F')

    def run_process(self):

        '''Get Data'''
        signal = self.read_and_fix_data()
        interp_data = self.interpolation(signal)
        fourie = self.fourie(interp_data)

        '''Draw Graphic'''
        self.draw_interp(signal, interp_data, 'Interpolation data', 'Primary data: {} values',
                         'Interpolation data: {} values', LIMIT=5)
        self.draw_fourie(fourie, 'Fourier transform')
        self.draw_inverse_fourie(interp_data, fourie, 'Inverse Fourier transform')

        self.create_analytics_report(filename=f'{RESOURCE_PATH}report-{self.data_service.time.strftime("%d.%m.%Y-%H.%M.%S")}.pdf')
