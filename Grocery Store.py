import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass


# =========================
# Data Models / Config
# =========================
@dataclass(frozen=True)
class Product:
    name: str
    price: float


PRODUCT_PRICES = {
    "Apple": Product("Apple", 3.00),
    "Biscuit": Product("Biscuit", 3.00),
    "Bread": Product("Bread", 2.00),
    "Chicken": Product("Chicken", 5.00),
    "Coke": Product("Coke", 2.00),
    "Egg": Product("Egg", 1.00),
    "Fish": Product("Fish", 3.00),
    "Onion": Product("Onion", 3.00),
}

DISCOUNT_RATES = {
    "Gold": 0.10,
    "Silver": 0.05,
    "Bronze": 0.00,
}


# =========================
# Business Logic
# =========================
class GroceryCheckoutService:
    def __init__(self, products: dict[str, Product], discounts: dict[str, float]):
        self.products = products
        self.discounts = discounts

    def validate_quantity(self, quantity_text: str) -> int:
        try:
            quantity = int(quantity_text)
        except ValueError as exc:
            raise ValueError("Quantity must be a whole number.") from exc

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        return quantity

    def calculate_subtotal(self, product_name: str, quantity: int) -> float:
        if product_name not in self.products:
            raise ValueError(f"Unknown product: {product_name}")
        return self.products[product_name].price * quantity

    def calculate_bill(self, cart: dict[str, int], membership: str) -> dict:
        if not cart:
            raise ValueError("Cart is empty.")

        if membership not in self.discounts:
            raise ValueError("Invalid membership type.")

        line_items = []
        bill_amount = 0.0

        for product_name, quantity in cart.items():
            unit_price = self.products[product_name].price
            subtotal = unit_price * quantity
            bill_amount += subtotal

            line_items.append(
                {
                    "product": product_name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "subtotal": subtotal,
                }
            )

        discount_rate = self.discounts[membership]
        discount_amount = bill_amount * discount_rate
        final_total = bill_amount - discount_amount

        return {
            "line_items": line_items,
            "bill_amount": round(bill_amount, 2),
            "discount_rate": discount_rate,
            "discount_amount": round(discount_amount, 2),
            "final_total": round(final_total, 2),
        }


