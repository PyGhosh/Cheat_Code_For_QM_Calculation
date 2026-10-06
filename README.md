#sequential_jobs.py` – Sequential batch runner for Gaussian, ORCA and Q-Chem jobs

Runs quantum chemistry input files one after another on a local machine. It searches the current directory and all sub-directories, runs each job inside its own folder, and writes timestamped progress to `log.out`.

- **Supported inputs and commands:**
  - `.in` (Q-Chem): `qchem -nt 10 <file> > <name>.out`
  - `.com`, `.gjf` (Gaussian): `g16 < <file> > <name>.log`
  - `.inp` (ORCA): `$HOME/orca_6_1_0/orca <file> > <name>.out`
- **Requirements:** Python 3.6+ (standard library only), plus `qchem`, `g16` and ORCA installed and available on the machine. ORCA is expected at `$HOME/orca_6_1_0/orca`, so edit the path in the script if yours differs.
- **Usage:** copy the script into the top-level folder containing your job folders, then run `python sequential_jobs.py &`.
- **Behavior:** jobs run in sorted path order. The log records each job start, success, failure (with return code) and skipped file. `log.out` is overwritten at every run.
- **Notes:**
  - Q-Chem uses 10 threads by default (`-nt 10`), so change this to match your machine.
  - Q-Chem and ORCA both write `<name>.out`, so keep inputs with the same base name in separate folders.
  - The `.in` extension is also used by other programs, so make sure those files are Q-Chem inputs.
