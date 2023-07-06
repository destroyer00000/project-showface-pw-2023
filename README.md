# project-showface-pw-2023

1. download cmake from https://cmake.org/download/
2. add to your PATH variable under `Edit the system environmental variables > Environmental variables.. > Path > New` and paste your CMake/bin directory `C:\Program Files\CMake\bin`
3. download Microsoft C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
4. enable C++ CMake Tools for Windows under `Visual Studio Build Tools > Modify > Desktop Development with C++ > Optional > C++ CMake Tools for Windows`
5. ensure that the correct Windows SDK version is installed (Windows 10 or Windows 11) under `Visual Studio Build Tools > Modify > Desktop Development with C++ > Optional > Windows SDK`
6. create a Virtual Environment with `py -m venv (your venv name)`
7. assuming you are using visual studio code, enable your Virtual Environment through `Command Palette (Ctrl+Shift+P) > Python: Select Interpreter > (your venv name)`
8. install all build dependencies with `py -m pip install -r requirements.txt` (and run `py -m pip install -U pip` to upgrade pip if necessary)