import subprocess

subprocess.run(["python3", "tests/test_login.py"])
subprocess.run(["python3", "tests/test_dashboard.py"])
subprocess.run(["python3", "tests/test_batch_download.py"])