# =========================
# UI Layer
# =========================
class GroceryStoreApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Grocery Checkout System")
        self.root.geometry("960x650")
        self.root.minsize(900, 600)

        self.service = GroceryCheckoutService(PRODUCT_PRICES, DISCOUNT_RATES)
        self.cart: dict[str, int] = {}

        self._configure_style()
        self._build_ui()
        self._refresh_cart_view()

    def _configure_style(self):
        self.root.configure(bg="#f7f7f7")
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background="#f7f7f7", foreground="#222")
        style.configure("Section.TLabelframe", background="#ffffff")
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", background="#f7f7f7", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Treeview", font=("Consolas", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_ui(self):
        container = tk.Frame(self.root, bg="#f7f7f7")
        container.pack(fill="both", expand=True, padx=16, pady=16)

        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=3)
        container.grid_rowconfigure(1, weight=1)

        title = ttk.Label(container, text="Grocery Checkout System", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        subtitle = ttk.Label(
            container,
            text="Product selection, cart management, membership discounts, and receipt generation",
        )
        subtitle.grid(row=0, column=0, columnspan=2, sticky="w", pady=(36, 10))

        self._build_left_panel(container)
        self._build_right_panel(container)

    def _build_left_panel(self, parent):
        left = ttk.LabelFrame(parent, text="Add Items", style="Section.TLabelframe", padding=14)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left.grid_columnconfigure(1, weight=1)

        ttk.Label(left, text="Product").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.product_var = tk.StringVar()
        self.product_dropdown = ttk.Combobox(
            left,
            textvariable=self.product_var,
            values=sorted(PRODUCT_PRICES.keys()),
            state="readonly",
            width=24,
        )
        self.product_dropdown.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        self.product_dropdown.bind("<<ComboboxSelected>>", lambda _e: self._update_preview())

        ttk.Label(left, text="Quantity").grid(row=1, column=0, sticky="w", pady=(0, 8))
        self.quantity_var = tk.StringVar()
        self.quantity_entry = ttk.Entry(left, textvariable=self.quantity_var, width=12)
        self.quantity_entry.grid(row=1, column=1, sticky="ew", pady=(0, 8))
        self.quantity_entry.bind("<KeyRelease>", lambda _e: self._update_preview())

        ttk.Label(left, text="Membership").grid(row=2, column=0, sticky="w", pady=(0, 8))
        self.membership_var = tk.StringVar(value="Bronze")
        self.membership_dropdown = ttk.Combobox(
            left,
            textvariable=self.membership_var,
            values=list(DISCOUNT_RATES.keys()),
            state="readonly",
            width=24,
        )
        self.membership_dropdown.grid(row=2, column=1, sticky="ew", pady=(0, 8))
        self.membership_dropdown.bind("<<ComboboxSelected>>", lambda _e: self._update_totals())

        preview_frame = ttk.LabelFrame(left, text="Selection Preview", style="Section.TLabelframe", padding=10)
        preview_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 14))
        preview_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(preview_frame, text="Unit Price").grid(row=0, column=0, sticky="w")
        self.unit_price_var = tk.StringVar(value="$0.00")
        ttk.Label(preview_frame, textvariable=self.unit_price_var).grid(row=0, column=1, sticky="w")

        ttk.Label(preview_frame, text="Line Subtotal").grid(row=1, column=0, sticky="w")
        self.line_subtotal_var = tk.StringVar(value="$0.00")
        ttk.Label(preview_frame, textvariable=self.line_subtotal_var).grid(row=1, column=1, sticky="w")

        button_frame = tk.Frame(left, bg="#ffffff")
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.add_button = ttk.Button(button_frame, text="Add to Cart", command=self.add_to_cart)
        self.add_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.clear_selection_button = ttk.Button(button_frame, text="Clear Selection", command=self.clear_selection)
        self.clear_selection_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        totals_frame = ttk.LabelFrame(left, text="Cart Totals", style="Section.TLabelframe", padding=10)
        totals_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        totals_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(totals_frame, text="Items in Cart").grid(row=0, column=0, sticky="w")
        self.total_items_var = tk.StringVar(value="0")
        ttk.Label(totals_frame, textvariable=self.total_items_var).grid(row=0, column=1, sticky="w")

        ttk.Label(totals_frame, text="Subtotal").grid(row=1, column=0, sticky="w")
        self.subtotal_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_frame, textvariable=self.subtotal_var).grid(row=1, column=1, sticky="w")

        ttk.Label(totals_frame, text="Discount").grid(row=2, column=0, sticky="w")
        self.discount_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_frame, textvariable=self.discount_var).grid(row=2, column=1, sticky="w")

        ttk.Label(totals_frame, text="Final Total").grid(row=3, column=0, sticky="w")
        self.final_total_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_frame, textvariable=self.final_total_var).grid(row=3, column=1, sticky="w")

        checkout_buttons = tk.Frame(left, bg="#ffffff")
        checkout_buttons.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        checkout_buttons.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Button(checkout_buttons, text="Preview Bill", command=self.preview_bill).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(checkout_buttons, text="Checkout", command=self.checkout).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(checkout_buttons, text="Clear Cart", command=self.clear_cart).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

    def _build_right_panel(self, parent):
        right = ttk.LabelFrame(parent, text="Cart", style="Section.TLabelframe", padding=14)
        right.grid(row=1, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.cart_tree = ttk.Treeview(
            right,
            columns=("product", "quantity", "unit_price", "subtotal"),
            show="headings",
            height=18,
        )

        self.cart_tree.heading("product", text="Product")
        self.cart_tree.heading("quantity", text="Qty")
        self.cart_tree.heading("unit_price", text="Unit Price")
        self.cart_tree.heading("subtotal", text="Subtotal")

        self.cart_tree.column("product", width=180, anchor="center")
        self.cart_tree.column("quantity", width=80, anchor="center")
        self.cart_tree.column("unit_price", width=100, anchor="center")
        self.cart_tree.column("subtotal", width=100, anchor="center")

        self.cart_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        bottom = tk.Frame(right, bg="#ffffff")
        bottom.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        bottom.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(bottom, text="Remove Selected Item", command=self.remove_selected_item).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(bottom, text="Refresh Cart", command=self._refresh_cart_view).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def _update_preview(self):
        product_name = self.product_var.get().strip()
        quantity_text = self.quantity_var.get().strip()

        if not product_name or product_name not in PRODUCT_PRICES:
            self.unit_price_var.set("$0.00")
            self.line_subtotal_var.set("$0.00")
            return

        unit_price = PRODUCT_PRICES[product_name].price
        self.unit_price_var.set(f"${unit_price:.2f}")

        if quantity_text.isdigit() and int(quantity_text) > 0:
            subtotal = unit_price * int(quantity_text)
            self.line_subtotal_var.set(f"${subtotal:.2f}")
        else:
            self.line_subtotal_var.set("$0.00")

    def _refresh_cart_view(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        for product_name, quantity in sorted(self.cart.items()):
            unit_price = PRODUCT_PRICES[product_name].price
            subtotal = unit_price * quantity
            self.cart_tree.insert(
                "",
                "end",
                values=(
                    product_name,
                    quantity,
                    f"${unit_price:.2f}",
                    f"${subtotal:.2f}",
                ),
            )

        self._update_totals()

    def _update_totals(self):
        total_items = sum(self.cart.values())
        self.total_items_var.set(str(total_items))

        subtotal = 0.0
        for product_name, quantity in self.cart.items():
            subtotal += PRODUCT_PRICES[product_name].price * quantity

        membership = self.membership_var.get()
        discount_rate = DISCOUNT_RATES.get(membership, 0.0)
        discount_amount = subtotal * discount_rate
        final_total = subtotal - discount_amount

        self.subtotal_var.set(f"${subtotal:.2f}")
        self.discount_var.set(f"${discount_amount:.2f} ({discount_rate:.0%})")
        self.final_total_var.set(f"${final_total:.2f}")

    def add_to_cart(self):
        product_name = self.product_var.get().strip()
        quantity_text = self.quantity_var.get().strip()

        if not product_name:
            messagebox.showwarning("Missing Product", "Please select a product.")
            return

        try:
            quantity = self.service.validate_quantity(quantity_text)
        except ValueError as exc:
            messagebox.showerror("Invalid Quantity", str(exc))
            return

        self.cart[product_name] = self.cart.get(product_name, 0) + quantity
        self._refresh_cart_view()
        self.clear_selection()

    def remove_selected_item(self):
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select an item to remove.")
            return

        values = self.cart_tree.item(selection[0], "values")
        if not values:
            return

        product_name = values[0]
        if product_name in self.cart:
            del self.cart[product_name]

        self._refresh_cart_view()

    def preview_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items before previewing the bill.")
            return

        try:
            bill = self.service.calculate_bill(self.cart, self.membership_var.get())
        except ValueError as exc:
            messagebox.showerror("Billing Error", str(exc))
            return

        lines = ["GROCERY CHECKOUT SUMMARY", ""]
        for item in bill["line_items"]:
            lines.append(
                f"{item['product']}: ${item['unit_price']:.2f} x {item['quantity']} = ${item['subtotal']:.2f}"
            )

        lines.extend(
            [
                "",
                f"Subtotal: ${bill['bill_amount']:.2f}",
                f"Membership: {self.membership_var.get()}",
                f"Discount: ${bill['discount_amount']:.2f} ({bill['discount_rate']:.0%})",
                f"Final Total: ${bill['final_total']:.2f}",
            ]
        )

        messagebox.showinfo("Bill Preview", "\n".join(lines))

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items before checkout.")
            return

        try:
            bill = self.service.calculate_bill(self.cart, self.membership_var.get())
        except ValueError as exc:
            messagebox.showerror("Billing Error", str(exc))
            return

        lines = ["Confirm checkout?", ""]
        for item in bill["line_items"]:
            lines.append(
                f"{item['product']}: ${item['unit_price']:.2f} x {item['quantity']} = ${item['subtotal']:.2f}"
            )

        lines.extend(
            [
                "",
                f"Subtotal: ${bill['bill_amount']:.2f}",
                f"Discount: ${bill['discount_amount']:.2f}",
                f"Final Total: ${bill['final_total']:.2f}",
            ]
        )

        confirmed = messagebox.askyesno("Confirm Checkout", "\n".join(lines))
        if not confirmed:
            return

        receipt_lines = ["Receipt", "-" * 30]
        for item in bill["line_items"]:
            receipt_lines.append(
                f"{item['product']} x{item['quantity']}  @ ${item['unit_price']:.2f}  = ${item['subtotal']:.2f}"
            )

        receipt_lines.extend(
            [
                "-" * 30,
                f"Subtotal: ${bill['bill_amount']:.2f}",
                f"Membership: {self.membership_var.get()}",
                f"Discount: -${bill['discount_amount']:.2f}",
                f"Final Total: ${bill['final_total']:.2f}",
                "",
                "Thank you for shopping with us.",
            ]
        )

        messagebox.showinfo("Checkout Complete", "\n".join(receipt_lines))
        self.clear_cart()

    def clear_selection(self):
        self.product_var.set("")
        self.quantity_var.set("")
        self.unit_price_var.set("$0.00")
        self.line_subtotal_var.set("$0.00")

    def clear_cart(self):
        self.cart.clear()
        self._refresh_cart_view()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GroceryStoreApp(root)
    app.run()
