import argparse
import secrets
import string
import sys
import tkinter as tk
from tkinter import ttk


def generate_password(length: int, use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> str:
    if length < 1:
        raise ValueError("Length must be at least 1.")

    chars = ""
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?"

    if not chars:
        raise ValueError("At least one character type must be enabled.")

    return "".join(secrets.choice(chars) for _ in range(length))


def run_gui() -> None:
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("420x340")
    root.resizable(False, False)

    length_var = tk.IntVar(value=16)
    use_upper_var = tk.BooleanVar(value=True)
    use_lower_var = tk.BooleanVar(value=True)
    use_digits_var = tk.BooleanVar(value=True)
    use_symbols_var = tk.BooleanVar(value=True)
    count_var = tk.IntVar(value=1)
    output_var = tk.StringVar(value="")

    def generate_button_click() -> None:
        try:
            passwords = [
                generate_password(
                    length=length_var.get(),
                    use_upper=use_upper_var.get(),
                    use_lower=use_lower_var.get(),
                    use_digits=use_digits_var.get(),
                    use_symbols=use_symbols_var.get(),
                )
                for _ in range(count_var.get())
            ]
            output_var.set("\n".join(passwords))
        except ValueError as error:
            output_var.set(str(error))

    frame = ttk.Frame(root, padding=12)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Password length:").grid(column=0, row=0, sticky="w")
    ttk.Spinbox(frame, from_=1, to=128, textvariable=length_var, width=8).grid(column=1, row=0, sticky="w")

    ttk.Checkbutton(frame, text="Uppercase", variable=use_upper_var).grid(column=0, row=1, sticky="w")
    ttk.Checkbutton(frame, text="Lowercase", variable=use_lower_var).grid(column=1, row=1, sticky="w")
    ttk.Checkbutton(frame, text="Digits", variable=use_digits_var).grid(column=0, row=2, sticky="w")
    ttk.Checkbutton(frame, text="Symbols", variable=use_symbols_var).grid(column=1, row=2, sticky="w")

    ttk.Label(frame, text="Number of passwords:").grid(column=0, row=3, sticky="w")
    ttk.Spinbox(frame, from_=1, to=20, textvariable=count_var, width=8).grid(column=1, row=3, sticky="w")

    ttk.Button(frame, text="Generate", command=generate_button_click).grid(column=0, row=4, columnspan=2, pady=10)

    output_label = ttk.Label(frame, text="Result:")
    output_label.grid(column=0, row=5, columnspan=2, sticky="w")

    output_box = tk.Text(frame, width=48, height=8, wrap="word", state="normal")
    output_box.grid(column=0, row=6, columnspan=2, pady=(4, 0))
    output_box.insert("1.0", output_var.get())
    output_box.config(state="disabled")

    def update_output(*args: object) -> None:
        output_box.config(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", output_var.get())
        output_box.config(state="disabled")

    output_var.trace_add("write", update_output)

    for child in frame.winfo_children():
        child.grid_configure(padx=4, pady=4)

    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Secure password generator.")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
    parser.add_argument("--no-upper", action="store_false", dest="use_upper", help="Do not use uppercase letters")
    parser.add_argument("--no-lower", action="store_false", dest="use_lower", help="Do not use lowercase letters")
    parser.add_argument("--no-digits", action="store_false", dest="use_digits", help="Do not use digits")
    parser.add_argument("--no-symbols", action="store_false", dest="use_symbols", help="Do not use symbols")
    parser.add_argument("-n", "--count", type=int, default=1, help="How many passwords to generate")
    parser.add_argument("--cli", action="store_true", help="Use command-line mode")

    args = parser.parse_args()

    if args.cli:
        try:
            for i in range(args.count):
                password = generate_password(
                    length=args.length,
                    use_upper=args.use_upper,
                    use_lower=args.use_lower,
                    use_digits=args.use_digits,
                    use_symbols=args.use_symbols,
                )
                print(password)
        except ValueError as error:
            parser.error(str(error))
        return

    run_gui()


if __name__ == "__main__":
    main()
