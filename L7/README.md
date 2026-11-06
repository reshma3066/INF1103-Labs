# Lab 7: inheritance, overriding, abstraction and interfaces

This solution extends the existing Lab 6 inventory system. Lab 6 files are unchanged.
No third-party Python packages are needed to run Lab 7.

## Run

From the repository root:

```powershell
python L7/main.py
python -m unittest discover -s L7 -v
```

The application loads `L7/inventory.json` automatically. Choose option 2 to add
a product, enter its common information, then choose 1 for physical or 2 for
digital. Supply weight in kilograms or download size in megabytes. Stock updates
replace the current quantity and record the change in transaction history.
Options 5 and 6 save; option 6 also exits. Restart to reload the saved products.

The sample file contains a 3 kg guitar and a 250 MB music tutorial. Shipping is
$5 per kilogram, so the guitar's shipping cost is $15. Zero weight/size is allowed;
negative, non-numeric and non-finite measurements are rejected. Digital stock
continues to represent available units/licences for consistency with Lab 6.

## What changed and why

1. **Inheritance:** `PhysicalProduct` and `DigitalProduct` are specialised kinds
   of `Product`. Their constructors call `super().__init__()` for shared fields
   and validation, then store their own measurement.
2. **Overriding:** both subclasses implement `display_information()`. They first
   call `super().display_information()` to reuse the common output, then print
   their own details and fulfilment message.
3. **Abstraction:** `Product` inherits `ABC` and declares the abstract method
   `get_fulfilment_info()`. Trying `Product("X", "Generic", 1, 1)` raises
   `TypeError`; each concrete subclass supplies the required behaviour.
4. **Interface:** `CanBeShipped` declares only `calculate_shipping_cost()`.
   `PhysicalProduct(Product, CanBeShipped)` has one is-a parent and one capability
   contract. Digital products do not implement shipping.
5. **Encapsulation:** inherited private fields remain private. Subclasses expose
   read-only `weight` and `download_size` properties, as introduced in Week 9.
6. **Responsibilities:** `Inventory` still manages objects and delegates display
   and stock changes. `main.py` handles input, and `file_handling.py` handles JSON.
   No product-specific branches were needed in `Inventory`.
7. **Persistence:** each JSON record has a `type` plus `weight` or `download_size`.
   Loading constructs the correct subclass and preserves transaction history.
   Untyped Lab 6 records are rejected rather than guessing a type or measurement.
   Invalid input files are left unchanged when startup fails.

See [the UML diagram](class_diagram.md), which can be viewed in a Markdown preview
with Mermaid support. It shows inheritance, interface realisation, abstract
methods, and Inventory's association with Product.

## Verification completed

On 6 November 2026, all 9 tests passed with local Python and in the Docker image.
Coverage includes abstract-class enforcement, interface membership, display,
fulfilment, multiple shipping weights, validation, inventory operations,
encapsulation, invalid files, menu operations and persistence across a new Python
process. Tests use temporary files and do not change the sample inventory.

The Docker image built successfully, and a container menu run displayed both
sample products and exited successfully. See `verification.md` for recorded results.

## Docker workflow

Run these commands from the repository root:

```powershell
docker build -t inf1103-lab7 ./L7
docker run --rm inf1103-lab7 python -m unittest -v
docker run --rm -it --mount "type=bind,source=$((Resolve-Path ./L7).Path),target=/app" inf1103-lab7
```

The bind mount makes interactive inventory changes persist in your local L7
folder. Without a bind mount, changes in a `--rm` container disappear on exit.

## Git and submission evidence

Lab 7 was committed and published to `reshma3066/INF1103-Labs` on `main`.
The command-line push required credentials, so publication used the authenticated
GitHub connector. A subsequent `git fetch` verified the published commit. The
identical local tree was aligned with the published commit; the original local
commit remains on `lab7-local-backup`. Changes in L2, L4 and L5 were excluded.

The `evidence` folder contains actual Docker build, test and program logs plus
Git verification output. The JPG screenshots show these logs in Notepad; they
are screenshots of saved command output, not an interactive terminal session.
The Docker test screenshot shows all 9 tests passing. The program screenshot
shows both product types and the physical product's shipping calculation.

The submission ZIP contains this L7 folder, including code, tests, UML source,
sample JSON, Docker files, explanations, logs and screenshots. It excludes
Python caches, temporary tooling, Git internals and other labs.

## Optional reflection: extending the system

The optional `SubscriptionProduct` exercise is not implemented. A new subclass
can reuse `Product` without changing it, and `Inventory` can already manage any
concrete Product. However, adding subscription products would currently require
new choices in the menu and new type mappings in JSON loading/saving. Therefore,
the core classes support the Open-Closed Principle better than the input and
persistence layers. A registry mapping type identifiers to factories and input
handlers could reduce those changes; inheritance alone cannot remove them.
