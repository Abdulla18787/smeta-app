import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform

# FPDF2 - Android bilan 100% muammosiz ishlaydigan sof Python PDF kutubxonasi
from fpdf import FPDF


class SmetaPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.cell(0, 8, "QURILISH VA REMONT ISHLARI SMETASI", ln=True, align='C')
        self.set_draw_color(2, 132, 199)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f"Sahifa {self.page_no()}", align='C')


class SmetaApp(App):
    def build(self):
        self.title = "Prorab Abdulla — Smeta & Avans"
        self.work_rows = []
        self.adv_rows = []

        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # Uy egasi
        client_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=8)
        client_box.add_widget(Label(text="Uy Egasi:", size_hint_x=0.3, bold=True, color=(0.1, 0.1, 0.1, 1)))
        self.client_input = TextInput(hint_text="Buyurtmachi F.I.Sh...", multiline=False, size_hint_x=0.7)
        client_box.add_widget(self.client_input)
        root.add_widget(client_box)

        # Skroll
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        # 1. Bajarilgan ishlar
        content.add_widget(Label(text="1. BAJARILGAN ISHLAR SMETASI", bold=True, size_hint_y=None, height=30, color=(0.01, 0.52, 0.78, 1)))
        
        w_btn_box = BoxLayout(size_hint_y=None, height=40, spacing=8)
        btn_add_work = Button(text="+ Ish Qo'shish", background_color=(0.06, 0.73, 0.5, 1))
        btn_add_work.bind(on_release=lambda x: self.add_work_row_ui())
        btn_del_work = Button(text="- O'chirish", background_color=(0.94, 0.27, 0.27, 1))
        btn_del_work.bind(on_release=lambda x: self.delete_work_row_ui())
        w_btn_box.add_widget(btn_add_work)
        w_btn_box.add_widget(btn_del_work)
        content.add_widget(w_btn_box)

        w_header = GridLayout(cols=5, size_hint_y=None, height=30)
        w_header.add_widget(Label(text="№", size_hint_x=0.1, bold=True, color=(0,0,0,1)))
        w_header.add_widget(Label(text="Ish Nomi", size_hint_x=0.4, bold=True, color=(0,0,0,1)))
        w_header.add_widget(Label(text="Birlik", size_hint_x=0.15, bold=True, color=(0,0,0,1)))
        w_header.add_widget(Label(text="Hajm", size_hint_x=0.15, bold=True, color=(0,0,0,1)))
        w_header.add_widget(Label(text="Narx", size_hint_x=0.2, bold=True, color=(0,0,0,1)))
        content.add_widget(w_header)

        self.works_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4)
        self.works_container.bind(minimum_height=self.works_container.setter('height'))
        content.add_widget(self.works_container)

        # 2. Avanslar
        content.add_widget(Label(text="2. OLINGAN AVANSLAR VA PULLAR", bold=True, size_hint_y=None, height=30, color=(0.01, 0.52, 0.78, 1)))

        a_btn_box = BoxLayout(size_hint_y=None, height=40, spacing=8)
        btn_add_adv = Button(text="+ Avans Qo'shish", background_color=(0.06, 0.73, 0.5, 1))
        btn_add_adv.bind(on_release=lambda x: self.add_adv_row_ui())
        btn_del_adv = Button(text="- O'chirish", background_color=(0.94, 0.27, 0.27, 1))
        btn_del_adv.bind(on_release=lambda x: self.delete_adv_row_ui())
        a_btn_box.add_widget(btn_add_adv)
        a_btn_box.add_widget(btn_del_adv)
        content.add_widget(a_btn_box)

        a_header = GridLayout(cols=4, size_hint_y=None, height=30)
        a_header.add_widget(Label(text="№", size_hint_x=0.1, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Sana", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Summa", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Izoh", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        content.add_widget(a_header)

        self.adv_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4)
        self.adv_container.bind(minimum_height=self.adv_container.setter('height'))
        content.add_widget(self.adv_container)

        scroll.add_widget(content)
        root.add_widget(scroll)

        # 3. Yakuniy hisob va tugmalar
        footer = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=4)
        self.lbl_calc_status = Label(text="Ishlar: 0 | Avans: 0 | Qoldiq: 0 So'm", bold=True, color=(0.1, 0.1, 0.1, 1))
        
        btn_calc = Button(text="Hisoblash", size_hint_y=None, height=40, background_color=(0.15, 0.39, 0.92, 1))
        btn_calc.bind(on_release=lambda x: self.update_calculations())

        btn_pdf = Button(text="PDF Saqlash", size_hint_y=None, height=45, background_color=(0.02, 0.47, 0.34, 1), bold=True)
        btn_pdf.bind(on_release=lambda x: self.generate_pdf())

        footer.add_widget(self.lbl_calc_status)
        footer.add_widget(btn_calc)
        footer.add_widget(btn_pdf)
        root.add_widget(footer)

        for _ in range(3):
            self.add_work_row_ui()
        for _ in range(2):
            self.add_adv_row_ui()

        Window.clearcolor = (0.95, 0.96, 0.98, 1)
        self.request_android_permissions()
        return root

    def request_android_permissions(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ])
            except Exception:
                pass

    def add_work_row_ui(self):
        idx = len(self.work_rows) + 1
        row = GridLayout(cols=5, size_hint_y=None, height=40, spacing=3)
        lbl_num = Label(text=str(idx), size_hint_x=0.1, color=(0,0,0,1))
        txt_name = TextInput(hint_text="Ish nomi", size_hint_x=0.4, multiline=False)
        txt_unit = TextInput(hint_text="m2", size_hint_x=0.15, multiline=False)
        txt_qty = TextInput(hint_text="0", size_hint_x=0.15, multiline=False, input_filter='float')
        txt_price = TextInput(hint_text="0", size_hint_x=0.2, multiline=False, input_filter='float')

        row.add_widget(lbl_num)
        row.add_widget(txt_name)
        row.add_widget(txt_unit)
        row.add_widget(txt_qty)
        row.add_widget(txt_price)

        self.works_container.add_widget(row)
        self.work_rows.append((lbl_num, txt_name, txt_unit, txt_qty, txt_price))

    def delete_work_row_ui(self):
        if self.work_rows:
            last = self.work_rows.pop()
            self.works_container.remove_widget(last[0].parent)
            self.update_calculations()

    def add_adv_row_ui(self):
        idx = len(self.adv_rows) + 1
        row = GridLayout(cols=4, size_hint_y=None, height=40, spacing=3)
        lbl_num = Label(text=str(idx), size_hint_x=0.1, color=(0,0,0,1))
        txt_date = TextInput(text=datetime.now().strftime("%d.%m.%Y"), size_hint_x=0.3, multiline=False)
        txt_sum = TextInput(hint_text="Summa", size_hint_x=0.3, multiline=False, input_filter='float')
        txt_note = TextInput(hint_text="Izoh...", size_hint_x=0.3, multiline=False)

        row.add_widget(lbl_num)
        row.add_widget(txt_date)
        row.add_widget(txt_sum)
        row.add_widget(txt_note)

        self.adv_container.add_widget(row)
        self.adv_rows.append((lbl_num, txt_date, txt_sum, txt_note))

    def delete_adv_row_ui(self):
        if self.adv_rows:
            last = self.adv_rows.pop()
            self.adv_container.remove_widget(last[0].parent)
            self.update_calculations()

    def update_calculations(self):
        total_works = 0.0
        for _, _, _, q, p in self.work_rows:
            try:
                qv = float(q.text.replace(" ", "").replace(",", ".")) if q.text else 0.0
                pv = float(p.text.replace(" ", "").replace(",", ".")) if p.text else 0.0
                total_works += qv * pv
            except ValueError:
                pass

        total_adv = 0.0
        for _, _, s, _ in self.adv_rows:
            try:
                sv = float(s.text.replace(" ", "").replace(",", ".")) if s.text else 0.0
                total_adv += sv
            except ValueError:
                pass

        balance = total_works - total_adv
        self.lbl_calc_status.text = f"Ishlar: {total_works:,.0f} | Avans: {total_adv:,.0f} | Qoldiq: {balance:,.0f} So'm".replace(",", " ")
        return total_works, total_adv, balance

    def show_popup(self, title, msg):
        pop = Popup(title=title, content=Label(text=msg), size_hint=(0.85, 0.4))
        pop.open()

    def get_output_dir(self):
        # Faylni xavfsiz va kafolatli saqlash papkasi
        if platform == 'android':
            from android.storage import app_storage_path
            path = app_storage_path()
            return path
        return os.path.expanduser("~")

    def generate_pdf(self):
        client = self.client_input.text.strip()
        if not client:
            self.show_popup("Xatolik", "Iltimos, Uy Egasining ismini kiriting!")
            return

        total_w, total_a, bal = self.update_calculations()
        out_dir = self.get_output_dir()
        file_name = f"Smeta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(out_dir, file_name)

        try:
            pdf = SmetaPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Metadata
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(100, 6, f"Prorab: Prorab Abdulla", ln=False)
            pdf.cell(90, 6, f"Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align='R')
            pdf.cell(100, 6, f"Uy Egasi: {client}", ln=False)
            pdf.cell(90, 6, "Turi: Remont Smetasi", ln=True, align='R')
            pdf.ln(4)

            # 1. Ishlar jadvali
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(1, 82, 122)
            pdf.cell(0, 7, "1. BAJARILGAN ISHLAR:", ln=True)
            pdf.set_text_color(0, 0, 0)

            # Sarlavha
            pdf.set_fill_color(2, 132, 199)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(10, 7, "No", 1, 0, 'C', fill=True)
            pdf.cell(75, 7, "Ish Nomi", 1, 0, 'L', fill=True)
            pdf.cell(25, 7, "Birlik", 1, 0, 'C', fill=True)
            pdf.cell(25, 7, "Hajm", 1, 0, 'C', fill=True)
            pdf.cell(25, 7, "Narx", 1, 0, 'R', fill=True)
            pdf.cell(30, 7, "Jami", 1, 1, 'R', fill=True)

            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', '', 8.5)
            w_idx = 0
            for _, nw, uw, qw, pw in self.work_rows:
                nm = nw.text.strip()
                if nm:
                    w_idx += 1
                    u = uw.text.strip()
                    qv = float(qw.text.replace(" ", "").replace(",", ".")) if qw.text else 0.0
                    pv = float(pw.text.replace(" ", "").replace(",", ".")) if pw.text else 0.0
                    tot = qv * pv
                    pdf.cell(10, 6, str(w_idx), 1, 0, 'C')
                    pdf.cell(75, 6, nm[:35], 1, 0, 'L')
                    pdf.cell(25, 6, u[:10], 1, 0, 'C')
                    pdf.cell(25, 6, str(qv), 1, 0, 'C')
                    pdf.cell(25, 6, f"{pv:,.0f}".replace(",", " "), 1, 0, 'R')
                    pdf.cell(30, 6, f"{tot:,.0f}".replace(",", " "), 1, 1, 'R')

            pdf.ln(4)

            # 2. Avanslar jadvali
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(1, 82, 122)
            pdf.cell(0, 7, "2. OLINGAN AVANSLAR VA PULLAR:", ln=True)
            pdf.set_text_color(0, 0, 0)

            pdf.set_fill_color(71, 85, 105)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(10, 7, "No", 1, 0, 'C', fill=True)
            pdf.cell(35, 7, "Sana", 1, 0, 'C', fill=True)
            pdf.cell(45, 7, "Summa (So'm)", 1, 0, 'R', fill=True)
            pdf.cell(100, 7, "Izoh", 1, 1, 'L', fill=True)

            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', '', 8.5)
            a_idx = 0
            for _, dw, sw, iw in self.adv_rows:
                st = sw.text.strip()
                if st and st != "0":
                    a_idx += 1
                    val = float(st.replace(" ", "").replace(",", "."))
                    pdf.cell(10, 6, str(a_idx), 1, 0, 'C')
                    pdf.cell(35, 6, dw.text.strip(), 1, 0, 'C')
                    pdf.cell(45, 6, f"{val:,.0f}".replace(",", " "), 1, 0, 'R')
                    pdf.cell(100, 6, (iw.text.strip() or "Qo'ldan berildi")[:45], 1, 1, 'L')

            pdf.ln(5)

            # 3. Yakuniy qoldiq
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(120, 7, "Jami ishlar qiymati:", 1, 0, 'L')
            pdf.cell(70, 7, f"{total_w:,.0f} So'm".replace(",", " "), 1, 1, 'R')
            pdf.cell(120, 7, "Olingan jami avans:", 1, 0, 'L')
            pdf.cell(70, 7, f"- {total_a:,.0f} So'm".replace(",", " "), 1, 1, 'R')
            
            b_text = "TO'LANISHI KERAK (QOLDIQ):" if bal >= 0 else "ORTIQCHA TO'LOV:"
            pdf.cell(120, 8, b_text, 1, 0, 'L')
            pdf.cell(70, 8, f"{abs(bal):,.0f} So'm".replace(",", " "), 1, 1, 'R')

            pdf.output(file_path)
            self.show_popup("Muvaffaqiyat", f"PDF tayyor!\nSaqlandi:\n{file_name}")

        except Exception as e:
            self.show_popup("Xatolik", f"PDF xatosi: {str(e)}")


if __name__ == '__main__':
    SmetaApp().run()
