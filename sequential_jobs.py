import os
import subprocess
from datetime import datetime

def find_input_files(root_dir, extensions):
    """Recursively find all files with given extensions under the root directory."""
    input_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                input_files.append(os.path.join(dirpath, filename))
    return input_files

def log_status(logfile, message):
    """Append a timestamped message to the log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(logfile, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def submit_jobs_serially(input_files, log_file):
    """Submit jobs one by one based on file extension and log their status."""
    for idx, file_path in enumerate(input_files, 1):
        job_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        base_name = os.path.splitext(file_name)[0]

        job_msg = f"Job {idx}/{len(input_files)}: {file_path}"
        log_status(log_file, f"Starting {job_msg}")

        try:
            os.chdir(job_dir)

            if file_ext == '.in':
                # Q-Chem job
                cmd = f"qchem -nt 10 {file_name} > {base_name}.out"
            elif file_ext in ['.com', '.gjf']:
                # Gaussian job
                cmd = f"g16 < {file_name} > {base_name}.log"
            elif file_ext == '.inp':
                # ORCA job
                orca_path = os.path.join(os.environ["HOME"], "orca_6_1_0", "orca")
                cmd = f"{orca_path} {file_name} > {base_name}.out"
            else:
                log_status(log_file, f"Skipped unknown file type: {file_path}")
                continue

            result = subprocess.run(cmd, shell=True)

            if result.returncode == 0:
                log_status(log_file, f"Finished {job_msg} successfully.")
            else:
                log_status(log_file, f"Error: Job failed for {file_path} with return code {result.returncode}.")

        except Exception as e:
            log_status(log_file, f"Exception while running {file_path}: {e}")

def main():
    root_dir = os.getcwd()
    log_file = os.path.join(root_dir, "log.out")

    # Clear previous log
    with open(log_file, 'w') as f:
        f.write("Quantum Chemistry Job Submission Log\n\n")

    extensions = ['.in', '.com', '.gjf', '.inp']
    input_files = sorted(find_input_files(root_dir, extensions))

    if not input_files:
        log_status(log_file, "No input files found.")
    else:
        log_status(log_file, f"Found {len(input_files)} input files. Starting job submission...\n")
        submit_jobs_serially(input_files, log_file)
        log_status(log_file, "All jobs submitted and completed.\n")

if __name__ == "__main__":
    main()

