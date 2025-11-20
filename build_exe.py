import os
import subprocess
import shutil
import sys

def run_command(command, cwd=None):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    base_dir = os.getcwd()
    backend_dir = os.path.join(base_dir, "backend")
    
    # Explicitly list EVERY module to be absolutely sure
    hidden_imports = [
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=sqlalchemy.sql.default_comparator",
        "--hidden-import=sklearn.neighbors._typedefs",
        "--hidden-import=sklearn.utils._cython_blas",
        "--hidden-import=sklearn.tree._utils",
        "--hidden-import=sklearn.neighbors._quad_tree",
        "webview", "google.generativeai",
        # App Core
        "--hidden-import=app.core",
        "--hidden-import=app.core.config",
        "--hidden-import=app.core.database",
        "--hidden-import=app.core.security",
        # App Models
        "--hidden-import=app.models",
        "--hidden-import=app.models.user",
        "--hidden-import=app.models.account",
        "--hidden-import=app.models.transaction",
        "--hidden-import=app.models.category",
        "--hidden-import=app.models.portfolio",
        "--hidden-import=app.models.file",
        "--hidden-import=app.models.statement",
        # App Services
        "--hidden-import=app.services",
        "--hidden-import=app.services.auth_service",
        "--hidden-import=app.services.user_service",
        "--hidden-import=app.services.ai_advisor",
        "--hidden-import=app.services.bank_parsers",
        "--hidden-import=app.services.categorizer",
        "--hidden-import=app.services.statement_processor",
        # App Schemas (CRITICAL ADDITION)
        "--hidden-import=app.schemas",
        "--hidden-import=app.schemas.auth", 
        # App API
        "--hidden-import=app.api.api_v1.api",
        "--hidden-import=app.main"
    ]

    run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=backend_dir)

    print("\n=== Step 2: Creating Standalone EXE ===")
    sep = ";" if os.name == 'nt' else ":"
    
    # Hidden imports for complex libraries
    hidden = [
        "uvicorn.loops.auto", "uvicorn.lifespan.on", "uvicorn.logging",
        "sqlalchemy.sql.default_comparator",
        "sklearn.neighbors._typedefs", "sklearn.utils._cython_blas", 
        "sklearn.tree._utils", "sklearn.neighbors._quad_tree",
        "webview", "google.generativeai",
        # App Modules
        "app.models", "app.models.user", "app.models.account", 
        "app.models.transaction", "app.models.category", 
        "app.models.portfolio", "app.models.file", "app.models.statement",
        "app.services", "app.services.ai_advisor", 
        "app.api.api_v1.api", "app.main"
    ]
    
    hidden_args = " ".join([f"--hidden-import={x}" for x in hidden])

    cmd = (
        f"pyinstaller --noconfirm --onefile --windowed --name \"FinanceTracker\" "
        f"--clean "
        f"--paths \"{backend_dir}\" "
        f"--add-data \"app/templates{sep}app/templates\" "
        f"--add-data \"app/static{sep}app/static\" "
        f"{hidden_args} "
        f"run_app.py"
    )
    
    run_command(cmd, cwd=backend_dir)

    print("\n=== SUCCESS! ===")
    print(f"Executable created at: {os.path.join(backend_dir, 'dist', 'FinanceTracker.exe')}")

if __name__ == "__main__":
    main()