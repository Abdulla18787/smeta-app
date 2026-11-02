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

# ReportLab PDF kutubxonasi
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


class SmetaApp(App):
    def build(self):
        self.title = "Prorab Abdulla — Smeta & Avans"
        self.work_rows = []
        self.adv_rows = []

        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # 1. Bosh qism: Uy egasi nomi
        client_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=8)
        client_box.add_widget(Label(text="Uy Egasi:", size_hint_x=0.3, bold=True, color=(0.1, 0.1, 0.1, 1)))
        self.client_input = TextInput(hint_text="Buyurtmachi F.I.Sh...", multiline=False, size_hint_x=0.7)
        client_box.add_widget(self.client_input)
        root.add_widget(client_box)

        # Skroll maydoni
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        # --- BO'LIM 1: BAJARILGAN ISHLAR ---
        content.add_widget(Label(text="1. BAJARILGAN ISHLAR SMETASI", bold=True, size_hint_y=None, height=30, color=(0.01, 0.52, 0.78, 1)))
        
        # Tugmalar
        w_btn_box = BoxLayout(size_hint_y=None, height=40, spacing=8)
        btn_add_work = Button(text="+ Ish Qo'shish", background_color=(0.06, 0.73, 0.5, 1))
        btn_add_work.bind(on_release=lambda x: self.add_work_row_ui())
        btn_del_work = Button(text="- Oxirgi Qatorni O'chirish", background_color=(0.94, 0.27, 0.27, 1))
        btn_del_work.bind(on_release=lambda x: self.delete_work_row_ui())
        w_btn_box.add_widget(btn_add_work)
        w_btn_box.add_widget(btn_del_work)
        content.add_widget(w_btn_box)

        # Jadval bosh sarlavhasi
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

        # --- BO'LIM 2: OLINGAN AVANSLAR ---
        content.add_widget(Label(text="2. OLINGAN AVANSLAR VA PULLAR", bold=True, size_hint_y=None, height=30, color=(0.01, 0.52, 0.78, 1)))

        a_btn_box = BoxLayout(size_hint_y=None, height=40, spacing=8)
        btn_add_adv = Button(text="+ Avans Qo'shish", background_color=(0.06, 0.73, 0.5, 1))
        btn_add_adv.bind(on_release=lambda x: self.add_adv_row_ui())
        btn_del_adv = Button(text="- Oxirgi Avansni O'chirish", background_color=(0.94, 0.27, 0.27, 1))
        btn_del_adv.bind(on_release=lambda x: self.delete_adv_row_ui())
        a_btn_box.add_widget(btn_add_adv)
        a_btn_box.add_widget(btn_del_adv)
        content.add_widget(a_btn_box)

        a_header = GridLayout(cols=4, size_hint_y=None, height=30)
        a_header.add_widget(Label(text="№", size_hint_x=0.1, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Sana", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Summa (So'm)", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        a_header.add_widget(Label(text="Izoh", size_hint_x=0.3, bold=True, color=(0,0,0,1)))
        content.add_widget(a_header)

        self.adv_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=4)
        self.adv_container.bind(minimum_height=self.adv_container.setter('height'))
        content.add_widget(self.adv_container)

        scroll.add_widget(content)
        root.add_widget(scroll)

        # --- BO'LIM 3: YAKUNIY HISOB VA TUGMA ---
        footer = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=4)
        self.lbl_calc_status = Label(text="Ishlar: 0 | Avans: 0 | Qoldiq: 0 So'm", bold=True, color=(0.1, 0.1, 0.1, 1))
        
        btn_calc = Button(text="🔄 Hisoblash", size_hint_y=None, height=40, background_color=(0.15, 0.39, 0.92, 1))
        btn_calc.bind(on_release=lambda x: self.update_calculations())

        btn_pdf = Button(text="📄 PDF Hisobot Yaratish (Yuklanmalar papkasiga)", size_hint_y=None, height=45, background_color=(0.02, 0.47, 0.34, 1), bold=True)
        btn_pdf.bind(on_release=lambda x: self.generate_pdf())

        footer.add_widget(self.lbl_calc_status)
        footer.add_widget(btn_calc)
        footer.add_widget(btn_pdf)
        root.add_widget(footer)

        # Dastlabki bo'sh qatorlar
        for _ in range(3):
            self.add_work_row_ui()
        for _ in range(2):
            self.add_adv_row_ui()

        # Oyna fonini ochiq rangga sozlash
        Window.clearcolor = (0.95, 0.96, 0.98, 1)

        # Android ruxsatlarini tekshirish
        self.request_android_permissions()

        return root

    def request_android_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

    # --- Qator boshqaruvlari ---
    def add_work_row_ui(self):
        idx = len(self.work_rows) + 1
        row = GridLayout(cols=5, size_hint_y=None, height=40, spacing=3)
        lbl_num = Label(text=str(idx), size_hint_x=0.1, color=(0,0,0,1))
        txt_name = TextInput(hint_text="Ish nomi", size_hint_x=0.4, multiline=False)
        txt_unit = TextInput(hint_text="kv.m", size_hint_x=0.15, multiline=False)
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
            # Ota vidjetni topib tozalash
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
        # Android 10+ tizimida Download papkasini aniqlash
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dl_path = os.path.join(primary_external_storage_path(), 'Download')
            if os.path.exists(dl_path):
                return dl_path
            return primary_external_storage_path()
        return os.path.expanduser("~")

    def generate_pdf(self):
        client = self.client_input.text.strip()
        if not client:
            self.show_popup("Xatolik", "Iltimos, Uy Egasining ismini kiriting!")
            return

        total_w, total_a, bal = self.update_calculations()
        out_dir = self.get_output_dir()
        file_name = f"Smeta_{client.replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.pdf"
        file_path = os.path.join(out_dir, file_name)

        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=24, leftMargin=24, topMargin=24, bottomMargin=24)
            styles = getSampleStyleSheet()

            t_style = ParagraphStyle('T', parent=styles['Heading1'], fontSize=15, leading=19, alignment=1, textColor=colors.HexColor('#0f172a'))
            sec_style = ParagraphStyle('S', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#0369a1'), spaceBefore=8, spaceAfter=4)
            th_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=9, textColor=colors.white, fontName='Helvetica-Bold', alignment=1)
            td_style = ParagraphStyle('TD', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=colors.HexColor('#1e293b'))
            meta_style = ParagraphStyle('M', parent=styles['Normal'], fontSize=9, leading=13)

            elements = []
            elements.append(Paragraph("<b>QURILISH VA REMONT ISHLARI BO'YICHA SMETA VA AVANS HISOBI</b>", t_style))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=8))

            meta_data = [
                [Paragraph("<b>Prorab:</b> Prorab Abdulla", meta_style), Paragraph(f"<b>Sana:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", meta_style)],
                [Paragraph(f"<b>Uy Egasi:</b> {client}", meta_style), Paragraph("<b>Turi:</b> Padkluch Remont", meta_style)]
            ]
            t_meta = Table(meta_data, colWidths=[280, 260])
            elements.append(t_meta)
            elements.append(Spacer(1, 8))

            # 1. Ishlar jadvali
            elements.append(Paragraph("<b>1. BAJARILGAN ISHLAR:</b>", sec_style))
            w_table_data = [[
                Paragraph("<b>№</b>", th_style), Paragraph("<b>Ish Nomi</b>", th_style),
                Paragraph("<b>Birlik</b>", th_style), Paragraph("<b>Hajm</b>", th_style),
                Paragraph("<b>Narx</b>", th_style), Paragraph("<b>Jami</b>", th_style)
            ]]

            w_idx = 0
            for _, name_w, unit_w, q_w, p_w in self.work_rows:
                nm = name_w.text.strip()
                if nm:
                    w_idx += 1
                    u = unit_w.text.strip()
                    qv = float(q_w.text.replace(" ", "").replace(",", ".")) if q_w.text else 0.0
                    pv = float(p_w.text.replace(" ", "").replace(",", ".")) if p_w.text else 0.0
                    row_tot = qv * pv
                    w_table_data.append([
                        Paragraph(str(w_idx), td_style), Paragraph(nm, td_style),
                        Paragraph(u, td_style), Paragraph(str(qv), td_style),
                        Paragraph(f"{pv:,.0f}".replace(",", " "), td_style),
                        Paragraph(f"{row_tot:,.0f}".replace(",", " "), td_style)
                    ])

            tw = Table(w_table_data, colWidths=[24, 230, 60, 50, 85, 90])
            tw.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(tw)
            elements.append(Spacer(1, 8))

            # 2. Avanslar jadvali
            elements.append(Paragraph("<b>2. OLINGAN AVANSLAR VA PULLAR:</b>", sec_style))
            a_table_data = [[
                Paragraph("<b>№</b>", th_style), Paragraph("<b>Sana</b>", th_style),
                Paragraph("<b>Summa (So'm)</b>", th_style), Paragraph("<b>Izoh</b>", th_style)
            ]]

            a_idx = 0
            for _, dt_w, s_w, note_w in self.adv_rows:
                st = s_w.text.strip()
                if st and st != "0":
                    a_idx += 1
                    val = float(st.replace(" ", "").replace(",", "."))
                    a_table_data.append([
                        Paragraph(str(a_idx), td_style), Paragraph(dt_w.text.strip(), td_style),
                        Paragraph(f"{val:,.0f}".replace(",", " "), td_style),
                        Paragraph(note_w.text.strip() or "Qo'ldan berildi", td_style)
                    ])

            ta = Table(a_table_data, colWidths=[24, 110, 125, 280])
            ta.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(ta)
            elements.append(Spacer(1, 10))

            # 3. Yakuniy moliyaviy blok
            b_color = "#047857" if bal >= 0 else "#b91c1c"
            b_label = "TO'LANISHI KERAK (QOLDIQ):" if bal >= 0 else "ORTIQCHA TO'LOV:"
            summary_data = [
                [Paragraph("<b>Jami ishlar:</b>", meta_style), Paragraph(f"<b>{total_w:,.0f} So'm</b>".replace(",", " "), td_style)],
                [Paragraph("<b>Olingan avans:</b>", meta_style), Paragraph(f"<b>- {total_a:,.0f} So'm</b>".replace(",", " "), td_style)],
                [Paragraph(f"<b><font color='{b_color}'>{b_label}</font></b>", meta_style),
                 Paragraph(f"<b><font size=10 color='{b_color}'>{abs(bal):,.0f} So'm</font></b>".replace(",", " "), td_style)]
            ]
            ts = Table(summary_data, colWidths=[339, 200])
            ts.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(ts)
            elements.append(Spacer(1, 25))

            # Imzolar
            sig_data = [
                [Paragraph("<b>Prorab:</b> Prorab Abdulla", meta_style), Paragraph(f"<b>Uy Egasi:</b> {client}", meta_style)],
                [Paragraph("Imzo: ________________", meta_style), Paragraph("Imzo: ________________", meta_style)]
            ]
            elements.append(Table(sig_data, colWidths=[270, 269]))

            doc.build(elements)
            self.show_popup("Muvaffaqiyat", f"PDF tayyor!\nSaqlandi:\n{file_path}")

        except Exception as e:
            self.show_popup("Xatolik", f"PDF yaratib bo'lmadi:\n{str(e)}")


if __name__ == '__main__':
    SmetaApp().run()