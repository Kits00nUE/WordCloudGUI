import customtkinter  ##zmodyfikowany tkinter, nanarzędzie do interfejsu graficznego uzytkownika
from tkinter import \
    filedialog  ##do otwierania okien dialogowych plików, umożliwiających użytkownikowi wybór plików lub katalogów
from wordcloud import WordCloud  ## to stworzenia wizualnej grafiki w pythone, aktualnie do stworzenia wordclouda
import \
    matplotlib.pyplot as plt  ## uzytkowana do tworzenia róznych wizualizacji, u nas do wyświetlenia wygenerowanej chmury
from rich.console import Console  ## formatowanie tekstu w konsoli
from nltk.tokenize import word_tokenize  ##tokenizacja
from nltk.probability import FreqDist  ## analiza dystrybycji częstotliwości słów
from nltk.corpus import stopwords
import nltk  ## natural language toolkit, do pracy z danymi językowymi

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

nltk.download('punkt')  ## dzielenie tekstu do na słowa, dokladnie ,,tokeny"
nltk.download(
    'stopwords')  ## pobieranie listy popoularnych słow, które nastepnie mają być omijane w tworzeniu wordclouda, poniewaz nie niosą dużo informacji


class WordCloudApp:
    def __init__(self):
        self.file_path = None
        self.root = customtkinter.CTk()
        self.root.geometry("500x350")
        plt.style.use('dark_background')

        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="WordCloudApp", font=("Roboto", 24))
        label.pack(pady=12, padx=10)

        button_choose_file = customtkinter.CTkButton(master=frame, text='Wybierz plik', command=self.choose_file)
        button_choose_file.pack(pady=12, padx=10)

        label_color = customtkinter.CTkLabel(master=frame, text="wybierz kolor:", fg_color="transparent")
        label_color.pack(pady=10, padx=10)

        colormaps_list = list(plt.colormaps())
        self.combobox = customtkinter.CTkComboBox(master=frame, values=colormaps_list)
        self.combobox.pack(padx=12, pady=10)
        self.combobox.set("viridis")  # ustawienie domyślnego motywu wordclouda

        button_generate_wordcloud = customtkinter.CTkButton(master=frame, text='Generuj WordCloud',
                                                            command=self.generate_wordcloud_callback)
        button_generate_wordcloud.pack(pady=12, padx=10)

    def generate_wordcloud(self, file_path, colormap_name):
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # tokenizacja tekstu
        words = word_tokenize(text_content.lower())

        # usunięcie tokenów nic nie wnosząch(and, a ,the)
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # liczenie słów
        word_count = len(words)

        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

        # Find most common words
        freq_dist = FreqDist(words)
        most_common_words = freq_dist.most_common(5)

        # Choose colormap
        colormap = plt.get_cmap(colormap_name)

        # generowanie wordclouda wraz z wybranym colormapem
        wordcloud = WordCloud(width=800, height=400, colormap=colormap).generate_from_frequencies(freq_dist)

        # wyświetlanie w konsoli informacji na temat tekstu
        console = Console()
        console.print(f"Liczba słów: [bold]{word_count}[/bold]")
        console.print(f"Średnia długość słowa: [bold]{avg_word_length:.2f}[/bold] znaków")
        console.print("Najczęściej występujące słowa:")
        for word, frequency in most_common_words:
            console.print(f"{word}: [bold]{frequency}[/bold] razy")
        # wyswietlanie wordclouda
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')  # bilinear do tego, aby wygładzić obraz
        plt.axis('off')  # wylączenie widocznosci osi na obrazie
        plt.show()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(title="Wybierz plik tekstowy", filetypes=[("Text files", "*.txt")])

    def generate_wordcloud_callback(self):
        if self.file_path:
            colormap_name = self.combobox.get()
            self.generate_wordcloud(self.file_path, colormap_name)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WordCloudApp()
    app.run()