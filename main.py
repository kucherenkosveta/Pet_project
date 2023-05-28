import numpy as np
from scipy.stats import ttest_ind, ttest_rel, ttest_1samp
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_file1 = tk.Button(self)
        self.select_file1["text"] = "Выберите файл для первой выборки"
        self.select_file1["command"] = self.browse_file1
        self.select_file1.pack(side="top")

        self.select_file2 = tk.Button(self)
        self.select_file2["text"] = "Выберите файл для второй выборки"
        self.select_file2["command"] = self.browse_file2
        self.select_file2.pack(side="top")

        self.select_test_type = tk.Label(self, text="Выберите критерий:")
        self.select_test_type.pack(side="top")

        self.test_type = tk.StringVar(value="one_sample")
        self.one_sample_ttest = tk.Radiobutton(self, text="Одновыборочный t-критерий",
                                               variable=self.test_type, value="one_sample")
        self.one_sample_ttest.pack(side="top")

        self.independent_ttest = tk.Radiobutton(self, text="Двухвыборочный t-критерий для независимых выборок",
                                                variable=self.test_type, value="independent")
        self.independent_ttest.pack(side="top")

        self.related_ttest = tk.Radiobutton(self, text="Двухвыборочный t-критерий для зависимых выборок",
                                            variable=self.test_type, value="related")
        self.related_ttest.pack(side="top")

        self.run_analysis = tk.Button(self)
        self.run_analysis["text"] = "Запустить анализ"
        self.run_analysis["command"] = self.analyze_data
        self.run_analysis.pack(side="top")

        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.pack(side="top")

        self.save_results_btn = tk.Button(self)
        self.save_results_btn["text"] = "Сохранить результаты"
        self.save_results_btn["command"] = self.save_results
        self.save_results_btn.pack(side="top")

    def browse_file1(self):
        filename = filedialog.askopenfilename()
        self.file1_path = filename

    def browse_file2(self):
        filename = filedialog.askopenfilename()
        self.file2_path = filename

    def analyze_data(self):
        try:
            sample1 = self.read_data(self.file1_path)
            sample2 = self.read_data(self.file2_path)

            if self.test_type.get() != "one_sample":
                assert len(sample1) == len(sample2), "Выборки должны иметь одинаковый размер"

            if self.test_type.get() == "one_sample":
                t_statistic, p_value = ttest_1samp(sample1, 0)

                # Вывод графика для одновыборочного теста
                plt.figure()
                plt.hist(sample1, bins='auto')
                plt.xlabel('Значения')
                plt.ylabel('Частота')
                plt.title('Гистограмма выборки')
                plt.show()

            elif self.test_type.get() == "independent":
                t_statistic, p_value = ttest_ind(sample1, sample2)

                # Вывод графиков для двухвыборочного теста для независимых выборок
                plt.figure()
                plt.hist(sample1, bins='auto', alpha=0.5, label='Выборка 1')
                plt.hist(sample2, bins='auto', alpha=0.5, label='Выборка 2')
                plt.xlabel('Значения')
                plt.ylabel('Частота')
                plt.title('Гистограмма выборок 1 и 2')
                plt.legend()
                plt.show()

            elif self.test_type.get() == "related":
                t_statistic, p_value = ttest_rel(sample1, sample2)

                # Вывод графиков для двухвыборочного теста для зависимых выборок
                plt.figure()
                plt.plot(sample1, label='Выборка 1')
                plt.plot(sample2, label='Выборка 2')
                plt.xlabel('Индекс')
                plt.ylabel('Значения')
                plt.title('Графики выборок 1 и 2')
                plt.legend()
                plt.show()

            self.result_text.delete("1.0", "end")
            self.result_text.insert("end", f"Значение t-статистики: {t_statistic}\n")
            self.result_text.insert("end", f"p-значение: {p_value}\n")

            if p_value < 0.05:
                self.result_text.insert("end", "Отвергаем нулевую гипотезу\n")
            else:
                self.result_text.insert("end", "Не отвергаем нулевую гипотезу\n")

            self.save_results_btn.pack(side="top")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def read_data(self, filename):
        data = np.loadtxt(filename)

        if data.ndim != 1:
            raise ValueError("Файл должен содержать одномерный массив данных")

        return data

    def save_results(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as file:
                file.write(self.result_text.get("1.0", "end"))
                messagebox.showinfo("Сохранение", "Результаты успешно сохранены.")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Критерий Стьюдента")
    app = Application(master=root)
    app.mainloop()
