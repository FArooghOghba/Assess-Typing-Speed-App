from tkinter import *
from tkinter import messagebox

LIGHTEN_GREEN = '#EDFFEC'
GREEN = '#CAF7E3'
LIGHT_GREEN = '#B5FE83'
GREY = '#D1D1D1'
FONT = 'Helvetica'
frames = {}
word_index = 0
space_counter = 0
word_label_index_bg = 1
word_per_min = 0
char_per_min = 0
usr_wrong_words = {}
actual_word_per_min = 0
actual_char_per_min = 0
timer = ''


def gui_app():
    window = Tk()
    window.title('   Assess Typing Speed App')
    window.iconbitmap('favicon.ico')
    window.geometry('900x600')

    # ---------------------------- Reset Mechanism ---------------------------- #
    def reset_timer():
        global space_counter, word_index, word_per_min, char_per_min, actual_word_per_min, actual_char_per_min, usr_wrong_words, word_label_index_bg

        window.after_cancel(timer)
        window.focus_set()
        cpm_entry_label.config(text='?')
        wpm_entry_label.config(text='?')
        time_entry_label.config(text='60')
        typing_entry.delete(0, END)
        typing_entry.config(fg=GREY)
        typing_entry.insert(END, 'type the words here')
        word_per_min = 0
        char_per_min = 0
        usr_wrong_words = {}
        actual_word_per_min = 0
        actual_char_per_min = 0
        word_label_index_bg = 1
        word_index = 0
        space_counter = 0

        # TEXT READER
        grid = 0
        for a in range(5):
            for b in range(5):
                element_index = str(a) + str(b)
                frames[element_index].config(text=words[grid], bg=LIGHTEN_GREEN)
                frames[element_index].pack()

                grid += 1
        list(frames.values())[0].config(bg=LIGHT_GREEN)

    # ---------------------------- Countdown Mechanism Timer ---------------------------- #

    def score(cpm, wpm, wrong_words):
        score_label = Label(
            text=f'Your score: {cpm} CPM (that is {wpm} WPM)\n\n',
            font=(FONT, 25, 'bold'),
            fg='#3F3351',
            bg=LIGHTEN_GREEN
        )
        score_label.pack(pady=40)

        if len(wrong_words) > 0:
            title_label = Label(
                text='Your mistakes were:\n',
                font=(FONT, 15, 'bold'),
                fg='#3F3351',
                bg=LIGHTEN_GREEN
            )
            title_label.pack()

            for usr_word in wrong_words:
                usr_word_label = Label(
                    text=f'>> Instead of "{usr_word}", you typed "{wrong_words[usr_word]}".',
                    font=(FONT, 15, 'bold'),
                    fg='#3F3351',
                    bg=GREEN
                )
                usr_word_label.pack(pady=5)

            footer_label = Label(
                text=f'You typed {actual_char_per_min} CPM, but you made {actual_word_per_min-word_per_min} mistakes (out of {actual_word_per_min} worlds),\n'
                     f'which were not counted in the corrected scores.',
                font=(FONT, 15, 'bold'),
                fg='#3F3351',
                bg=LIGHTEN_GREEN
            )
            footer_label.pack(pady=30)

    # ---------------------------- Countdown Mechanism Timer ---------------------------- #

    def count_down(count):
        global timer

        count_sec = str(count).zfill(2)

        time_entry_label.config(text=count_sec)
        if count > 0:
            timer = window.after(1000, count_down, count - 1)
        else:
            reader_frame.destroy()
            scoreboard_frame.destroy()
            typing_frame.destroy()
            window.config(bg=LIGHTEN_GREEN)
            score(char_per_min, word_per_min, usr_wrong_words)

    # ------------------------------- Check Entry words ------------------------------- #

    def check_entry_words(every_word, every_word_index):
        global word_per_min, char_per_min, actual_word_per_min, actual_char_per_min

        labels = list(frames.values())

        wpm_entry_label.config(text=0)
        cpm_entry_label.config(text=0)

        word_reader_label = labels[every_word_index]['text'].strip()
        word_user_enter = every_word.strip()
        if word_reader_label == word_user_enter:
            print(labels[every_word_index]['text'], every_word)

            word_per_min += 1
            char_per_min += len(word_user_enter)
        else:
            usr_wrong_words[word_reader_label] = word_user_enter

        wpm_entry_label.config(text=str(word_per_min))
        cpm_entry_label.config(text=str(char_per_min))
        actual_word_per_min += 1
        actual_char_per_min += len(word_user_enter)

    # ------------------------------- Word Bg Color ------------------------------- #
    def word_bg_color():
        global word_label_index_bg

        if word_label_index_bg == 5:
            list(frames.values())[4].config(bg=LIGHTEN_GREEN)
            word_label_index_bg = 0

        list(frames.values())[word_label_index_bg - 1].config(bg=LIGHTEN_GREEN)
        list(frames.values())[word_label_index_bg].config(bg=LIGHT_GREEN)
        word_label_index_bg += 1

    # ------------------------------- Get Typing Entry ------------------------------- #

    def get_typing_entry(event):
        global word_index, space_counter

        if event.keysym == 'space':
            word = typing_entry.get()
            typing_entry.delete(0, END)

            word_bg_color()  # changing word bg color
            check_entry_words(word, space_counter)  # checking entry words

            # ------------- Scrolling Text ------------- #
            space_counter += 1
            if space_counter == 5:
                word_index += 5

                for fr in list(frames.values()):
                    fr.config(text=words[word_index])
                    word_index += 1
                word_index -= 25
                space_counter = 0
        elif event.keysym == 'Return':
            messagebox.showerror(
                title='typing speed test',
                message='Use space bar instead of enter, \nUse the "Restart" button to start over.'
            )

    # ------------------------------- Clear Typing Entry ------------------------------- #

    def clear_typing(event):
        typing_entry.delete(0, END)
        typing_entry.config(fg='black')
        typing_entry.unbind('<FocusIn>')
        count_down(60)

    # ------------------------------- Tkinter UI Setup ------------------------------- #

    # WINDOW ROW & COLUMN CONFIGURATION
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=3)
    window.rowconfigure(2, weight=1)
    window.columnconfigure(0, weight=1)

    # SCOREBOARD FRAME
    scoreboard_frame = Frame(window, bg=GREEN)
    scoreboard_frame.grid(row=0, column=0, sticky="nsew")

    # SCOREBOARD FRAME ROW & COLUMN CONFIGURATION
    scoreboard_frame.rowconfigure(0, weight=1)

    # CPM LABEL (CHARACTER PER MINUET)
    cpm_label = Label(scoreboard_frame, text='Corrected CPM:', font=(FONT, 10), bg=GREEN)
    cpm_label.place(relx=0.22, rely=0.5, anchor=CENTER)

    # CPM ENTRY LABEL
    cpm_entry_label = Label(scoreboard_frame, text='?', width=4, font=(FONT, 12), justify='center', relief=SUNKEN)
    cpm_entry_label.place(relx=0.30, rely=0.5, anchor=CENTER)

    # WPM LABEL (WORD PER MINUTE)
    wpm_label = Label(scoreboard_frame, text='WPM:', font=(FONT, 10), bg=GREEN)
    wpm_label.place(relx=0.42, rely=0.5, anchor=CENTER)

    # WPM ENTRY LABEL
    wpm_entry_label = Label(scoreboard_frame, text='?', width=4, font=(FONT, 12), justify='center', relief=SUNKEN)
    wpm_entry_label.place(relx=0.47, rely=0.5, anchor=CENTER)

    # TIME LEFT LABEL
    time_label = Label(scoreboard_frame, text='Time left:', font=(FONT, 10), bg=GREEN)
    time_label.place(relx=0.59, rely=0.5, anchor=CENTER)

    # TIME ENTRY LABEL
    time_entry_label = Label(scoreboard_frame, text='60', width=4, font=(FONT, 12), justify='center', relief=SUNKEN)
    time_entry_label.place(relx=0.65, rely=0.5, anchor=CENTER)

    # RESTART BUTTON
    restart_button = Button(scoreboard_frame, text='Restart', font=(FONT, 10), command=reset_timer)
    restart_button.place(relx=0.8, rely=0.5, anchor=CENTER)

    # READER FRAME
    reader_frame = Frame(window, bg=LIGHTEN_GREEN)
    reader_frame.grid(row=1, column=0, sticky="nsew")

    # TEXT READER LABEL
    with open(file='text.txt') as text:
        reader = text.read()

    words = reader.split()

    # TEXT READER
    word_grid = 0
    for i in range(5):
        reader_frame.columnconfigure(i, weight=1)
        reader_frame.rowconfigure(i, weight=1)

        for j in range(5):
            frame = Frame(reader_frame)
            frame.grid(row=i, column=j)

            word_dict_index = str(i) + str(j)
            frames[word_dict_index] = Label(frame, text=words[word_grid], bg=LIGHTEN_GREEN, font=(FONT, 26))
            frames[word_dict_index].pack()

            word_grid += 1

    list(frames.values())[0].config(bg=LIGHT_GREEN)

    # TYPING FRAME
    typing_frame = Frame(window, bg=GREEN)
    typing_frame.grid(row=2, column=0, sticky="nsew")

    # TYPING ENTRY
    typing_entry = Entry(typing_frame, width=50, font=(FONT, 18), justify='center', fg=GREY)
    typing_entry.insert(END, 'type the words here')
    typing_entry.bind('<FocusIn>', clear_typing)
    typing_entry.bind('<Key>', get_typing_entry)
    typing_entry.place(relx=0.5, rely=0.5, anchor=CENTER)


if __name__ == '__main__':
    gui_app()
    mainloop()
