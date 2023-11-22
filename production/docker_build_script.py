import subprocess


def install_solc() -> None:
    not_installed_solcs: list[str] = (
        subprocess.run(["solc-select", "install"], capture_output=True, text=True)
        .stdout.replace("Available versions to install:", "")
        .split()
    )

    if len(not_installed_solcs) > 0:
        print("Installing solcs for Slither...")
        processes: list[subprocess.Popen[bytes]] = [
            subprocess.Popen(["solc-select", "install", solc])
            for solc in not_installed_solcs
        ]
        for process in processes:
            process.wait()

install_solc()
