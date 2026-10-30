# INF1103 Week 8 - Lab 6

An object-oriented refactor of the Week 5 inventory system, following the
worksheet's Product, Inventory, main-program and file-handling responsibilities.
The application uses the Week 8 concepts: classes, objects, `__init__`, `self`,
encapsulation and the Single Responsibility Principle.

## Run locally

Open PowerShell in this `L6` folder and run:

```powershell
python main.py
```

The menu has six options: display all products, add a product, update stock,
search by product ID, save inventory, and exit. Exit also saves the inventory.
**Update Stock sets the new total quantity**, rather than adding that quantity.
For example, changing 45 to 50 adds a `5` entry to the stock transaction history.

## Files and responsibilities

| File | Purpose |
| --- | --- |
| `product.py` | `Product` stores private product details, validates and updates its own stock, and displays its information. |
| `inventory.py` | `Inventory` holds a list of Product objects, adds and finds products, delegates stock updates and displays the collection. |
| `main.py` | Displays the menu, reads input and calls public methods. |
| `file_handling.py` | Loads JSON records into objects and saves objects as JSON records using public getters. |
| `inventory.json` | Updated inventory data, compatible with the Week 5 format. |
| `class_diagram.png` / `.svg` | UML for both application classes, including visibility, types, parameters and return types. |
| `class_diagram.md` | Explains the diagram and design choices. |
| `reflection.md` | Answers to all 10 worksheet reflection questions. |
| `test_inventory.py` | Automated checks using Python's standard library. |
| `Dockerfile` | Optional image definition for running this lab independently. |
| `log.txt` | Git history exported after the completed lab commit. |
| `evidence/` | Actual Docker screenshots, run logs and verification results. |

The application has only two classes. There is no inheritance, abstract class,
interface, menu class or file-handling class. The classes in the optional test
file belong to the testing framework, not the application design.

## Data and validation

Product IDs are unique and case insensitive. Blank IDs/names, negative or
non-finite prices, and invalid stock quantities are rejected. Product attributes
are private by convention using double underscores; other code uses public
methods. The list getters return copies to protect the stored lists.

The existing Week 5 stock histories are preserved. During the Docker demonstration,
Mouse (`P002`) was changed from 45 to 50 units and Webcam (`P005`, $79.90,
8 units) was added. The final file contains Laptop, Mouse, Keyboard, Monitor and
Webcam. Earlier lab folders are unchanged by this refactor.

The program reads `inventory.json` beside the Python files, regardless of the
terminal's current directory. A missing file starts an empty inventory. Malformed
data stops startup without replacing the original file. Older valid records
without a transaction history start with their current stock as the first entry.

## Docker with a volume mount

From PowerShell in `L6`, use the existing worksheet image:

```powershell
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor python -B main.py
```

The explicit `python -B main.py` replaces the older image's `auditor.py` command.
The mounted folder means code changes take effect without rebuilding the image,
and saves persist in the host's `L6/inventory.json` after the container exits.

If the existing image is unavailable, build the supplied Dockerfile once:

```powershell
docker build -t inf1103-lab6 .
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-lab6
```

## Verification evidence

All 12 automated tests passed locally and in Docker. Tests cover independent
object state, validation, duplicate IDs, copied lists, JSON round trips, legacy
records, malformed-file protection, all six menu options and input recovery.
They use temporary files and do not change the lab's inventory.

```powershell
python -B -m unittest -v test_inventory.py
```

- `evidence/01-docker-running.jpg`: Docker Desktop shows the running container,
  menu option 1 and the initial inventory output.
- `evidence/02-program-input-output.jpg`: a new container accepts option 4 and
  product ID P005, then displays the saved Webcam product.
- `evidence/docker-run.txt`: actual first-run output, including adding Webcam,
  updating Mouse, saving and searching. Some answers were fed together, so their
  terminal echo appears before the corresponding prompts.
- `evidence/docker-container.txt`: first container's status, image, command and
  bind mount.
- `evidence/docker-restart.txt`: a fresh container loads Mouse stock 50 and
  Webcam stock 8, then exits successfully.
- `evidence/tests.txt`: clean test output and exit code 0 from Docker.

## Submission

The Python files, updated JSON, UML, Git log and both requested screenshots are
included in this folder. `L6_submission.zip` is beside the `L6` folder and contains
the complete submission folder without Python cache files.

The work has been committed locally. GitHub push and xSite upload have not been
performed. Review the files and reflection answers before submitting them.

To update the exported Git history or rebuild the archive after later edits, run
from the repository root:

```powershell
git log > L6/log.txt
Compress-Archive -Path L6 -DestinationPath L6_submission.zip -Force
```
