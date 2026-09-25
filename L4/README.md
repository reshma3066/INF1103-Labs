# Week 4: Persistent Auditor

The Week 4 program builds on the Week 3 functions and adds file storage and a list of transactions.

## What changed

- `load_inventory()` reads the saved total from line 1 and the comma-separated quantities from line 2. `int()` converts file text back into numbers. If the file is missing, it returns `0, []` so the first run works.
- `transaction_history.append(quantity)` records each accepted delivery, including zero. Rejected input never reaches this line.
- `save_inventory(total, history)` writes the current total and the complete history. `str()` and `join()` turn the list into comma-separated text. Opening with `w` replaces the old snapshot; `with` closes the file automatically.
- `main()` loads once at startup, updates the total and list, then saves after the loop. Both `quit` and the existing overstock exit reach the save step.
- `Path(__file__).with_name("inventory.txt")` keeps the file beside the script even if Python is started from another folder.
- The existing input validation, 10% tax, overstock alert above 500, and per-session counters remain in use.

The saved demonstration data is:

```text
175
100,50,25
```

The first line is the total; the second represents the Python list `[100, 50, 25]`. The file stores history across runs, while delivery and rejected-entry counters describe only the current run. The program expects files in this two-line format; malformed files are not repaired automatically. Save happens on normal loop exit, not forced termination.

## Run locally

From the repository root in PowerShell:

```powershell
python L4/persistent_auditor.py
```

Enter a whole non-negative quantity for each delivery, then type `quit` to save and exit.

## Build and run in Docker

From the repository root in PowerShell:

```powershell
docker build -t inf1103-labs-persistent-auditor:latest L4
$labFolder = (Resolve-Path L4).Path
docker run --rm -it --mount "type=bind,source=$labFolder,target=/usr/src/app" inf1103-labs-persistent-auditor:latest
```

The image is the packaged program. `docker run` creates a container from it. The bind mount connects the host's `L4` folder to `/usr/src/app`, so `inventory.txt` is stored on your computer. Removing the container with `--rm` does not remove that host file. This folder mount also makes the host script visible inside the container; rebuild the image after code changes to keep its packaged copy current.

Docker uses a build to save the reproducible image; a separate `docker commit` is unnecessary. The image is available locally in Docker Desktop. No Docker registry upload is needed for this lab.

## Verification and evidence

Local checks passed for first-run startup, empty history, valid and invalid input, zero quantities, save/reload across separate processes, a different working directory, and saving the transaction that pushes stock above 500.

Docker checks passed for the image without a mount and for persistence across two containers:

1. The first mounted container accepted `100`, rejected `bad`, accepted `50`, then saved `150` on `quit`. That container was removed.
2. A new container loaded `150` and `[100, 50]`, accepted `25`, and saved `175` and `[100, 50, 25]`.
3. The host file and the container's mount configuration were checked.

`evidence/docker-verification.txt` contains the actual output, image listing, and mount inspection. The stopped `inf1103-week4-evidence` container is retained in Docker Desktop for reviewing its logs and bind mount. A stopped container is expected after `quit`.

`log.txt` records Git history through the implementation/evidence commit. The later commit that adds the log cannot appear inside its own log file.

The PDF's sample screenshot shows a separate product-orders example. This implementation follows the written inventory requirements: `inventory.txt`, numeric totals, and transaction history.

## Remaining submission screenshots

Desktop screenshot capture was unavailable because the Computer Use native pipe could not connect. The text evidence is real execution output, but it does not replace the screenshots requested in the handout.

Before uploading, capture:

1. A terminal running `docker images inf1103-labs-persistent-auditor`.
2. An interactive run using the Docker command above, showing a quantity entered and the saved report after `quit`.
3. The volume mount, either in Docker Desktop under `inf1103-week4-evidence` or using `docker inspect inf1103-week4-evidence`.

Add those screenshots to the submission ZIP. Further runs update `inventory.txt`; include the newest file if you make additional transactions. Upload to xSite yourself when ready.
