from tkinter import *
from tkinter import ttk
from math import log
from tkinter.messagebox import showinfo, showerror
import json


def load_json():
    with open('promo.json') as fp:
        return json.load(fp)


def save_json(json_file):
    with open('promo.json', 'w', encoding='utf-8') as fp:
        json.dump(json_file, fp, indent=4, ensure_ascii=False)


json_file = {}
try:
    json_file = load_json()
except FileNotFoundError:
    json_file = {'staff_codes': [], 'card_used': {'card_code': ''}}


def main_window():
    root = Tk()
    root.title('Промо')
    window_width = 1
    window_height = 1
    font_size = 1
    root.geometry(f'300x200+{int(root.winfo_screenwidth() / 2) - int(300 / 2)}+{int(root.winfo_screenheight() / 2) - int(300 / 2)}')
    root.minsize(310, 200)

    def config(event):
        nonlocal window_height
        nonlocal window_width
        nonlocal font_size
        if event.widget == root:
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            font_size = int((window_width + window_height) / log(window_width + window_height, 1.1) + 5)
            staff_label['font'] = staff_combo['font'] = card_label['font'] = card_entry['font'] = ('', font_size)
            print(window_width, window_height)

    def create_frame(master, label_text):
        frame = ttk.Frame(master, borderwidth=1, relief=SOLID, padding=[5, 5])
        label = ttk.Label(frame, text=label_text, font=('', 13))
        label.pack(anchor=NW)
        return frame, label

    def create_combo_frame(master, label_text, items_list):
        frame, label = create_frame(master, label_text)
        combo = ttk.Combobox(frame, values=items_list, state='readonly')
        combo.pack(fill=X, side='left', expand=True)
        btn_remove = ttk.Button(frame, text='-', width=5)
        btn_remove.pack(side='right', expand=1)
        btn_add = ttk.Button(frame, text='+', width=5)
        btn_add.pack(side='right', expand=1)
        return frame, combo, label, btn_add, btn_remove

    def create_entry_frame(master, label_text):
        frame, label = create_frame(master, label_text)
        entry = ttk.Entry(frame, width=20, font=('', 16))
        entry.pack(anchor=NW, fill=X)
        return frame, entry, label

    def save_text(entry, combo):
        print(entry.get(), combo.get())

    # Dialog window ----------------------------------------
    def add_to_items_list_window(master, combo, items_list, mode):
        master.withdraw()
        window = Toplevel(master)
        window.title('Добавить сотрудника')
        window.geometry(f'300x300+{int(window.winfo_screenwidth() / 2) - int(300 / 2)}+{int(window.winfo_screenheight() / 2) - int(300 / 2)}')

        def win_destroy(win):
            win.grab_release()
            win.destroy()
            master.deiconify()

        def get_valid_item(entry):
            if entry.get().strip() != '':
                try:
                    return int(entry.get().replace(' ', ''))
                except ValueError:
                    showerror('Ошибка', f'В строке "{entry.get()}" должны быть только цифры')
            return False

        def change_items_list(combo, entry, items_list):
            value = get_valid_item(entry)
            if value:
                if value not in items_list:
                    if mode == 'remove':
                        showinfo('Информация', f'Пользователя "{value}" нет в списке')
                    else:
                        items_list.append(value)
                        combo['values'] = items_list
                        entry.delete(0, END)
                else:
                    if mode == 'remove':
                        items_list.remove(value)
                        combo['values'] = items_list
                        entry.delete(0, END)
                    else:
                        showinfo('Информация', f'Пользователь "{value}" уже записан')

        window.protocol('WM_DELETE_WINDOW', lambda: win_destroy(window))

        if mode == 'remove':
            dialog_staff_frame, dialog_staff_entry, _ = create_entry_frame(window, 'Удалить продавца')
            dialog_staff_btn = ttk.Button(window,
                                          command=lambda: change_items_list(combo, dialog_staff_entry, items_list),
                                          text='Удалить')
        else:
            dialog_staff_frame, dialog_staff_entry, _ = create_entry_frame(window, 'Добавить продавца')
            dialog_staff_btn = ttk.Button(window,
                                          command=lambda: change_items_list(combo, dialog_staff_entry, items_list),
                                          text='Добавить')
        dialog_staff_frame.pack(fill=X, pady=5, padx=5)
        dialog_staff_btn.pack(pady=5)

        window.grab_set()
        window.wait_window()

    card_frame, card_entry, card_label = create_entry_frame(root, 'Номер карты')
    card_frame.pack(fill=X, pady=5, padx=5)

    staff_list = [1, 2, 3, 4]

    staff_frame, staff_combo, staff_label, staff_btn_add, staff_btn_remove = create_combo_frame(root, 'Код сотрудника', staff_list)
    staff_btn_add['command'] = lambda: add_to_items_list_window(root, staff_combo, staff_list, 'add')
    staff_btn_remove['command'] = lambda: add_to_items_list_window(root, staff_combo, staff_list, 'remove')
    staff_frame.pack(fill=X, padx=5, pady=5)

    btn_ok = ttk.Button(command=lambda: save_text(card_entry, staff_combo))
    btn_ok['text'] = 'OK'
    btn_ok.pack(side='bottom', pady=10)

    root.bind("<Configure>", config)
    root.mainloop()


if __name__ == '__main__':
    main_window()