import os
import subprocess
from . import utils
import fman.fs as fs
from fman.url import as_human_readable, as_url
from fman import DirectoryPaneCommand, QuicksearchItem
from fman import show_alert, show_prompt, show_quicksearch, show_status_message

class MiniCopyPathToClipboard(DirectoryPaneCommand):
    def __call__(self):
        current_path = self.pane.get_path()
        if current_path:
            os.system(f'echo {as_human_readable(current_path)} | clip')
            show_status_message('Path copied to clipboard')
class MiniSelectFileAndMoveCursorDown(DirectoryPaneCommand):
    def __call__(self):
        current_file = self.pane.get_file_under_cursor()
        if current_file:
            # 將當前檔案設為選取狀態
            self.pane.select([current_file])
        # 移動游標向上
        self.pane.move_cursor_down()
class MiniSelectFileAndMoveCursorUp(DirectoryPaneCommand):
    def __call__(self):
        current_file = self.pane.get_file_under_cursor()
        if current_file:
            # 將當前檔案設為選取狀態
            self.pane.select([current_file])
        # 移動游標向上
        self.pane.move_cursor_up()
class MiniExtractWith7z(DirectoryPaneCommand):
    def __call__(self):
        current_file = self.pane.get_file_under_cursor()
        os.chdir(as_human_readable(self.pane.get_path()))
        try:
            subprocess.run(["7z.exe", "x", as_human_readable(current_file)], check=True)
            show_alert(f"Extracted File Successful: {current_file}")
        except subprocess.CalledProcessError as e:
            show_alert(f"Extract Failed: {e}")
class MiniAddTo7z(DirectoryPaneCommand):
    def __call__(self):
        selected_files = self.pane.get_selected_files()
        
        if not selected_files:
            show_alert("Please select at least one file.")
            return

        output_path = self.pane.get_path()  # Use the current directory as the output path
        output_filename = os.path.join(output_path, "output.7z")
        output_filename, ok = show_prompt('output filename', output_filename, len(output_filename) - len('output.7z'), len(output_filename) - len('.7z'))

        if ok and output_filename:
            # Use 7z.exe to compress the selected files
            try:
                subprocess.run(["7z.exe", "a", as_human_readable(output_filename)] + [as_human_readable(str(file)) for file in selected_files], check=True)
                show_alert(f"Compression successful: {output_filename}")
            except subprocess.CalledProcessError as e:
                show_alert(f"Compression failed: {e}")
class MiniPowershellTerminal(DirectoryPaneCommand):
    def __call__(self):
        os.system(f'pwsh -WorkingDirectory {as_human_readable(self.pane.get_path())}')
class MiniRenameFiles(DirectoryPaneCommand):
    def __call__(self):
        path = as_human_readable(self.pane.get_path())
        orinames = [fs.basename(v) for v in self.pane.get_selected_files()]
        newnames = [v.strip() for v in utils.edit_with_code('\n'.join(orinames)).split('\n')]

        for i in range(len(orinames)):
            from_name = as_url(os.path.join(path, orinames[i]))
            to_name = as_url(os.path.join(path, newnames[i]))
            fs.move(from_name, to_name)
class MiniRunPowershellCommand(DirectoryPaneCommand):
    def __call__(self):
        command, ok = show_prompt("Command:")
        if ok and command:
            with utils.EnterPath(as_human_readable(self.pane.get_path())):
                os.system(f'pwsh -Command "{command}"')
class MiniRunSystemCommand(DirectoryPaneCommand):
    def __call__(self):
        command, ok = show_prompt("Command:")
        if ok and command:
            with utils.EnterPath(as_human_readable(self.pane.get_path())):
                os.system(command)