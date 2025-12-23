import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data_file = "expenses.csv"
        self.load_data()

        # Budget
        self.budget = 0.0

        # Create UI
        self.create_widgets()

    def load_data(self):
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        else:
            self.df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

    def save_data(self):
        self.df.to_csv(self.data_file, index=False)

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Expense")
        input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky="w")
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Amount:").grid(row=2, column=0, sticky="w")
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=3, column=0, sticky="w")
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)

        # Budget Frame
        budget_frame = ttk.LabelFrame(self.root, text="Budget")
        budget_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(budget_frame, text="Set Budget:").grid(row=0, column=0, sticky="w")
        self.budget_entry = ttk.Entry(budget_frame)
        self.budget_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(budget_frame, text="Set Budget", command=self.set_budget).grid(row=0, column=2, padx=5, pady=5)

        # Actions Frame
        actions_frame = ttk.LabelFrame(self.root, text="Actions")
        actions_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(actions_frame, text="Upload CSV", command=self.upload_csv).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(actions_frame, text="Pie Chart by Category", command=self.pie_chart).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_frame, text="Bar Chart by Date", command=self.bar_chart).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(actions_frame, text="Export to Excel", command=self.export_excel).grid(row=0, column=3, padx=5, pady=5)

        # Data Display
        display_frame = ttk.LabelFrame(self.root, text="Expenses")
        display_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(display_frame, columns=('Date', 'Category', 'Amount', 'Description'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Description', text='Description')
        self.tree.pack(fill="both", expand=True)

        self.update_display()

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()

        try:
            amount = float(amount)
            date = pd.to_datetime(date)
            new_row = pd.DataFrame({'Date': [date], 'Category': [category], 'Amount': [amount], 'Description': [desc]})
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save_data()
            self.update_display()
            self.check_budget()
            messagebox.showinfo("Success", "Expense added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def set_budget(self):
        try:
            self.budget = float(self.budget_entry.get())
            messagebox.showinfo("Success", f"Budget set to {self.budget}")
        except ValueError:
            messagebox.showerror("Error", "Invalid budget!")

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                new_df = pd.read_csv(file_path)
                new_df['Date'] = pd.to_datetime(new_df['Date'])
                self.df = pd.concat([self.df, new_df], ignore_index=True)
                self.save_data()
                self.update_display()
                self.check_budget()
                messagebox.showinfo("Success", "CSV uploaded!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def pie_chart(self):
        if self.df.empty:
            messagebox.showwarning("Warning", "No data to plot!")
            return
        category_sum = self.df.groupby('Category')['Amount'].sum()
        plt.figure(figsize=(8, 6))
        plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.show()

    def bar_chart(self):
        if self.df.empty:
            messagebox.showwarning("Warning", "No data to plot!")
            return
        self.df['Date'] = self.df['Date'].dt.date
        date_sum = self.df.groupby('Date')['Amount'].sum()
        plt.figure(figsize=(10, 6))
        date_sum.plot(kind='bar')
        plt.title('Expenses by Date')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.show()

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", "Exported to Excel!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_display(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in self.df.iterrows():
            self.tree.insert('', 'end', values=(row['Date'].strftime('%Y-%m-%d'), row['Category'], row['Amount'], row['Description']))

    def check_budget(self):
        total = self.df['Amount'].sum()
        if self.budget > 0 and total > self.budget:
            messagebox.showwarning("Budget Alert", f"Total expenses ({total}) exceed budget ({self.budget})!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
