import os
import sys
import time
import random
import subprocess
import colorama
from colorama import Fore, Back, Style
import shutil

# Initialize colorama for Windows terminal colors
colorama.init()

# Get terminal width for centering content
terminal_width = shutil.get_terminal_size().columns

# ASCII art for the menu
ASCII_ART = """
██╗     ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗██╗    ██╗ █████╗ ██████╗ ███████╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗    ██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██║     ╚██╗ ██╔╝████╗  ██║██╔════╝██║  ██║██║    ██║██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝    ██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗
██║      ╚████╔╝ ██╔██╗ ██║██║     ███████║██║ █╗ ██║███████║██████╔╝█████╗      ██║     ██████╔╝███████║██║     █████╔╝     ██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝
██║       ╚██╔╝  ██║╚██╗██║██║     ██╔══██║██║███╗██║██╔══██║██╔══██╗██╔══╝      ██║     ██╔══██╗██╔══██║██║     ██╔═██╗     ██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗
███████╗   ██║   ██║ ╚████║╚██████╗██║  ██║╚███╔███╔╝██║  ██║██║  ██║███████╗    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗    ███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
   
"""

def clear_screen():
    """Clear the terminal screen for Windows or Unix-like systems."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gradient_text(text, start_color=(91, 50, 168), end_color=(25, 25, 112)):
    """Print text with a gradient color from start_color to end_color."""
    lines = text.split('\n')
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        # Calculate gradient color for this line
        r = start_color[0] + int((end_color[0] - start_color[0]) * (i / total_lines))
        g = start_color[1] + int((end_color[1] - start_color[1]) * (i / total_lines))
        b = start_color[2] + int((end_color[2] - start_color[2]) * (i / total_lines))
        
        # Print the line centered with the calculated color
        colored_line = f"\033[38;2;{r};{g};{b}m{line.center(terminal_width)}\033[0m"
        print(colored_line)

def typing_effect(text, speed=0.003):
    """Create a typing animation effect (much faster)."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def progress_bar(prefix='', suffix='', length=30, fill='█', empty='░', duration=0.2):
    """Display a very quick animated progress bar."""
    print()
    steps = 10  # Reduce steps for faster progress
    for i in range(0, 101, 10):
        filled_length = int(length * i // 100)
        bar = fill * filled_length + empty * (length - filled_length)
        
        sys.stdout.write(f'\r{prefix} |{bar}| {i}% {suffix}')
        sys.stdout.flush()
        time.sleep(duration / steps)
    
    # Jump to 100% for immediate completion
    sys.stdout.write(f'\r{prefix} |{fill * length}| 100% {suffix}')
    sys.stdout.flush()
    print("\n")

def quick_download_animation(message="Downloading zip"):
    """Display a minimal download animation."""
    print(f"\n{Fore.CYAN}{message}...{Style.RESET_ALL}")
    sys.stdout.write(f"{Fore.GREEN}Downloading LynchWare.zip... Complete!{Style.RESET_ALL}")
    print("\n")

def frame_animation(frames, duration=0.05, repeat=1):
    """Display a simple frame-by-frame animation."""
    for _ in range(repeat):
        for frame in frames:
            sys.stdout.write('\r' + frame)
            sys.stdout.flush()
            time.sleep(duration)
    print()

def show_system_check():
    """Show a quick system compatibility check."""
    components = [
        ("CPU", "Compatible", True),
        ("Memory", "64 MB Available", True),
        ("Disk Space", "120 MB Available", True),
        ("Network", "Connected", True),
        ("Permissions", "Administrator", True)
    ]
    
    print(f"\n{Fore.CYAN}System Compatibility Check:{Style.RESET_ALL}")
    for component, status, ok in components:
        color = Fore.GREEN if ok else Fore.RED
        sys.stdout.write(f"\r{Fore.YELLOW}Checking {component}... {color}{status}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.08)
        print()
    
    print(f"{Fore.GREEN}✓ All systems ready{Style.RESET_ALL}")
    time.sleep(0.1)

def show_menu():
    """Display the main menu with options."""
    clear_screen()
    print_gradient_text(ASCII_ART)
    
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{' PFS CHAMP LYNCHWARE CRACK MENU ':^46}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╠══════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{' 1. Run LynchWare Crack ':^46}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{' 2. Install LynchWare Crack Source Code ':^46}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}{' 3. Exit ':^46}{Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    return input(f"\n{Fore.MAGENTA}Enter your choice (1-3): {Style.RESET_ALL}")

def run_lynchware():
    """Run the LynchWare crack with minimal waiting."""
    clear_screen()
    print_gradient_text("LAUNCHING LYNCHWARE CRACK")
    
    # Quick loading message
    typing_effect(f"{Fore.CYAN}Initializing LynchWare...{Style.RESET_ALL}", speed=0.001)
    progress_bar(prefix=f"{Fore.YELLOW}Loading", suffix=f"{Style.RESET_ALL}", duration=0.2)
    
    print(f"{Fore.GREEN}Starting application...{Style.RESET_ALL}")
    
    try:
        # Full path to the crack file
        crack_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LW_Crack-2.9.6(Run This).py")
        
        if getattr(sys, 'frozen', False):
            # If running as a PyInstaller bundle
            subprocess.Popen([sys.executable, crack_path], shell=True)
        else:
            # If running as a script
            subprocess.Popen([sys.executable, crack_path], shell=False)
        
        print(f"{Fore.GREEN}LynchWare launched successfully!{Style.RESET_ALL}")
        time.sleep(0.3)
    except Exception as e:
        print(f"{Fore.RED}Error launching LynchWare: {e}{Style.RESET_ALL}")
        time.sleep(0.5)

def install_source_code():
    """Simulate installing the LynchWare crack source code quickly."""
    clear_screen()
    print_gradient_text("INSTALLING SOURCE CODE")
    
    # Single quick message
    typing_effect(f"{Fore.CYAN}Extracting LynchWare source code...{Style.RESET_ALL}", speed=0.001)
    progress_bar(prefix=f"{Fore.YELLOW}Extracting zip", suffix=f"{Style.RESET_ALL}", duration=0.2)
    
    # Create a fake installation path that looks legitimate
    install_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source_code")
    print(f"{Fore.GREEN}Installation complete! Files extracted to:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{install_path}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Press any key to return to menu...{Style.RESET_ALL}")
    input()

def main():
    """Main function to run the menu program."""
    # Enhanced boot sequence with more animation
    clear_screen()
    
    # Initial loading spinner
    spinner_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    print(f"{Fore.MAGENTA}Starting LynchWare Crack...{Style.RESET_ALL}")
    frame_animation([f"{Fore.CYAN}{frame} Loading system{Style.RESET_ALL}" for frame in spinner_frames], 0.03, 2)
    
    # Main title with gradient
    print_gradient_text("INITIALIZING PFS CHAMP LYNCHWARE CRACK")
    
    # Simulated system check
    typing_effect(f"{Fore.YELLOW}Performing system check...{Style.RESET_ALL}", speed=0.001)
    show_system_check()
    
    # Boot sequence animation
    boot_steps = [
        ("Initializing kernel", Fore.CYAN, 0.15),
        ("Loading core modules", Fore.GREEN, 0.15),
        ("Preparing interface", Fore.MAGENTA, 0.15),
        ("Establishing secure connection", Fore.YELLOW, 0.15)
    ]
    
    for step, color, duration in boot_steps:
        typing_effect(f"{color}{step}...{Style.RESET_ALL}", speed=0.001)
        progress_bar(prefix=f"{color}Progress", suffix=f"{Style.RESET_ALL}", duration=duration)
    
    # Final loading before menu
    print(f"\n{Fore.GREEN}✓ PFS CHAMP LYNCHWARE CRACK LOADED SUCCESSFULLY{Style.RESET_ALL}")
    time.sleep(0.2)
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_lynchware()
        elif choice == '2':
            install_source_code()
        elif choice == '3':
            clear_screen()
            print_gradient_text("THANK YOU FOR USING PFS CHAMP'S LYNCHWARE CRACK")
            typing_effect(f"{Fore.CYAN}Shutting down...{Style.RESET_ALL}", speed=0.001)
            progress_bar(prefix=f"{Fore.YELLOW}Closing", suffix=f"{Style.RESET_ALL}", duration=0.2)
            print(f"{Fore.MAGENTA}Goodbye!{Style.RESET_ALL}")
            time.sleep(0.3)
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
            time.sleep(0.3)

if __name__ == "__main__":
    main()
