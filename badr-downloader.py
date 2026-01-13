import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import re
from urllib.parse import urljoin

class BookScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("متحمل كتب موقع الشيخ عبد الرزاق البدر")
        self.root.geometry("600x500")
        
        # تنسيق الواجهة
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 10))

        # الإطارات
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # عنوان ورابط البداية
        ttk.Label(main_frame, text="نطاق البحث (من معرف إلى معرف):").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.start_id = tk.IntVar(value=1)
        self.end_id = tk.IntVar(value=250)
        
        ttk.Label(main_frame, text="من:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.start_id, width=10).grid(row=1, column=0, padx=(30,0), sticky=tk.W)
        
        ttk.Label(main_frame, text="إلى:").grid(row=1, column=1, sticky=tk.W)
        ttk.Entry(main_frame, textvariable=self.end_id, width=10).grid(row=1, column=1, padx=(30,0), sticky=tk.W)

        # زر البدء
        self.start_btn = ttk.Button(main_frame, text="بدء التحميل المُنظم", command=self.start_thread)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=20, sticky=tk.NSEW)

        # شريط التقدم
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # منطقة عرض السجلات
        self.log_area = scrolledtext.ScrolledText(main_frame, height=15, font=("Consolas", 9))
        self.log_area.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, pady=5)

        self.base_url = "https://al-badr.net"
        self.is_running = False

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def sanitize_filename(self, filename):
        # إزالة الرموز غير المسموح بها في أسماء المجلدات والملفات
        return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

    def download_file(self, url, dest_path):
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(dest_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
        except Exception as e:
            self.log(f"خطأ في تحميل الملف {url}: {e}")
        return False

    def scrape_books(self):
        self.is_running = True
        start = self.start_id.get()
        end = self.end_id.get()
        total = end - start + 1
        
        self.progress["maximum"] = total
        self.progress["value"] = 0
        
        # إنشاء مجلد رئيسي للتحميلات
        main_dir = "Downloaded_Books"
        if not os.path.exists(main_dir):
            os.makedirs(main_dir)

        for i, book_id in enumerate(range(start, end + 1)):
            if not self.is_running: break
            
            page_url = f"{self.base_url}/ebook/{book_id}"
            self.log(f"--- فحص الصفحة: {book_id} ---")
            
            try:
                response = requests.get(page_url, timeout=20)
                if response.status_code != 200:
                    self.log(f"تخطي المعرف {book_id}: الصفحة غير موجودة.")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # استخراج البيانات
                title_tag = soup.find('h2', class_='post-title-single')
                if not title_tag:
                    self.log(f"تخطي {book_id}: لم يتم العثور على عنوان كتاب.")
                    continue
                
                title = self.sanitize_filename(title_tag.get_text())
                author_tag = soup.find('div', class_='author')
                author = author_tag.get_text().strip() if author_tag else "غير معروف"
                
                # استخراج صورة الغلاف
                img_div = soup.find('div', class_='kitabsingle')
                img_url = ""
                if img_div and img_div.find('img'):
                    img_src = img_div.find('img')['src']
                    img_url = urljoin(self.base_url, img_src)

                # استخراج رابط التحميل
                dl_link_tag = soup.find('a', class_='tahmil')
                pdf_url = ""
                if dl_link_tag:
                    pdf_url = urljoin(self.base_url, dl_link_tag['href'])

                if not pdf_url:
                    self.log(f"تنبيه: لم يتم العثور على ملف PDF للكتاب: {title}")
                    continue

                # إنشاء مجلد خاص بالكتاب
                book_folder = os.path.join(main_dir, f"{book_id}_{title}")
                if not os.path.exists(book_folder):
                    os.makedirs(book_folder)

                # 1. حفظ البيانات في ملف نصي
                with open(os.path.join(book_folder, "info.txt"), "w", encoding="utf-8") as f:
                    f.write(f"اسم الكتاب: {title}\n")
                    f.write(f"المؤلف: {author}\n")
                    f.write(f"رابط الصفحة: {page_url}\n")
                    f.write(f"رابط التحميل: {pdf_url}\n")

                # 2. تحميل صورة الغلاف
                if img_url:
                    self.log(f"جاري تحميل الغلاف: {title}...")
                    self.download_file(img_url, os.path.join(book_folder, "cover.jpg"))

                # 3. تحميل ملف الـ PDF
                self.log(f"جاري تحميل الكتاب PDF: {title}...")
                pdf_name = f"{title}.pdf"
                success = self.download_file(pdf_url, os.path.join(book_folder, pdf_name))
                
                if success:
                    self.log(f"تم تحميل الكتاب بنجاح في مجلد: {title}")
                else:
                    self.log(f"فشل تحميل ملف PDF للكتاب: {title}")

            except Exception as e:
                self.log(f"خطأ غير متوقع في المعرف {book_id}: {e}")
            
            self.progress["value"] = i + 1
            self.root.update_idletasks()

        self.log("✅ اكتملت العملية!")
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        messagebox.showinfo("تم", "اكتملت عملية تحميل وتنسيق الكتب بنجاح.")

    def start_thread(self):
        self.start_btn.config(state=tk.DISABLED)
        t = threading.Thread(target=self.scrape_books)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookScraperApp(root)
    root.mainloop()