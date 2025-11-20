import os
import subprocess
import shutil
import sys

def run_command(command, cwd=None, shell=True):
    print(f"Step: {command} (in {cwd if cwd else 'root'})")
    try:
        subprocess.check_call(command, shell=shell, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def main():
    root_dir = os.getcwd()
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")
    
    # 1. Install Backend Dependencies
    print("\n=== 1. Installing Backend Dependencies ===")
    run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=backend_dir)
    
    # 2. Build Frontend
    print("\n=== 2. Building Frontend ===")
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("Installing Node modules...")
        run_command("npm install", cwd=frontend_dir)
    
    print("Running npm build...")
    run_command("npm run build", cwd=frontend_dir)
    
    # 3. Integrate Frontend into Backend
    print("\n=== 3. Integrating Frontend into Backend ===")
    frontend_build = os.path.join(frontend_dir, "build")
    backend_static = os.path.join(backend_dir, "app", "static")
    
    if os.path.exists(backend_static):
        shutil.rmtree(backend_static)
    
    if os.path.exists(frontend_build):
        shutil.copytree(frontend_build, backend_static)
        print(f"Copied {frontend_build} to {backend_static}")
    else:
        print("Error: Frontend build directory not found!")
        sys.exit(1)

    # 4. Create Executable
    print("\n=== 4. Creating Executable with PyInstaller ===")
    
    hidden_imports = [
        "uvicorn.loops.auto", 
        "uvicorn.lifespan.on",
        "uvicorn.logging",
        "sqlalchemy.sql.default_comparator",
        "app.api.api_v1.api",
        "app.core.database",
        "app.core.config",
        "app.models.user", 
        "app.models.account", 
        "app.models.transaction",
        "app.models.category",
        "app.models.portfolio",
        "app.models.file",
        "app.models.statement",
        "app.services.auth_service",
        "app.services.user_service"
    ]
    
    hidden_args = " ".join([f"--hidden-import={x}" for x in hidden_imports])
    
    sep = ";" if os.name == 'nt' else ":"
    
    # Bundle the static folder into the EXE
    add_data = f"--add-data \"app/static{sep}app/static\""
    
    cmd = (
        f"pyinstaller --noconfirm --onefile --windowed --name \"FinanceTracker\" "
        f"--clean "
        f"--paths \"{backend_dir}\" "
        f"{add_data} "
        f"{hidden_args} "
        f"run_app.py"
    )
    
    run_command(cmd, cwd=backend_dir)

    print("\n=== SUCCESS! ===")
    print(f"Executable created at: {os.path.join(backend_dir, 'dist', 'FinanceTracker.exe')}")

if __name__ == "__main__":
    main()