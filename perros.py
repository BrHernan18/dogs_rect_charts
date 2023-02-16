import pandas as pd
import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def handleSelectFileButton():
    try:
        filepath = getExcelFile()
        analizeFileAndShowCharts(filepath=filepath)

    except Exception as e:
        messagebox.showerror("Something went wrong.", str(e))


def getExcelFile():
    filetypes = [('CSV files', '*.csv')]
    filepath = fd.askopenfilename(
        title='Open a file',
        filetypes=filetypes
    )

    if not filepath:
        raise Exception('Please select a file.')

    return filepath


def analizeFileAndShowCharts(filepath):
    df = pd.read_csv(filepath)

    try:
        ageDataFrame = df[['edad']].round(
            decimals=0).value_counts().sort_index()
    except Exception:
        raise Exception('The excel file must have the column "edad"')

    try:
        pd.to_numeric(df['edad'], errors='raise').notnull().all()
    except Exception as e:
        raise Exception(
            'The column "edad" must only contain numbers. Error on index: ' + str(e)[-1])

    try:
        breedDataFrame = df[['raza']].value_counts().sort_index()
    except Exception:
        raise Exception('The excel file must have the column "raza"')

    root = tk.Toplevel()
    root.title("Dog charts")

    putDogsAgesChart(agesDataFrame=ageDataFrame, root=root)
    putDogBreedsChart(breedsDataFrame=breedDataFrame, root=root)


def putDogsAgesChart(agesDataFrame, root):
    agesFigure = plt.figure(figsize=(5, 8), dpi=100)
    ax1 = agesFigure.add_subplot(111)
    bar1 = FigureCanvasTkAgg(agesFigure, root)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.NONE)
    agesDataFrame.plot(kind='bar', legend=False, ax=ax1)
    ax1.set_title('Dogs by age')


def putDogBreedsChart(breedsDataFrame, root):
    breedsFigure = plt.figure(figsize=(11, 8), dpi=100)
    ax2 = breedsFigure.add_subplot(111)
    bar2 = FigureCanvasTkAgg(breedsFigure, root)
    bar2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE)
    breedsDataFrame.plot(kind='bar', legend=False, ax=ax2)
    ax2.set_title('Dogs by breed')


def main():
    root = tk.Tk()
    root.geometry('150x150')
    selectExcelButton = tk.Button(
        root, text='Select file', command=handleSelectFileButton)
    selectExcelButton.pack(side=tk.TOP)

    try:
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", str(e))


if __name__ == "__main__":
    main()
