import subprocess
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

KV = """
ScreenManager:
    MainScreen:

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'

        MDLabel:
            text: "Manage Python Dependencies"
            font_size: '24sp'

        MDTextField:
            id: requirements_text
            hint_text: "Paste your requirements.txt here..."
            multiline: True
            size_hint_y: 0.6

        MDRaisedButton:
            text: "Install/Resolve Dependencies"
            on_release: app.process_requirements()

        MDLabel:
            id: message_label
            halign: "center"
            size_hint_y: 0.2

        MDDialog:
            id: dialog
            size_hint: (0.8, 0.6)
            buttons: [
                MDRaisedButton(text="OK", on_release=lambda x: app.close_dialog())
            ]
"""

class MainScreen(MDScreen):
    pass

class DependencyManagerApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def process_requirements(self):
        requirements_text = self.root.ids.requirements_text.text
        if not requirements_text:
            self.show_dialog("Error", "Please paste the requirements.txt content.")
            return

        try:
            # Write the content to a temporary file
            with open("temp_requirements.txt", "w") as file:
                file.write(requirements_text)

            # Attempt to install using pip
            result = subprocess.run(
                ['pip', 'install', '-r', 'temp_requirements.txt'],
                capture_output=True
            )

            if result.returncode == 0:
                self.show_dialog("Success", "Dependencies installed successfully.")
            else:
                self.show_dialog("Error", f"Error installing dependencies:\n{result.stderr.decode()}")

        except Exception as e:
            self.show_dialog("Error", f"An unexpected error occurred: {str(e)}")

    def show_dialog(self, title, message):
        self.root.ids.dialog.title = title
        self.root.ids.dialog.text = message
        self.root.ids.dialog.open()

    def close_dialog(self):
        self.root.ids.dialog.dismiss()

if __name__ == "__main__":
    DependencyManagerApp().run()
