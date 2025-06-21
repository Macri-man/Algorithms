import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class FourierTransformAnimator:
    def __init__(self, duration=1, sample_rate=500, freq_range=(0, 50), magnitude_threshold=1e-2):
        self.duration = duration
        self.sample_rate = sample_rate
        self.freq_range = freq_range
        self.magnitude_threshold = magnitude_threshold
        self.t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

        self.fig, (self.ax_time, self.ax_freq, self.ax_phase) = plt.subplots(3, 1, figsize=(8, 8))
        self.line_time, = self.ax_time.plot([], [], lw=2)
        self.line_freq, = self.ax_freq.plot([], [], lw=2)
        self.line_phase, = self.ax_phase.plot([], [], lw=2)

        self._setup_axes()

    def _setup_axes(self):
        self.ax_time.set_xlim(0, self.duration)
        self.ax_time.set_ylim(-2, 2)
        self.ax_time.set_title("Time Domain Signal")

        self.ax_freq.set_xlim(*self.freq_range)
        self.ax_freq.set_ylim(0, 1)
        self.ax_freq.set_title("Frequency Domain (Magnitude Spectrum)")

        self.ax_phase.set_xlim(*self.freq_range)
        self.ax_phase.set_ylim(-np.pi, np.pi)
        self.ax_phase.set_title("Frequency Domain (Phase Spectrum)")
        self.ax_phase.set_yticks([-np.pi, 0, np.pi])
        self.ax_phase.set_yticklabels(["-π", "0", "π"])

        plt.tight_layout()

    def signal(self, t, frame):
        f1 = 5
        f2 = 5 + frame * 0.2
        return np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

    def animate(self, frame):
        y = self.signal(self.t, frame)
        self.line_time.set_data(self.t, y)

        Y = np.fft.fft(y)
        freqs = np.fft.fftfreq(len(self.t), 1 / self.sample_rate)
        idx = np.where(freqs >= 0)

        freqs_pos = freqs[idx]
        Y_mag = np.abs(Y[idx])
        Y_phase = np.angle(Y[idx])

        # Mask out phase where magnitude is below threshold
        Y_phase_filtered = np.where(Y_mag > self.magnitude_threshold, Y_phase, np.nan)

        self.line_freq.set_data(freqs_pos, Y_mag)
        self.line_phase.set_data(freqs_pos, Y_phase_filtered)

        self.ax_freq.set_ylim(0, np.max(Y_mag) * 1.1 + 1e-3)

        return self.line_time, self.line_freq, self.line_phase

    def run(self, frames=100, interval=100):
        self.ani = animation.FuncAnimation(
            self.fig,
            self.animate,
            frames=frames,
            interval=interval,
            blit=True
        )
        plt.show()

# Example usage
if __name__ == "__main__":
    animator = FourierTransformAnimator()
    animator.run()
