
import subprocess
import webbrowser
from pathlib import Path


def start_work_mode(project_path: str) -> str:
    """Open YouTube and a project in Visual Studio Code."""

    path = Path(project_path).expanduser().resolve()

    if not path.is_dir():
        return f"Project directory not found: {path}"

    # Open YouTube in the default browser
    webbrowser.open(
        "https://www.youtube.com/watch?v=7XeqlN2PBBY&t=110s"
    )

    # Open the selected project in VS Code
    subprocess.Popen([
        "open",
        "-a",
        "Visual Studio Code",
        str(path)
    ])

    return "Work mode initiated, sir."
