import threading
import tkinter as tk
from tkinter import scrolledtext

from nano_core import Nano


class NanoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Nano")

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, width=80, height=24)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")

        self.entry = tk.Entry(self.root, width=72)
        self.entry.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="ew")
        self.entry.bind("<Return>", self._on_send)

        self.send_button = tk.Button(self.root, text="Send", command=self._on_send)
        self.send_button.grid(row=1, column=1, padx=(0, 8), pady=(0, 8), sticky="e")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.nano = Nano()

    def _append_text(self, text: str) -> None:
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + "\n")
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def _on_send(self, event=None) -> None:  # type: ignore[no-redef]
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self._append_text(f"You: {user_text}")

        thread = threading.Thread(target=self._handle_in_background, args=(user_text,), daemon=True)
        thread.start()

    def _handle_in_background(self, user_text: str) -> None:
        try:
            reply = self.nano.handle_user_input(user_text)
        except Exception as exc:
            reply = f"[Error] {exc}"
        self.root.after(0, lambda: self._append_text(f"Nano: {reply}"))


def main() -> None:
    root = tk.Tk()
    app = NanoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

