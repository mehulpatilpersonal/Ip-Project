# import subprocess
# import platform
# import time

# def run_output_in_new_terminal():
#     script = 'output.py'
#     system = platform.system()

#     if system == 'Windows':
#         # Open new Command Prompt window and run output.py
#         subprocess.Popen(['start', 'cmd', '/k', f'python {script}'], shell=True)


   
if __name__ == '__main__':
    run_output_in_new_terminal()
    time.sleep(500)  # Optional: wait a bit before running the script
