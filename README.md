
# Green Lantern Corps - Automated E-Waste Management System (AEWMS)

An automated, console-based solution designed to track, manage, and audit electronic waste (e-waste). The system monitors inventory thresholds, automatically flags overdue hazardous materials, computes customized recycling fees with bulk discounts, and generates detailed analytical reports.

---

## 🚀 Features

* **Persistent File Storage:** Automatically loads historical records on startup and commits operational changes to a flat-file database (`awems_data.txt`).
* **Dynamic ID Generation:** Autonomously computes structured sequential keys (e.g., `EW001`, `EW002`) by analyzing state history.
* **Multi-Criteria Inventory Sorting:** Native support for rendering views grouped by input chronology, weight metrics, or alphanumeric category classifications.
* **Comprehensive Data Validation:** Robust, loop-contained error capturing prevents string injections on numerical/float fields (weight, choice selection, pricing).
* **Capacity Limit Engine:** Enforces a rigid storage ceiling ($1000\text{ kg}$) with logic models flagging progressive warnings at $\ge 80\%$ usage and hard block thresholds at $100\%$.
* **Hazardous Lifecycle Alerts:** Automated temporal calculation tracks time differences from date of entry, triggering critical alerts for hazardous items stored longer than 30 days.
* **Audited Financial Receipts:** Computes localized transactional costs dynamically, applying a structured $5\%$ bulk discount rule if individual unit item mass crosses a $50\text{ kg}$ threshold.
* **Analytical Reporting Engine:** Segregates inventory variables into scope-defined buckets (Daily, Monthly, or Yearly), compiling categorized performance tables saved locally as clean structural reports.

---

## 🛠️ Technical Architecture & Data Model

The application leverages Python dictionaries stored inside a central reference vector (`awems[]`). 

### Data Structure Schema
Every managed item matches the following system schema structure:

| Key Field | Data Type | Description |
| :--- | :--- | :--- |
| `item_id` | `String` | Formatted unique key identifier (`EW###`) |
| `device_name` | `String` | Commercial or structural name of the electronic item |
| `category` | `String` | Class variants: `Recyclable`, `Hazardous`, or `Non-Recyclable` |
| `weight` | `Float` | Unit mass checked into the facility (measured in kg) |
| `fee_per_kg` | `Float` | Assigned processing tariff fee index |
| `storage_status`| `String` | Lifecycle flag tracking states: `Stored`, `Recycled`, or `Disposed` |
| `date_added` | `String` | Text timestamp payload recorded via `datetime` module |

---

## 📁 System Requirements & Installation

### Prerequisites
* Python 3.10 or higher (Utilizes native `match-case` control flow syntax)

### Setup Steps
1. Clone this repository to your local architecture:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
   cd YOUR_REPOSITORY_NAME



2. Execution requires zero external dependency installations. Run the core system directly via terminal:
```bash
python main.py

```



---

## 🕹️ Application Interface Overview

When running, the console presents an interactive CLI dashboard mapping out programmatic features:

```text
==================== GREEN LANTERN CORPS AEWMS ====================
1. View Current Inventory
2. Add New E-Waste Item
3. Update Existing Item
4. Delete Item
5. Search Item by ID or Device Name
6. Calculate Processing Fee
7. Generate Storage Reports
8. Mark Item as Recycled or Disposed
9. Check Hazardous Expiry (30 Days)
10. Check Storage Capacity (80% Warning)
11. Save & Exit
===================================================================

```

> 💡 **Automated background scanning:** The engine silently executes an ecosystem audit before serving the menu loop interface, verifying category capacity volumes and surfacing warning indices if overdue hazardous assets need direct remediation.

---

## 💾 File Formatting Structure

Data writes to `awems_data.txt` using strict pipelined separation values (`|`). If modifying or inspecting logs, notice the systemic string construction layout:

```text
EW001|CRTScreen Monitor|Hazardous|32.5|15.0|Stored|24/05/2026 -- 14:20:10
EW002|Lithium Battery Pack|Hazardous|12.0|25.0|Stored|15/04/2026 -- 09:12:00
EW003|Office Server Rack|Recyclable|65.0|10.0|Recycled|25/05/2026 -- 10:05:45

```

---

## 📜 License

This project is open-source and available under the MIT License.

