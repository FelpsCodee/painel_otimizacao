from __future__ import annotations

import sys
import ctypes

from src.app import PCOptimizerApp
from src.ui.display import show_warning, show_error


def main() -> None:
    if sys.platform != "win32":
        show_error("Este programa é compatível apenas com Windows.")
        sys.exit(1)

    if not ctypes.windll.shell32.IsUserAnAdmin():
        show_warning(
            "Executando sem privilégios de administrador. Algumas funções podem não funcionar."
        )

    app = PCOptimizerApp()
    app.run()


if __name__ == "__main__":
    main()
