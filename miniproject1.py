from datetime import datetime

class Transaction:

  def __init__(self, trans_type, amount, category, date=None):
    self.trans_type = trans_type  
    self.amount = float(amount)
    self.category = category      
    self.date = date if date else datetime.now().strftime("%Y-%m-%d")

  def __str__(self):
    return f"Tarix: {self.date} | Növ: {self.trans_type} | Kateqoriya: {self.category} | Məbləğ: {self.amount:.2f} AZN"


class BudgetManager:

  def __init__(self, filename="transactions.txt"):
    self.filename = filename
    self.__balance = 0.0  
    self.transactions = []
    self.load_from_file()

  @property
  def balance(self):
    
    return self.__balance

  def add_transaction(self, trans_type, amount, category):
    try:
     amount = float(amount)
    except ValueError:
      raise ValueError("Məbləğ daxil edərkən yalnız rəqəmlərdən istifadə edin!")
    
    if amount <= 0:
      raise ValueError("Məbləğ 0-dan böyük olmalıdır!")

    if not category.strip():
      raise ValueError("Kateqoriya boş ola bilməz!")

    
    if trans_type.lower() == "xərc" and amount > self.__balance:
      raise ValueError(
          f"Balansda kifayət qədər vəsait yoxdur! (Cari balans: {self.__balance:.2f} AZN)"
      )

    trans = Transaction(trans_type, amount, category)
    self.transactions.append(trans)

    if trans_type.lower() == "gəlir":
      self.__balance += amount
    else:
      self.__balance -= amount

    self.save_to_file()
    print(" Əməliyyat uğurla yerinə yetirildi!")

  def save_to_file(self):
    try:
      with open(self.filename, "w", encoding="utf-8") as f:
        for t in self.transactions:
          f.write(f"{t.trans_type},{t.amount},{t.category},{t.date}\n")
    except Exception as e:
      print(f"Fayla yazarkən xəta baş verdi: {e}")

  def load_from_file(self):
    try:
      with open(self.filename, "r", encoding="utf-8") as f:
        self.__balance = 0.0
        self.transactions = []
        for line in f:
          parts = line.strip().split(",")
          if len(parts) == 4:
            t_type, amount_str, category, date_str = parts
            amount = float(amount_str)
            trans = Transaction(t_type, amount, category, date_str)
            self.transactions.append(trans)

            if t_type.lower() == "gəlir":
              self.__balance += amount
            else:
              self.__balance -= amount
    except FileNotFoundError:
      pass
    except Exception as e:
      print(f"Fayldan oxuyarkən xəta baş verdi: {e}")

  def filter_by_date(self, start_date_str, end_date_str):
    
    try:
      start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
      end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

      filtered = []
      for t in self.transactions:
        t_date = datetime.strptime(t.date, "%Y-%m-%d")
        if start_date <= t_date <= end_date:
          filtered.append(t)

      if not filtered:
        print("\n Bu tarix aralığında heç bir əməliyyat tapılmadı.")
      else:
        print(f"\n--- Süzgəc Nəticələri ({start_date_str} - {end_date_str}) ---")
        for t in filtered:
          print(t)
    except ValueError:
      print(" Xəta: Tarix formatı yanlışdır! Zəhmət olmasa YYYY-MM-DD daxil edin.")

  def show_balance(self):
    
    print(f"\n Cari Balans: {self.__balance:.2f} AZN")

  def show_transactions(self):
    
    print(f"\n Bütün Əməliyyatlar ({len(self.transactions)} ədəd):")
    if not self.transactions:
      print("Hələ heç bir əməliyyat qeydə alınmayıb.")
    else:
      for t in self.transactions:
        print(t)

  def show_report(self):
    total_income = sum(t.amount for t in self.transactions if t.trans_type.lower() == "gəlir")
    total_expense = sum(t.amount for t in self.transactions if t.trans_type.lower() == "xərc")

    print("\n===== ÜMUMİ HESABAT =====")
    print(f" Ümumi gəlir : {total_income:.2f} AZN")
    print(f" Ümumi xərc  : {total_expense:.2f} AZN")
    print(f" Cari balans : {self.__balance:.2f} AZN")
    print("==========================")

  def show_monthly_report(self, year_month_str):
    try:
      datetime.strptime(year_month_str, "%Y-%m")
    except ValueError:
      print(" Xəta: Ay formatı yanlışdır! Zəhmət olmasa YYYY-MM daxil edin.")
      return

    monthly_trans = [t for t in self.transactions if t.date.startswith(year_month_str)]

    if not monthly_trans:
      print(f"\n {year_month_str} ayı üçün heç bir əməliyyat tapılmadı.")
      return

    total_income = sum(t.amount for t in monthly_trans if t.trans_type.lower() == "gəlir")
    total_expense = sum(t.amount for t in monthly_trans if t.trans_type.lower() == "xərc")

    print(f"\n===== {year_month_str} AYININ HESABATI =====")
    print(f" Əməliyyat sayı : {len(monthly_trans)}")
    print(f" Aylıq gəlir    : {total_income:.2f} AZN")
    print(f" Aylıq xərc     : {total_expense:.2f} AZN")
    print(f" Aylıq fərq     : {total_income - total_expense:.2f} AZN")
    print("=====================================")


def main():
  manager = BudgetManager()

  while True:
    print("\n==============================")
    print(" ŞƏXSI BÜDCƏ İDARƏETMƏ SISTEMI")
    print("==============================")
    print("1. Balansı göstər")
    print("2. Bütün əməliyyatları göstər")
    print("3. Gəlir əlavə et")
    print("4. Xərc əlavə et")
    print("5. Tarixə görə süzgəcdən keçir")
    print("6. Ümumi hesabat")
    print("7. Aylıq hesabat")
    print("8. Çıxış")

    choice = input("Seçiminizi daxil edin (1-8): ").strip()

    if choice == "1":
      manager.show_balance()

    elif choice == "2":
      manager.show_transactions()

    elif choice == "3":
      try:
        amount = (input("Gəlir məbləğini daxil edin (AZN): "))
        category = input("Kateqoriya: ")
        manager.add_transaction("Gəlir", amount, category)
      except ValueError as e:
        print(f" Xəta: {e}")

    elif choice == "4":
      try:
        amount = (input("Xərc məbləğini daxil edin (AZN): "))
        category = input("Kateqoriya: ")
        manager.add_transaction("Xərc", amount, category)
      except ValueError as e:
        print(f" Xəta: {e}")

    elif choice == "5":
      start = input("Başlanğıc tarixi (YYYY-MM-DD): ")
      end = input("Bitiş tarixi (YYYY-MM-DD): ")
      manager.filter_by_date(start, end)

    elif choice == "6":
      manager.show_report()

    elif choice == "7":
      year_month = input("Hesabatını görmək istədiyiniz ay (YYYY-MM, məs: 2024-01): ")
      manager.show_monthly_report(year_month)

    elif choice == "8":
      print("Proqramdan çixdiniz. Hələlik!")
      break
    else:
      print(" Yanlış seçim! Zəhmət olmasa 1 ilə 8 arasında bir rəqəm seçin.")


if __name__ == "__main__":
  main()