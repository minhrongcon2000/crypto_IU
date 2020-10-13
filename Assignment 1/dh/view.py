import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import secrets
import dh


class GroupField(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.group_list = [
            "  5",
            "14",
            "15",
            "16",
            "17",
            "18"
        ]
        self.value = tk.IntVar()
        self.create_widget()

    def create_widget(self):
        self.group_label = tk.Label(
            self, text="Choose a group to generate common keys...")
        self.group_label.grid(row=0, column=0)

        for val, name in enumerate(self.group_list):
            tk.Radiobutton(self, text=name, value=int(name),
                           variable=self.value).grid(row=val+1, column=0)


class SharedKeyField(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widget()

    def create_widget(self):
        self.group_field = GroupField(self)
        self.group_field.grid(row=0, column=0, columnspan=2)

        self.label = tk.Label(self, text="Common keys")
        self.label.grid(row=1, column=0, columnspan=2)

        self.modulus_label = tk.Label(self, text="Modulus")
        self.modulus_label.grid(row=2, column=0, sticky=tk.W)
        self.modulus_entry = tk.Entry(self)
        self.modulus_entry.configure(state='disabled')
        self.modulus_entry.grid(row=2, column=1)

        self.generator_label = tk.Label(self, text="Generator")
        self.generator_label.grid(row=3, column=0, sticky=tk.W)
        self.generator_entry = tk.Entry(self)
        self.generator_entry.configure(state='disabled')
        self.generator_entry.grid(row=3, column=1, pady=(0, 10))

        self.generate_btn = tk.Button(
            self, text="Generate...", bg="yellow", activeforeground="blue", command=self.onButtonPressed)
        self.generate_btn.grid(row=4, column=0, columnspan=2)

    def onButtonPressed(self):
        if self.group_field.value.get() == 0:
            tk.messagebox.showerror(
                title="KeyError", message="Please choose a group to generate common keys")
            return
        chosen_group = self.group_field.value.get()

        self.modulus_entry.configure(state='normal')
        self.modulus_entry.delete(0, tk.END)
        self.modulus_entry.insert(0, dh.SHARED_KEY[chosen_group]["p"])
        self.modulus_entry.configure(state='disabled')

        self.generator_entry.configure(state='normal')
        self.generator_entry.delete(0, tk.END)
        self.generator_entry.insert(0, dh.SHARED_KEY[chosen_group]["g"])
        self.generator_entry.configure(state='disabled')


class UserBox(tk.Frame):
    def __init__(self, username, master=None):
        super().__init__(master)
        self.username = username
        self.create_widget()

    def create_widget(self):
        self.title_label = tk.Label(self, text=self.username)
        self.title_label.grid(row=0, column=0, columnspan=2)

        self.private_label = tk.Label(self, text="Private Key")
        self.private_label.grid(row=1, column=0, sticky=tk.W)
        self.private_entry = tk.Entry(self)
        self.private_entry.grid(row=2, column=0)

        self.public_label = tk.Label(self, text="Public Key")
        self.public_label.grid(row=3, column=0, sticky=tk.W)
        self.public_entry = tk.Entry(self)
        self.public_entry.configure(state="disabled")
        self.public_entry.grid(row=4, column=0, pady=(0, 10))

        self.generate_btn = tk.Button(
            self, text="Generate...", activeforeground="blue", command=self.onButtonPressed)
        self.generate_btn.grid(row=5, column=0, columnspan=2)

    def onButtonPressed(self):
        user_input_bits = tkinter.simpledialog.askinteger(
            title="Test", prompt="Input the bits")
        self.private_entry.delete(0, tk.END)
        self.private_entry.insert(0, secrets.randbits(user_input_bits))


class AliceBobFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widget()

    def create_widget(self):
        self.alice_frame = tk.Frame(self, padx=20)
        self.alice_frame.grid(row=0, column=0)
        self.alice_box = UserBox("Alice", self.alice_frame)
        self.alice_box.grid(row=0, column=0)

        self.bob_frame = tk.Frame(self, padx=20)
        self.bob_frame.grid(row=0, column=1)
        self.bob_box = UserBox("Bob", self.bob_frame)
        self.bob_box.grid(row=0, column=0)


class MessageBox(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.message_label = tk.Label(self, text="Message")
        self.message_label.grid(row=0, column=0,
                                sticky=tk.W, pady=(20, 10))
        self.message_txt = tk.Text(
            self, width=50, height=10, padx=10, pady=10)
        self.message_txt.configure(state="disabled")
        self.message_txt.grid(row=1, column=0)


class SecretKeyField(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widget()

    def create_widget(self):
        self.secret_label = tk.Label(self, text="Secret key")
        self.secret_label.grid(row=0, column=0)

        self.secret_entry = tk.Entry(self)
        self.secret_entry.grid(row=0, column=1)


class MainApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.management_sys = dh.DHSystem()
        self.create_widget()

    def create_widget(self):
        self.global_content = SharedKeyField(self)
        self.global_content.grid(row=0, column=0, columnspan=2)

        self.user_frame = AliceBobFrame(self)
        self.user_frame.grid(row=1, column=0)

        self.message_box = MessageBox(self)
        self.message_box.grid(row=2, column=0, columnspan=2)

        self.secret_key_field = SecretKeyField(self)
        self.secret_key_field.grid(row=3, column=0, columnspan=2)

        self.exe_btn = tk.Button(
            self, text="Run...", activeforeground="blue", command=self.onButtonPressed)
        self.exe_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def __insertText(self, text):
        self.message_box.message_txt.configure(state='normal')
        self.message_box.message_txt.insert(tk.INSERT, text + '\n')
        self.message_box.message_txt.configure(state='disabled')

    def __clearText(self):
        self.message_box.message_txt.configure(state='normal')
        self.message_box.message_txt.delete("1.0", tk.END)
        self.message_box.message_txt.configure(state='disabled')

    def __insertField(self, field, content):
        field.configure(state='normal')
        field.delete(0, tk.END)
        field.insert(tk.INSERT, content)
        field.configure(state='disabled')

    def __isValidField(self, value):
        return value.isdecimal() and int(value) > 0

    def onButtonPressed(self):
        self.__clearText()

        isSharedKeysGenerated = self.__isValidField(self.global_content.modulus_entry.get(
        )) and self.__isValidField(self.global_content.generator_entry.get())

        if not isSharedKeysGenerated:
            tk.messagebox.showerror(
                title="Invalid shared keys", message="User hasn't generated common keys yet!")
            return

        self.management_sys.generator = int(
            self.global_content.generator_entry.get())
        self.management_sys.modulus = int(
            self.global_content.modulus_entry.get())

        isAlicePrivateKeysGenerated = self.__isValidField(
            self.user_frame.alice_box.private_entry.get())

        if not isAlicePrivateKeysGenerated:
            tk.messagebox.showerror(
                title="Invalid Alice's keys", message="User hasn't generated Alice's keys yet!")
            return

        isBobPrivateKeysGenerated = self.__isValidField(
            self.user_frame.bob_box.private_entry.get())

        if not isBobPrivateKeysGenerated:
            tk.messagebox.showerror(
                title="Invalid Alice's keys", message="User hasn't generated Bob's keys yet!")
            return

        self.management_sys.addUsers(
            self.user_frame.alice_box.title_label['text'],
            int(self.user_frame.alice_box.private_entry.get())
        )

        self.management_sys.addUsers(self.user_frame.bob_box.title_label['text'], int(
            self.user_frame.bob_box.private_entry.get()))

        self.__insertField(self.user_frame.alice_box.public_entry, self.management_sys.getPublicKey(
            self.user_frame.alice_box.title_label['text']
        ))

        self.__insertField(self.user_frame.bob_box.public_entry, self.management_sys.getPublicKey(
            self.user_frame.bob_box.title_label['text']
        ))

        # Alice send Bob public key
        self.management_sys.createMessage(
            self.user_frame.alice_box.title_label['text'],
            self.user_frame.bob_box.title_label['text'],
            int(self.user_frame.alice_box.public_entry.get())
        )

        self.__insertText("=================================\n{} -> {}:\n{}\n=================================".format(
            self.management_sys.messages[-1].sender.username,
            self.management_sys.messages[-1].receiver.username, self.management_sys.messages[-1].content
        ))

        # Bob send Alice public key
        self.management_sys.createMessage(
            self.user_frame.bob_box.title_label['text'],
            self.user_frame.alice_box.title_label['text'],
            int(self.user_frame.bob_box.public_entry.get())
        )

        self.__insertText("\n{} -> {}:\n{}\n=================================".format(
            self.management_sys.messages[-1].sender.username,
            self.management_sys.messages[-1].receiver.username, self.management_sys.messages[-1].content
        ))
        self.__insertField(self.secret_key_field.secret_entry,
                           self.management_sys.getSecretKey())
        self.global_content.modulus_entry.configure(state='normal')
        self.global_content.generator_entry.configure(state='normal')
        self.user_frame.alice_box.public_entry.configure(state='normal')
        self.user_frame.bob_box.public_entry.configure(state='normal')
        self.secret_key_field.secret_entry.configure(state='normal')


app = tk.Tk()
app.title('Diffie-Hellman Protocol Simulation')
app.geometry("550x750+500+100")

mainApp = MainApp(app)
mainApp.grid(row=0, column=0)

app.mainloop()
