import os
import subprocess
from . import utils
import fman.fs as fs
from fman.url import as_human_readable, as_url
from fman import DirectoryPaneCommand, QuicksearchItem
from fman import show_alert, show_prompt, show_quicksearch

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