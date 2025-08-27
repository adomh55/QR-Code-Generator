# Import necessary CustomTkinter and other libraries
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk 
import os
import re
import webbrowser

# Set the appearance mode and default color theme for the application
ctk.set_appearance_mode("System")  # Supports "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # Supports "blue", "green", "dark-blue"

class QRCodeGenerator(ctk.CTk):
    """
    Main application class for the personal QR Code Generator.
    """
    def __init__(self):
        super().__init__()
        
        # --- Configure the main window ---
        self.title("🔲 Personal QR Code Generator")
        self.geometry("800x900")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Variables
        self.qr_image = None
        self.custom_fields = {} # A dictionary to store custom field widgets.
        self.current_colors = {"fill": "black", "back": "#f0f0f0"}
        
        # Create GUI
        self.create_widgets()
        
        # Center window after creating widgets
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        """Main function to build the UI layout using CustomTkinter components"""
        
        # Use a CTkScrollableFrame for the main content area
        scrollable_frame = ctk.CTkScrollableFrame(self)
        scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Bind the mouse wheel to the scrollable frame for universal scrolling
        scrollable_frame.bind_all('<MouseWheel>', lambda e: scrollable_frame._on_mousewheel(e))

        # Title
        title_label = ctk.CTkLabel(scrollable_frame, 
                                   text="🔲 Personal QR Code Generator", 
                                   font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Basic Information Section
        self.create_basic_info_section(scrollable_frame)
        
        # Separator
        ctk.CTkLabel(scrollable_frame, text="─" * 40).pack(fill='x', pady=10)
        
        # Contact Information Section
        self.create_contact_section(scrollable_frame)
        
        # Separator
        ctk.CTkLabel(scrollable_frame, text="─" * 40).pack(fill='x', pady=10)
        
        # Social Media Section
        self.create_social_section(scrollable_frame)
        
        # Separator
        ctk.CTkLabel(scrollable_frame, text="─" * 40).pack(fill='x', pady=10)
        
        # Custom Fields Section
        self.create_custom_fields_section(scrollable_frame)
        
        # Separator
        ctk.CTkLabel(scrollable_frame, text="─" * 40).pack(fill='x', pady=10)
        
        # QR Code Options Section
        self.create_qr_options_section(scrollable_frame)
        
        # Separator
        ctk.CTkLabel(scrollable_frame, text="─" * 40).pack(fill='x', pady=10)
        
        # Generate Button
        generate_btn = ctk.CTkButton(scrollable_frame, 
                                     text="🚀 Generate QR Code", 
                                     command=self.generate_qr_code,
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     fg_color="#3498db", hover_color="#2980b9")
        generate_btn.pack(pady=20, ipadx=20, ipady=5)
        
        # QR Code Display
        self.qr_display_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        self.qr_display_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        self.qr_label = ctk.CTkLabel(self.qr_display_frame, text="QR Code will appear here", font=ctk.CTkFont(size=12))
        self.qr_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.qr_display_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)
        
        self.save_btn = ctk.CTkButton(buttons_frame, text="💾 Save QR Code", 
                                     command=self.save_qr_code, state="disabled")
        self.save_btn.pack(side="left", padx=5)
        
        self.preview_btn = ctk.CTkButton(buttons_frame, text="👁️ Preview", 
                                         command=self.preview_qr_code, state="disabled")
        self.preview_btn.pack(side="left", padx=5)

        # Footer Section
        self.create_footer_section(scrollable_frame)

    def create_basic_info_section(self, parent):
        """Create a section for personal details"""
        basic_frame = ctk.CTkFrame(parent, corner_radius=10)
        basic_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(basic_frame, text="📋 Basic Information", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        
        # Name (Required)
        ctk.CTkLabel(basic_frame, text="Full Name *", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.name_entry = ctk.CTkEntry(basic_frame, placeholder_text="Enter your full name")
        self.name_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # Job Title
        ctk.CTkLabel(basic_frame, text="Job Title", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.job_title_entry = ctk.CTkEntry(basic_frame, placeholder_text="Enter your job title")
        self.job_title_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # Company
        ctk.CTkLabel(basic_frame, text="Company", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.company_entry = ctk.CTkEntry(basic_frame, placeholder_text="Enter company name")
        self.company_entry.pack(fill="x", pady=(5, 10), padx=10)

    def create_contact_section(self, parent):
        """Create a section for contact information"""
        contact_frame = ctk.CTkFrame(parent, corner_radius=10)
        contact_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(contact_frame, text="📞 Contact Information", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        
        # Phone
        ctk.CTkLabel(contact_frame, text="Phone Number", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.phone_entry = ctk.CTkEntry(contact_frame, placeholder_text="Enter phone number")
        self.phone_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # WhatsApp
        whatsapp_frame = ctk.CTkFrame(contact_frame, fg_color="transparent")
        whatsapp_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        ctk.CTkLabel(whatsapp_frame, text="WhatsApp Number", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        whatsapp_input_frame = ctk.CTkFrame(whatsapp_frame, fg_color="transparent")
        whatsapp_input_frame.pack(fill="x", pady=(5, 0))
        
        self.whatsapp_entry = ctk.CTkEntry(whatsapp_input_frame, placeholder_text="Enter WhatsApp number")
        self.whatsapp_entry.pack(side="left", fill="x", expand=True)
        
        self.use_same_phone = ctk.CTkButton(whatsapp_input_frame, text="Same as Phone", 
                                             command=self.copy_phone_to_whatsapp,
                                             fg_color="gray", hover_color="darkgray")
        self.use_same_phone.pack(side="right", padx=(10, 0))
        
        # Email
        ctk.CTkLabel(contact_frame, text="Email", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.email_entry = ctk.CTkEntry(contact_frame, placeholder_text="Enter email address")
        self.email_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # Address
        ctk.CTkLabel(contact_frame, text="Address", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.address_text = ctk.CTkTextbox(contact_frame, height=3, activate_scrollbars=False)
        self.address_text.pack(fill="x", pady=(5, 10), padx=10)

    def create_social_section(self, parent):
        """Create a section for social media links"""
        social_frame = ctk.CTkFrame(parent, corner_radius=10)
        social_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(social_frame, text="🌐 Social Media & Web", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        
        # Website
        ctk.CTkLabel(social_frame, text="Website", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.website_entry = ctk.CTkEntry(social_frame, placeholder_text="https://example.com")
        self.website_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # Facebook
        ctk.CTkLabel(social_frame, text="Facebook", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.facebook_entry = ctk.CTkEntry(social_frame, placeholder_text="username or full URL")
        self.facebook_entry.pack(fill="x", pady=(5, 10), padx=10)
        
        # LinkedIn
        ctk.CTkLabel(social_frame, text="LinkedIn", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        self.linkedin_entry = ctk.CTkEntry(social_frame, placeholder_text="username or full URL")
        self.linkedin_entry.pack(fill="x", pady=(5, 10), padx=10)

    def create_custom_fields_section(self, parent):
        """Create a section for adding custom data fields"""
        self.custom_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.custom_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(self.custom_frame, text="➕ Custom Fields", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        
        add_custom_btn = ctk.CTkButton(self.custom_frame, text="+ Add Custom Field", 
                                        command=self.add_custom_field,
                                        font=ctk.CTkFont(size=12),
                                        fg_color="#2ecc71", hover_color="#27ae60")
        add_custom_btn.pack(pady=5, padx=10)
        
        self.custom_fields_container = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
        self.custom_fields_container.pack(fill="x", pady=5, padx=10, ipady=10) # Added ipady

    def create_qr_options_section(self, parent):
        """Create a section for QR code format and colors"""
        options_frame = ctk.CTkFrame(parent, corner_radius=10)
        options_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(options_frame, text="🎨 QR Code Options", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        
        # Format selection
        format_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        format_frame.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkLabel(format_frame, text="Format:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        self.format_var = tk.StringVar(value="vcard")
        
        vcard_radio = ctk.CTkRadioButton(format_frame, text="VCard (Contact)", 
                                         variable=self.format_var, value="vcard")
        vcard_radio.pack(side="left", padx=(10, 15))
        
        text_radio = ctk.CTkRadioButton(format_frame, text="Text with Links", 
                                         variable=self.format_var, value="text")
        text_radio.pack(side="left")
        
        # Color selection
        color_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(color_frame, text="Colors:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        
        self.color_preview = ctk.CTkLabel(color_frame, text="█", 
                                        text_color=self.current_colors["fill"], 
                                        fg_color=self.current_colors["back"],
                                        font=ctk.CTkFont(size=20),
                                        corner_radius=5)
        self.color_preview.pack(side="left", padx=10)
        
        color_btn = ctk.CTkButton(color_frame, text="Choose Colors", 
                                     command=self.choose_colors)
        color_btn.pack(side="left", padx=5)

    def create_footer_section(self, parent):
        """Create the footer with company information and support link"""
        footer_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 10))
        
        company_label = ctk.CTkLabel(footer_frame, 
                                    text="Application by PARMAGTEE Company", 
                                    font=ctk.CTkFont(size=12, weight="bold"))
        company_label.pack(pady=(0, 2))
        
        founder_label = ctk.CTkLabel(footer_frame, 
                                     text="Founder ADAM ELSHARKAWY", 
                                     font=ctk.CTkFont(size=12))
        founder_label.pack(pady=(0, 5))

        support_label = ctk.CTkLabel(footer_frame, 
                                     text="For technical support: parmagtee@gmail.com",
                                     font=ctk.CTkFont(size=12, underline=True),
                                     cursor="hand2",
                                     text_color="#3498db")
        support_label.pack(pady=(5, 0))
        
        # Bind the click event to open the email client
        support_label.bind("<Button-1>", lambda e: self.open_email_client("parmagtee@gmail.com"))

    def open_email_client(self, email):
        """Open the user's default email client with a pre-filled recipient."""
        try:
            webbrowser.open(f"mailto:{email}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open email client: {str(e)}")

    def copy_phone_to_whatsapp(self):
        """Copy phone number to WhatsApp field"""
        phone = self.phone_entry.get().strip()
        if phone:
            self.whatsapp_entry.delete(0, tk.END)
            self.whatsapp_entry.insert(0, phone)
        else:
            messagebox.showwarning("Warning", "Please enter a phone number first!")

    def add_custom_field(self):
        """
        Add a custom field by opening a new dialog.
        The main window waits for the dialog to close before proceeding.
        """
        dialog = CustomFieldDialog(self)
        self.wait_window(dialog)
        
        # If the dialog returned a result (name and value), create the widget
        if dialog.result:
            field_name, field_value = dialog.result
            if field_name and field_value:
                # Call the function to create the actual UI component
                self.create_custom_field_widget(field_name, field_value)

    def create_custom_field_widget(self, field_name, field_value):
        """
        Create a new frame with a label, an entry, and a remove button for the custom field.
        """
        # Create a frame to hold the label, entry, and button
        field_frame = ctk.CTkFrame(self.custom_fields_container, fg_color="transparent")
        field_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(field_frame, text=f"{field_name}:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
        
        entry = ctk.CTkEntry(field_frame)
        entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        entry.insert(0, field_value)
        
        remove_btn = ctk.CTkButton(field_frame, text="✕", width=30,
                                    command=lambda: self.remove_custom_field(field_frame, field_name),
                                    fg_color="red", hover_color="darkred")
        remove_btn.pack(side="right")
        
        # Store the entry widget in the dictionary for later retrieval
        self.custom_fields[field_name] = entry

    def remove_custom_field(self, frame, field_name):
        """Remove a custom field from the GUI and the dictionary"""
        frame.destroy()
        if field_name in self.custom_fields:
            del self.custom_fields[field_name]

    def choose_colors(self):
        """Choose QR code colors using standard Tkinter dialogs"""
        # First dialog for the QR code fill color
        fill_color_choice = colorchooser.askcolor(title="Choose QR code color")[1]
        if fill_color_choice:
            self.current_colors["fill"] = fill_color_choice
        
        # Second dialog for the QR code background color
        back_color_choice = colorchooser.askcolor(title="Choose background color")[1]
        if back_color_choice:
            self.current_colors["back"] = back_color_choice
        
        # Update the color preview label to show the selected colors
        self.color_preview.configure(text_color=self.current_colors["fill"], 
                                    fg_color=self.current_colors["back"])

    def validate_phone(self, phone):
        """Validate phone number"""
        if not phone: return ""
        phone = re.sub(r'[^\d+]', '', phone)
        if re.match(r'^\+?[\d]{10,15}$', phone): return phone
        return None

    def validate_email(self, email):
        """Validate email"""
        if not email: return ""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email): return email
        return None

    def validate_url(self, url, platform=""):
        """Validate and format URL"""
        if not url: return ""
        if not url.startswith(('http://', 'https://')):
            if platform.lower() == 'facebook':
                url = f"https://facebook.com/{url}"
            elif platform.lower() == 'linkedin':
                url = f"https://linkedin.com/in/{url}"
            else:
                url = f"https://{url}"
        return url

    def collect_user_data(self):
        """Collect all user data from the form"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return None
        
        phone = self.phone_entry.get().strip()
        validated_phone = self.validate_phone(phone)
        if phone and not validated_phone:
            messagebox.showerror("Error", "Invalid phone number format!")
            return None
        
        whatsapp = self.whatsapp_entry.get().strip()
        validated_whatsapp = self.validate_phone(whatsapp)
        if whatsapp and not validated_whatsapp:
            messagebox.showerror("Error", "Invalid WhatsApp number format!")
            return None
        
        email = self.email_entry.get().strip()
        validated_email = self.validate_email(email)
        if email and not validated_email:
            messagebox.showerror("Error", "Invalid email format!")
            return None
        
        # Collect data from custom fields
        custom_data = {name: entry.get().strip() for name, entry in self.custom_fields.items() if entry.get().strip()}
        
        return {
            'name': name,
            'job_title': self.job_title_entry.get().strip(),
            'company': self.company_entry.get().strip(),
            'phone': validated_phone or phone,
            'whatsapp': validated_whatsapp or whatsapp,
            'email': validated_email or email,
            'address': self.address_text.get("1.0", tk.END).strip(),
            'website': self.validate_url(self.website_entry.get().strip()),
            'facebook': self.validate_url(self.facebook_entry.get().strip(), 'facebook'),
            'linkedin': self.validate_url(self.linkedin_entry.get().strip(), 'linkedin'),
            'custom_fields': custom_data
        }

    def create_vcard_format(self, user_info):
        """Create VCard format"""
        vcard_parts = ['BEGIN:VCARD', 'VERSION:3.0']
        if user_info['name']:
            vcard_parts.extend([f"FN:{user_info['name']}", f"N:{user_info['name']};;;"])
        if user_info['job_title']: vcard_parts.append(f"TITLE:{user_info['job_title']}")
        if user_info['company']: vcard_parts.append(f"ORG:{user_info['company']}")
        if user_info['phone']: vcard_parts.append(f"TEL:{user_info['phone']}")
        if user_info['whatsapp']: vcard_parts.append(f"TEL;TYPE=whatsapp:+{user_info['whatsapp'].lstrip('+')}")
        if user_info['email']: vcard_parts.append(f"EMAIL:{user_info['email']}")
        if user_info['address']: vcard_parts.append(f"ADR:;;{user_info['address']};;;;")
        if user_info['website']: vcard_parts.append(f"URL:{user_info['website']}")
        if user_info['facebook']: vcard_parts.append(f"X-SOCIALPROFILE;TYPE=facebook:{user_info['facebook']}")
        if user_info['linkedin']: vcard_parts.append(f"X-SOCIALPROFILE;TYPE=linkedin:{user_info['linkedin']}")
        for name, value in user_info.get('custom_fields', {}).items():
            # The custom fields are added to the VCard
            vcard_parts.append(f"X-CUSTOM;TYPE={name}:{value}")
        vcard_parts.append('END:VCARD')
        return '\n'.join(vcard_parts)

    def create_text_format(self, user_info):
        """Create text format with separators"""
        data_parts = []
        if user_info['name']: data_parts.append(f"👤 Name: {user_info['name']}")
        if user_info['job_title']: data_parts.append(f"💼 Job Title: {user_info['job_title']}")
        if user_info['company']: data_parts.append(f"🏢 Company: {user_info['company']}")
        data_parts.append("─" * 30)
        if user_info['phone']: data_parts.append(f"📞 Phone: tel:{user_info['phone']}")
        if user_info['whatsapp']:
            whatsapp_number = user_info['whatsapp'].lstrip('+').replace(' ', '').replace('-', '')
            data_parts.append(f"💬 WhatsApp: https://wa.me/{whatsapp_number}")
        if user_info['email']: data_parts.append(f"📧 Email: mailto:{user_info['email']}")
        data_parts.append("─" * 30)
        if user_info['address']: data_parts.append(f"📍 Address: {user_info['address']}")
        if user_info['website']: data_parts.append(f"🌐 Website: {user_info['website']}")
        data_parts.append("─" * 30)
        if user_info['linkedin']: data_parts.append(f"💼 LinkedIn: {user_info['linkedin']}")
        if user_info['facebook']: data_parts.append(f"👥 Facebook: {user_info['facebook']}")
        if user_info.get('custom_fields'):
            data_parts.append("─" * 30)
            for name, value in user_info['custom_fields'].items():
                data_parts.append(f"✨ {name}: {value}")
        return '\n'.join(data_parts)

    def generate_qr_code(self):
        """Function to generate the QR code based on user input"""
        user_data = self.collect_user_data()
        if not user_data: return
        try:
            qr_data = self.create_vcard_format(user_data) if self.format_var.get() == "vcard" else self.create_text_format(user_data)
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            # Use the colors from self.current_colors when generating the QR image
            self.qr_image = qr.make_image(fill_color=self.current_colors["fill"], back_color=self.current_colors["back"])
            
            # --- The fix to make the background appear seamless ---
            # Set the foreground color of the display frame to match the QR code's background color
            self.qr_display_frame.configure(fg_color=self.current_colors["back"])
            
            self.display_qr_code()
            
            self.save_btn.configure(state="normal")
            self.preview_btn.configure(state="normal")
            
            messagebox.showinfo("Success", "QR code generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def display_qr_code(self):
        """Display QR code in the GUI"""
        if self.qr_image:
            pil_image = self.qr_image.convert('RGB')
            display_size = (300, 300)
            pil_image = pil_image.resize(display_size, Image.Resampling.LANCZOS)
            
            display_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=display_size)
            self.qr_label.configure(image=display_image, text="")
            self.qr_label.image = display_image 

    def save_qr_code(self):
        """Function to save the generated QR code"""
        if not self.qr_image:
            messagebox.showerror("Error", "No QR code to save!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
            title="Save QR Code"
        )
        
        if filename:
            try:
                self.qr_image.save(filename)
                messagebox.showinfo("Success", f"QR code saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

    def preview_qr_code(self):
        """Function to show a full-size preview of the QR code"""
        if not self.qr_image:
            messagebox.showerror("Error", "No QR code to preview!")
            return
            
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("QR Code Preview")
        preview_window.geometry("500x500")
        
        # Make the preview window modal (always on top)
        preview_window.attributes("-topmost", True)
        
        pil_image = self.qr_image.convert('RGB')
        
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(500, 500))
        label = ctk.CTkLabel(preview_window, image=ctk_image, text="")
        label.image = ctk_image # Keep reference
        label.pack(expand=True)
        
        # Center the window
        preview_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (preview_window.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (preview_window.winfo_height() // 2)
        preview_window.geometry(f"+{x}+{y}")


class CustomFieldDialog(ctk.CTkToplevel):
    """A dialog for adding new custom fields to the QR code data."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Custom Field")
        self.geometry("400x200")
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        
        self.center_dialog(parent)
        
        # Removed this line to prevent interference with main window events
        # self.attributes("-topmost", True)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Field Name:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(main_frame)
        self.name_entry.pack(fill="x", pady=(5, 10))
        
        ctk.CTkLabel(main_frame, text="Field Value:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.value_entry = ctk.CTkEntry(main_frame)
        self.value_entry.pack(fill="x", pady=(5, 20))
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel, fg_color="gray", hover_color="darkgray").pack(side="right", padx=(5, 0))
        ctk.CTkButton(button_frame, text="Add", command=self.ok, fg_color="#2ecc71", hover_color="#27ae60").pack(side="right")
        
        self.bind('<Return>', lambda e: self.ok())
        self.bind('<Escape>', lambda e: self.cancel())
        
        self.name_entry.focus()

    def center_dialog(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def ok(self):
        name = self.name_entry.get().strip()
        value = self.value_entry.get().strip()
        if not name or not value:
            messagebox.showwarning("Warning", "Please fill both fields!")
            return
        self.result = (name, value)
        self.destroy()

    def cancel(self):
        self.destroy()

# Check if the script is being run directly
if __name__ == "__main__":
    app = QRCodeGenerator()
    app.mainloop()
