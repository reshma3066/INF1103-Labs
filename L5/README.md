# INF1103 Lab 5 - Inventory Management

## Run locally

Open PowerShell in this `L5` folder:

```powershell
python inventory_manager.py
```

Choose 1 to display, 2 to add, 3 to update stock, 4 to search by product ID,
5 to save, or 6 to save and exit. Update Stock replaces the current quantity;
it does not add the entered number to the existing stock.

## How the program works

- The inventory is a list of dictionaries. Each product has `id`, `name`,
  `price`, `stock`, and `transactions` fields.
- `add_product()`, `update_stock()`, `search_product()`, and `display_all()`
  handle the product operations. IDs are unique and case insensitive.
- `load_inventory()` reads `inventory.json` beside the Python file. If it is
  missing, the program starts with an empty list, as the assignment requires.
- `save_inventory()` writes the list using `json.dump()`. Both Save and Exit
  persist the current products and their history.
- The scenario mentions transaction amounts without defining monetary sales.
  Here, transactions record signed stock quantities: the opening quantity,
  then each increase or decrease. For example, Mouse has `[40, 10]`, giving
  its current stock of 50. A change from 50 to 45 appends `-5`.
- Invalid quantities, prices, duplicate IDs and menu options are rejected.
  An unreadable or malformed inventory file stops startup without overwriting it.

The delivered JSON contains the sample workflow's final data: Laptop (15),
Mouse (50), Keyboard (25), and Monitor (10). The JSON file supplies the
initial products; the code does not silently seed a missing file.

## Docker with persistent storage

From PowerShell in `L5`:

```powershell
docker build -t inf1103-lab5 .
docker images inf1103-lab5
docker run --rm -it --mount "type=bind,source=$($PWD.Path),target=/usr/src/app" inf1103-lab5
```

The bind mount makes the host's `L5` folder available at `/usr/src/app`.
Saving in the container updates the host's `inventory.json`. `--rm` removes
the container after exit, while the host file remains. Run the same command
again and choose 1 to confirm the saved inventory loads.

## Verification and submission

The `evidence` folder contains actual command output from the sample menu
workflow, a fresh Docker container, the Docker image listing, and validation
checks. Both Docker runs succeeded; Monitor and the updated Mouse stock
persisted between containers. Input was piped during automated verification,
so the text logs do not echo the entered answers.

Local Git commits record the dictionary/operations phase, verified loading,
and verified saving/Docker persistence. `log.txt` contains the Git history.

Remaining submission steps:

1. Capture screenshots of `docker images inf1103-lab5` and the interactive
   mounted run above. Show an entered menu option and its result; for example,
   choose 4 and enter `P004`, then choose 6. Save screenshots under `evidence`.
   The desktop screenshot helper was unavailable during preparation, so the
   included text logs are not substitutes for the requested screenshots.
2. Review the local commits, then push them when ready using `git push origin main`.
   No GitHub push or xSite upload was performed.
3. Rebuild the ZIP after adding screenshots, from the repository root:

   ```powershell
   Compress-Archive -Path L5 -DestinationPath L5_submission.zip -Force
   ```

4. Upload `L5_submission.zip` to xSite.
