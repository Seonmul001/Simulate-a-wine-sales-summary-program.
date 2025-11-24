import tkinter as tk
from tkinter import ttk, messagebox

# ------------------------------
# เก็บข้อมูลบิลทั้งหมด
# ------------------------------
bills = []
current_bill = []

# เก็บชื่อไวน์และปีที่เคยกรอกไว้
wine_names = set()
wine_years = set()

# ------------------------------
# เพิ่มไวน์เข้าในบิล
# ------------------------------
def add_wine():
    name = entry_name.get().strip()
    year = entry_year.get().strip()
    price = entry_price.get()
    qty = entry_qty.get()
    status = promo_status.get()

    if not (name and year and price and qty):
        messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        return

    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        messagebox.showerror("ผิดพลาด", "กรุณากรอกราคาหรือจำนวนเป็นตัวเลข")
        return

    current_bill.append({
        "ชื่อไวน์": name,
        "ปี": year,
        "จำนวน": qty,
        "ราคาต่อขวด": price,
        "ประเภท": status
    })

    tree.insert("", "end", values=(name, year, qty, price, status))

    # บันทึกชื่อไวน์และปีไว้ในรายการ
    wine_names.add(name)
    wine_years.add(year)

    # อัปเดตรายการใน Combobox ให้เลือกได้ภายหลัง
    entry_name["values"] = sorted(wine_names)
    entry_year["values"] = sorted(wine_years)

    # ล้างช่องกรอก
    entry_name.set("")
    entry_year.set("")
    entry_price.delete(0, tk.END)
    entry_qty.delete(0, tk.END)

# ------------------------------
# ปิดบิล (รวมยอด)
# ------------------------------
def close_bill():
    if not current_bill:
        messagebox.showinfo("ไม่มีข้อมูล", "ยังไม่มีไวน์ในบิล")
        return
    bills.append(current_bill.copy())
    tree.delete(*tree.get_children())
    current_bill.clear()
    messagebox.showinfo("สำเร็จ", f"บันทึกบิลที่ {len(bills)} เรียบร้อย")

# ------------------------------
# สรุปยอดทั้งหมด
# ------------------------------
def show_summary():
    if not bills:
        messagebox.showinfo("ยังไม่มีข้อมูล", "ยังไม่มีบิลที่ถูกบันทึก")
        return

    summary_text = ""
    total_amount = 0
    bill_no = 1

    for bill in bills:
        summary_text += f"\n=== บิลที่ {bill_no} ===\n"
        bill_no += 1
        for item in bill:
            name = item['ชื่อไวน์']
            year = item['ปี']
            qty = item['จำนวน']
            price = item['ราคาต่อขวด']
            status = item['ประเภท']

            if status == "ราคาโปร":
                promo_price = 999 / 3
                item_total = promo_price * qty
            else:
                item_total = price * qty

            total_amount += item_total
            summary_text += f"{name} ({year}) - {qty} ขวด - {status} - รวม {item_total:.2f} บาท\n"

    summary_text += f"\n💰 ยอดขายรวมทั้งหมด: {total_amount:.2f} บาท"

    summary_window = tk.Toplevel(root)
    summary_window.title("สรุปยอดขายทั้งหมด")
    text = tk.Text(summary_window, wrap="word", width=70, height=25)
    text.pack(padx=10, pady=10)
    text.insert("1.0", summary_text)
    text.config(state="disabled")

# ------------------------------
# ส่วน UI หลัก
# ------------------------------
root = tk.Tk()
root.title("โปรแกรมบันทึกยอดขายไวน์")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# ฟอร์มกรอกข้อมูล
ttk.Label(frame, text="ชื่อไวน์:").grid(row=0, column=0)
entry_name = ttk.Combobox(frame, width=20, values=[])
entry_name.grid(row=0, column=1)

ttk.Label(frame, text="ปี:").grid(row=0, column=2)
entry_year = ttk.Combobox(frame, width=10, values=[])
entry_year.grid(row=0, column=3)

ttk.Label(frame, text="ราคาปกติ:").grid(row=1, column=0)
entry_price = ttk.Entry(frame, width=10)
entry_price.grid(row=1, column=1)

ttk.Label(frame, text="จำนวน:").grid(row=1, column=2)
entry_qty = ttk.Entry(frame, width=10)
entry_qty.grid(row=1, column=3)

ttk.Label(frame, text="ประเภท:").grid(row=2, column=0)
promo_status = ttk.Combobox(frame, values=["ราคาปกติ", "ราคาโปร"], width=17)
promo_status.current(0)
promo_status.grid(row=2, column=1)

ttk.Button(frame, text="เพิ่มไวน์ในบิล", command=add_wine).grid(row=2, column=3, sticky="e")

# ตารางแสดงข้อมูลไวน์ในบิล
columns = ("ชื่อไวน์", "ปี", "จำนวน", "ราคาต่อขวด", "ประเภท")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=3, column=0, columnspan=4, pady=10)

# ปุ่มสรุป/ปิดบิล
ttk.Button(frame, text="ปิดบิล", command=close_bill).grid(row=4, column=0, pady=10)
ttk.Button(frame, text="สรุปยอดทั้งหมด", command=show_summary).grid(row=4, column=3, pady=10, sticky="e")

root.mainloop()
