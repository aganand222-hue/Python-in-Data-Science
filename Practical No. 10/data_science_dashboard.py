"""
================================================================================
 UNIVERSAL DATA SCIENCE GUI DASHBOARD
================================================================================
Mini Data Science Project

Works with ANY real-world CSV dataset (Sales, E-commerce, Movies, Sports,
Student Performance, Employee Data, Healthcare, Weather, Banking, etc.)
Load a different CSV at any time from the top bar and every tab re-detects
its numeric / categorical columns automatically - nothing is hardcoded to
one specific dataset.

    Tab 1 : Data Overview        -> Part B (Loading & Exploration)
    Tab 2 : Data Cleaning        -> Part C (Cleaning)
    Tab 3 : Data Analysis        -> Part D (NumPy + Pandas analysis)
    Tab 4 : Visualizations       -> Part E (Matplotlib + Seaborn charts)
    Tab 5 : Web Data (BS4)       -> Part F (BeautifulSoup web scraping - bonus)
    Tab 6 : Dashboard            -> Part G (Final summary dashboard)

Libraries used : numpy, pandas, matplotlib, seaborn, tkinter, beautifulsoup4,
                 requests

Run it with:
    python data_science_dashboard.py

Then click "Browse..." (top-right) and pick ANY .csv file with at least
one numeric column - every tab will adapt to that dataset automatically.
================================================================================
"""

import os
import io
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

sns.set_style("whitegrid")

DEFAULT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")
MAX_CATEGORY_CARDINALITY = 30   # columns with more unique values than this are not offered as "category" columns


def is_text_dtype(series: pd.Series) -> bool:
    """True for text columns under BOTH the classic 'object' dtype and pandas 2.x/3.x's
    newer dedicated string dtype (pd.StringDtype / the default 'str' dtype in pandas 3.0+).
    Using only `dtype == object` silently misses every text column on pandas 3.x, which
    is exactly the kind of hidden incompatibility that breaks the app on a fresh dataset."""
    return series.dtype == object or pd.api.types.is_string_dtype(series)


# ==============================================================================
# COLUMN-DETECTION HELPERS (this is what makes the app dataset-agnostic)
# ==============================================================================
def detect_id_like_columns(df: pd.DataFrame):
    """Columns that look like unique identifiers (not useful for analysis).

    Important: the "every value is unique" heuristic is only applied to integer or
    text columns. Continuous float measurements (Price, Revenue, Balance, Salary...)
    are very often all-unique too, but they are exactly the columns we want to keep
    and analyze - so floats are never dropped purely for being unique.
    """
    ids = []
    for col in df.columns:
        name = col.lower()
        looks_like_id_name = name.endswith("id") or name in ("index", "unnamed: 0")
        is_int_or_text = pd.api.types.is_integer_dtype(df[col]) or is_text_dtype(df[col])
        is_unique_key = (is_int_or_text and len(df) > 1
                         and df[col].nunique(dropna=False) == len(df))
        if looks_like_id_name or is_unique_key:
            ids.append(col)
    return ids


def detect_numeric_columns(df: pd.DataFrame):
    cols = list(df.select_dtypes(include=[np.number]).columns)
    # a numeric column with only one distinct value is useless for analysis
    return [c for c in cols if df[c].nunique(dropna=True) > 1]


def detect_categorical_columns(df: pd.DataFrame):
    cats = []
    for col in df.columns:
        if col in detect_id_like_columns(df):
            continue
        n_unique = df[col].nunique(dropna=True)
        if n_unique < 2:
            continue
        if is_text_dtype(df[col]) or str(df[col].dtype) == "category":
            if n_unique <= max(MAX_CATEGORY_CARDINALITY, len(df) // 2):
                cats.append(col)
        elif pd.api.types.is_numeric_dtype(df[col]) and n_unique <= 12:
            # low-cardinality numeric columns (e.g. star ratings, 0/1 flags) work well as categories too
            cats.append(col)
    # sort so the most "usable" categories (fewer groups) come first - nicer default charts
    return sorted(cats, key=lambda c: df[c].nunique(dropna=True))


def best_default_numeric(df: pd.DataFrame, num_cols):
    """Prefer a continuous, high-variety numeric column over a 0/1 flag or a near-constant one,
    so charts default to something meaningful (e.g. a 'Balance' or 'Revenue' column) rather
    than a binary target column."""
    if not num_cols:
        return None
    return max(num_cols, key=lambda c: df[c].nunique(dropna=True))


def detect_text_columns(df: pd.DataFrame):
    """Free-text / high-cardinality columns, not treated as numeric or category."""
    numeric = set(detect_numeric_columns(df))
    cats = set(detect_categorical_columns(df))
    ids = set(detect_id_like_columns(df))
    return [c for c in df.columns if c not in numeric and c not in cats and c not in ids]


# ==============================================================================
# HELPER: a scrollable, monospace text panel used to print pandas/numpy output
# ==============================================================================
class OutputPanel(scrolledtext.ScrolledText):
    def __init__(self, master, **kwargs):
        super().__init__(master, wrap="none", font=("Consolas", 10), **kwargs)
        self.configure(state="disabled", bg="#0f172a", fg="#e2e8f0", insertbackground="white")

    def write(self, text):
        self.configure(state="normal")
        self.delete("1.0", tk.END)
        self.insert(tk.END, text)
        self.configure(state="disabled")


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
class DataScienceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Universal Data Science Dashboard")
        self.geometry("1300x820")
        self.minsize(1050, 680)
        self.configure(bg="#f1f5f9")

        self.df_raw = None
        self.df = None
        self.csv_path = tk.StringVar(value=DEFAULT_CSV)

        self._build_style()
        self._build_header()
        self._build_notebook()
        self._build_statusbar()

        if os.path.exists(DEFAULT_CSV):
            self.after(200, self.load_dataset)

    # ------------------------------------------------------------------ style
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))
        style.configure("Header.TFrame", background="#0f172a")
        style.configure("TButton", padding=6, font=("Segoe UI", 9))
        style.configure("Accent.TButton", padding=8, font=("Segoe UI", 10, "bold"))

    # ----------------------------------------------------------------- header
    def _build_header(self):
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x", side="top")
        tk.Label(header, text="📊  Universal Data Science Dashboard", bg="#0f172a", fg="white",
                 font=("Segoe UI", 18, "bold"), pady=14, padx=16).pack(side="left")
        tk.Label(header, text="Load ANY CSV - NumPy · Pandas · Matplotlib · Seaborn · BeautifulSoup",
                 bg="#0f172a", fg="#94a3b8", font=("Segoe UI", 10), padx=16).pack(side="left")

        path_frame = tk.Frame(header, bg="#0f172a")
        path_frame.pack(side="right", padx=12)
        ttk.Entry(path_frame, textvariable=self.csv_path, width=40).pack(side="left", padx=4)
        ttk.Button(path_frame, text="Browse...", command=self.browse_csv).pack(side="left", padx=2)
        ttk.Button(path_frame, text="Load Dataset", style="Accent.TButton",
                   command=self.load_dataset).pack(side="left", padx=4)

    # -------------------------------------------------------------- statusbar
    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Ready. Load any CSV dataset to begin.")
        tk.Label(self, textvariable=self.status_var, bd=1, relief="sunken", anchor="w",
                 bg="#e2e8f0", font=("Segoe UI", 9)).pack(side="bottom", fill="x")

    def set_status(self, text):
        self.status_var.set(text)
        self.update_idletasks()

    # -------------------------------------------------------------- notebook
    def _build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_overview = OverviewTab(self.notebook, self)
        self.tab_cleaning = CleaningTab(self.notebook, self)
        self.tab_analysis = AnalysisTab(self.notebook, self)
        self.tab_viz = VisualizationTab(self.notebook, self)
        self.tab_web = WebScrapeTab(self.notebook, self)
        self.tab_dashboard = DashboardTab(self.notebook, self)

        self.notebook.add(self.tab_overview, text="1. Data Overview")
        self.notebook.add(self.tab_cleaning, text="2. Data Cleaning")
        self.notebook.add(self.tab_analysis, text="3. Data Analysis")
        self.notebook.add(self.tab_viz, text="4. Visualizations")
        self.notebook.add(self.tab_web, text="5. Web Data (BeautifulSoup)")
        self.notebook.add(self.tab_dashboard, text="6. Dashboard")

    # ------------------------------------------------------------ csv loading
    def browse_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            self.csv_path.set(path)
            self.load_dataset()

    def load_dataset(self):
        path = self.csv_path.get()
        if not os.path.exists(path):
            messagebox.showerror("File not found", f"Could not find:\n{path}")
            return
        try:
            self.df_raw = pd.read_csv(path)
            if self.df_raw.shape[1] < 2:
                messagebox.showerror("Unsupported file", "That file doesn't look like a valid CSV table.")
                return
            self.df = self.df_raw.copy()
            self.set_status(f"Loaded '{os.path.basename(path)}' -> "
                             f"{self.df.shape[0]} rows x {self.df.shape[1]} columns")
            self.tab_overview.refresh()
            self.tab_cleaning.reset()
            self.tab_analysis.refresh_columns()
            self.tab_viz.refresh_columns()
            self.tab_dashboard.refresh_columns()
        except Exception as exc:
            messagebox.showerror("Error loading CSV", f"{exc}\n\nMake sure this is a plain CSV file "
                                  "with a header row and at least one numeric column.")
            traceback.print_exc()

    def require_data(self):
        if self.df is None:
            messagebox.showwarning("No data", "Please load a dataset first (top-right 'Load Dataset').")
            return False
        return True

    def current_df(self):
        return self.df if self.df is not None else self.df_raw


# ==============================================================================
# TAB 1 : DATA OVERVIEW  (Part B)  -- already fully generic
# ==============================================================================
class OverviewTab(ttk.Frame):
    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app
        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=6, padx=6)
        for label, cmd in [
            ("Head (5)", self.show_head), ("Tail (5)", self.show_tail),
            ("Shape", self.show_shape), ("Columns", self.show_columns),
            ("Data Types (info)", self.show_info), ("Describe (stats)", self.show_describe),
            ("Missing Values", self.show_missing), ("Duplicate Records", self.show_duplicates),
        ]:
            ttk.Button(btns, text=label, command=cmd).pack(side="left", padx=3)
        self.output = OutputPanel(self, height=35)
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

    def refresh(self):
        self.show_head()

    def show_head(self):
        if not self.app.require_data():
            return
        self.output.write("df.head()\n" + "-" * 90 + "\n" + self.app.current_df().head().to_string())

    def show_tail(self):
        if not self.app.require_data():
            return
        self.output.write("df.tail()\n" + "-" * 90 + "\n" + self.app.current_df().tail().to_string())

    def show_shape(self):
        if not self.app.require_data():
            return
        r, c = self.app.current_df().shape
        self.output.write(f"df.shape\n{'-'*90}\nRows: {r}\nColumns: {c}")

    def show_columns(self):
        if not self.app.require_data():
            return
        df = self.app.current_df()
        cols = "\n".join(f"  {i+1:>2}. {c}  ({df[c].dtype})" for i, c in enumerate(df.columns))
        self.output.write(f"df.columns  ({len(df.columns)} columns)\n{'-'*90}\n{cols}")

    def show_info(self):
        if not self.app.require_data():
            return
        buf = io.StringIO()
        self.app.current_df().info(buf=buf)
        self.output.write("df.info()\n" + "-" * 90 + "\n" + buf.getvalue())

    def show_describe(self):
        if not self.app.require_data():
            return
        self.output.write("df.describe(include='all').T\n" + "-" * 90 + "\n"
                           + self.app.current_df().describe(include="all").T.to_string())

    def show_missing(self):
        if not self.app.require_data():
            return
        df = self.app.current_df()
        miss = df.isnull().sum()
        pct = (miss / len(df) * 100).round(2)
        table = pd.DataFrame({"missing_count": miss, "missing_%": pct})
        self.output.write("df.isnull().sum()\n" + "-" * 90 + "\n" + table.to_string()
                           + f"\n\nTotal missing cells: {int(miss.sum())}")

    def show_duplicates(self):
        if not self.app.require_data():
            return
        dupes = self.app.current_df().duplicated().sum()
        self.output.write(f"df.duplicated().sum()\n{'-'*90}\nDuplicate rows: {dupes}")


# ==============================================================================
# TAB 2 : DATA CLEANING  (Part C)  -- fully generic, no hardcoded column names
# ==============================================================================
class CleaningTab(ttk.Frame):
    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app
        self.cleaned = False

        top = ttk.Frame(self)
        top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Cleaning pipeline (adapts to whichever dataset is loaded):",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        steps = (
            "  1. Remove exact duplicate rows (df.drop_duplicates())\n"
            "  2. Fill missing values: numeric columns -> median, text/category columns -> mode\n"
            "  3. Auto-detect and drop pure identifier columns (e.g. *Id, Unnamed: 0, or a column\n"
            "     whose values are 100% unique) - these carry no analytical signal\n"
            "  4. Strip leading/trailing whitespace from column names and text values\n"
            "  5. Convert low-cardinality text columns to the pandas 'category' dtype\n"
            "  6. Report which columns are numeric vs categorical after cleaning\n"
        )
        ttk.Label(top, text=steps, justify="left", font=("Consolas", 9)).pack(anchor="w", pady=4)
        ttk.Button(top, text="Run Cleaning", style="Accent.TButton",
                   command=self.run_cleaning).pack(anchor="w", pady=4)

        self.output = OutputPanel(self, height=30)
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

    def reset(self):
        self.cleaned = False

    def run_cleaning(self):
        if not self.app.require_data():
            return
        df = self.app.df_raw.copy()
        log = []

        df.columns = df.columns.str.strip()

        before_rows = len(df)
        df = df.drop_duplicates()
        log.append(f"Removed duplicate rows: {before_rows - len(df)} removed "
                    f"(before={before_rows}, after={len(df)})")

        missing_before = int(df.isnull().sum().sum())
        for col in df.columns:
            if df[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    mode = df[col].mode()
                    df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "Unknown")
        log.append(f"Missing values found: {missing_before} -> filled with median/mode "
                    f"({int(df.isnull().sum().sum())} remaining)")

        id_cols = detect_id_like_columns(df)
        if id_cols:
            df = df.drop(columns=id_cols)
        log.append(f"Dropped identifier-like columns (auto-detected): {id_cols or 'none found'}")

        for col in df.columns:
            if is_text_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip()
        for col in detect_categorical_columns(df):
            if is_text_dtype(df[col]):
                df[col] = df[col].astype("category")
        log.append("Converted low-cardinality text columns to 'category' dtype")

        self.app.df = df
        self.cleaned = True
        self.app.tab_analysis.refresh_columns()
        self.app.tab_viz.refresh_columns()
        self.app.tab_dashboard.refresh_columns()
        self.app.set_status(f"Cleaning complete -> {df.shape[0]} rows x {df.shape[1]} columns")

        num_cols = detect_numeric_columns(df)
        cat_cols = detect_categorical_columns(df)
        report = "DATA CLEANING LOG\n" + "=" * 90 + "\n"
        report += "\n".join(f"- {line}" for line in log)
        report += f"\n- Detected numeric columns  : {num_cols}"
        report += f"\n- Detected categorical columns: {cat_cols}"
        report += "\n\n" + "=" * 90 + "\nCleaned dataset preview (df.head()):\n" + "-" * 90 + "\n"
        report += df.head().to_string()
        report += "\n\n" + "-" * 90 + f"\nFinal shape: {df.shape}\nFinal columns: {list(df.columns)}"
        self.output.write(report)


# ==============================================================================
# TAB 3 : DATA ANALYSIS  (Part D)  -- column pickers instead of hardcoded names
# ==============================================================================
class AnalysisTab(ttk.Frame):
    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app

        picker = ttk.Frame(self)
        picker.pack(fill="x", padx=6, pady=6)
        ttk.Label(picker, text="Category column:").pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(picker, textvariable=self.cat_var, state="readonly", width=22)
        self.cat_combo.pack(side="left", padx=(4, 16))

        ttk.Label(picker, text="Numeric column:").pack(side="left")
        self.num_var = tk.StringVar()
        self.num_combo = ttk.Combobox(picker, textvariable=self.num_var, state="readonly", width=22)
        self.num_combo.pack(side="left", padx=(4, 16))

        ttk.Button(picker, text="Run Full Analysis (9 operations)", style="Accent.TButton",
                   command=self.run_analysis).pack(side="left", padx=8)

        self.output = OutputPanel(self, height=33)
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

    def refresh_columns(self):
        df = self.app.current_df()
        if df is None:
            return
        cats = detect_categorical_columns(df)
        nums = detect_numeric_columns(df)
        self.cat_combo["values"] = cats
        self.num_combo["values"] = nums
        self.cat_var.set(cats[0] if cats else "")
        self.num_var.set(best_default_numeric(df, nums) if nums else "")

    def run_analysis(self):
        if not self.app.require_data():
            return
        df = self.app.current_df()
        num_cols = detect_numeric_columns(df)
        cat_cols = detect_categorical_columns(df)
        if not num_cols:
            messagebox.showwarning("No numeric columns", "This dataset has no usable numeric columns to analyze.")
            return

        cat = self.cat_var.get() if self.cat_var.get() in cat_cols else (cat_cols[0] if cat_cols else None)
        num = self.num_var.get() if self.num_var.get() in num_cols else num_cols[0]
        out = ["DATA ANALYSIS - NumPy & Pandas (9 operations)", "=" * 90]

        # 1. Central tendency for every numeric column
        out.append("\n1) CENTRAL TENDENCY - mean / median / std for every numeric column")
        for col in num_cols:
            out.append(f"   {col:<20} mean={np.mean(df[col]):>14,.2f}  "
                        f"median={np.median(df[col]):>14,.2f}  std={np.std(df[col]):>14,.2f}")

        # 2. Range
        out.append(f"\n2) RANGE - max() / min() of '{num}'")
        out.append(f"   Highest {num}: {np.max(df[num]):,.2f}")
        out.append(f"   Lowest  {num}: {np.min(df[num]):,.2f}")

        # 3. sum & count
        out.append(f"\n3) SUM & COUNT - '{num}'")
        out.append(f"   Count (non-null): {df[num].count()}")
        out.append(f"   Sum             : {np.sum(df[num]):,.2f}")

        # 4. value_counts
        if cat:
            out.append(f"\n4) VALUE_COUNTS - records per '{cat}'")
            out.append(df[cat].value_counts().to_string())
        else:
            out.append("\n4) VALUE_COUNTS - skipped (no categorical column detected)")

        # 5. groupby mean
        if cat:
            out.append(f"\n5) GROUPBY - average '{num}' by '{cat}'")
            grp_mean = df.groupby(cat, observed=True)[num].mean().sort_values(ascending=False)
            out.append(grp_mean.round(2).to_string())
        else:
            grp_mean = None
            out.append("\n5) GROUPBY - skipped (no categorical column detected)")

        # 6. groupby count / sum
        if cat:
            out.append(f"\n6) GROUPBY - count of records and total '{num}' by '{cat}'")
            grp_agg = df.groupby(cat, observed=True)[num].agg(["count", "sum"]).sort_values("sum", ascending=False)
            out.append(grp_agg.round(2).to_string())
        else:
            out.append("\n6) GROUPBY - skipped (no categorical column detected)")

        # 7. sort_values - top 10 rows
        out.append(f"\n7) SORT_VALUES - Top 10 rows by '{num}'")
        show_cols = ([cat] if cat else []) + [num]
        show_cols = list(dict.fromkeys([c for c in show_cols if c in df.columns]))
        out.append(df.sort_values(num, ascending=False)[show_cols].head(10).to_string())

        # 8. correlation matrix
        out.append("\n8) CORRELATION - relationships between numeric columns")
        if len(num_cols) >= 2:
            corr = df[num_cols].corr(numeric_only=True)
            out.append(corr.round(3).to_string())
        else:
            out.append("   Only one numeric column available - correlation needs at least two.")

        # 9. NumPy quartile binning of the numeric column, then group
        out.append(f"\n9) NUMPY - '{num}' split into quartile bins (np.percentile) and compared")
        try:
            q = np.percentile(df[num].dropna(), [0, 25, 50, 75, 100])
            q = np.unique(q)
            if len(q) >= 3:
                bin_labels = [f"Q{i+1}" for i in range(len(q) - 1)]
                tmp = df.copy()
                tmp["_bin"] = pd.cut(tmp[num], bins=q, labels=bin_labels, include_lowest=True)
                other_num = next((c for c in num_cols if c != num), num)
                out.append(tmp.groupby("_bin", observed=True)[other_num].mean().round(2).to_string())
            else:
                out.append("   Not enough distinct values to form quartile bins.")
        except Exception as exc:
            out.append(f"   Could not compute quartile bins: {exc}")

        out.append("\n" + "=" * 90 + "\nKEY ANSWERS\n" + "=" * 90)
        out.append(f"- Average {num}          : {np.mean(df[num]):,.2f}")
        out.append(f"- Highest {num}          : {np.max(df[num]):,.2f}")
        out.append(f"- Lowest {num}           : {np.min(df[num]):,.2f}")
        if cat and grp_mean is not None and len(grp_mean) > 0:
            out.append(f"- '{cat}' with HIGHEST average {num}: {grp_mean.index[0]} ({grp_mean.iloc[0]:,.2f})")
            out.append(f"- '{cat}' with LOWEST average {num} : {grp_mean.index[-1]} ({grp_mean.iloc[-1]:,.2f})")
            out.append(f"- Most frequent {cat}  : {df[cat].value_counts().idxmax()}")

        self.output.write("\n".join(out))


# ==============================================================================
# TAB 4 : VISUALIZATIONS  (Part E)  -- column pickers instead of hardcoded names
# ==============================================================================
class VisualizationTab(ttk.Frame):
    CHART_OPTIONS = [
        "1. Bar Chart - Average [Numeric] by [Category]",
        "2. Line Chart - [Numeric] trend across quartile bins",
        "3. Histogram - Distribution of [Numeric]",
        "4. Seaborn Box Plot - [Numeric] by [Category]",
        "5. Pie Chart - Share of records by [Category]",
        "6. Seaborn Heatmap - Correlation of numeric columns",
    ]

    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app

        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=6, pady=6)
        ttk.Label(controls, text="Chart:").pack(side="left")
        self.chart_var = tk.StringVar(value=self.CHART_OPTIONS[0])
        ttk.Combobox(controls, textvariable=self.chart_var, values=self.CHART_OPTIONS,
                     width=42, state="readonly").pack(side="left", padx=(4, 14))

        ttk.Label(controls, text="Category:").pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(controls, textvariable=self.cat_var, state="readonly", width=16)
        self.cat_combo.pack(side="left", padx=(4, 14))

        ttk.Label(controls, text="Numeric:").pack(side="left")
        self.num_var = tk.StringVar()
        self.num_combo = ttk.Combobox(controls, textvariable=self.num_var, state="readonly", width=16)
        self.num_combo.pack(side="left", padx=(4, 14))

        ttk.Button(controls, text="Draw Chart", style="Accent.TButton",
                   command=self.draw_chart).pack(side="left", padx=8)
        ttk.Button(controls, text="Save Chart as PNG", command=self.save_chart).pack(side="left")

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=6, pady=6)
        self.figure = Figure(figsize=(9, 5.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
        self.toolbar.update()

    def refresh_columns(self):
        df = self.app.current_df()
        if df is None:
            return
        cats = detect_categorical_columns(df)
        nums = detect_numeric_columns(df)
        self.cat_combo["values"] = cats
        self.num_combo["values"] = nums
        self.cat_var.set(cats[0] if cats else "")
        self.num_var.set(best_default_numeric(df, nums) if nums else "")

    def draw_chart(self):
        if not self.app.require_data():
            return
        df = self.app.current_df()
        num_cols = detect_numeric_columns(df)
        if not num_cols:
            messagebox.showwarning("No numeric columns", "This dataset has no usable numeric columns to plot.")
            return
        cat_cols = detect_categorical_columns(df)
        cat = self.cat_var.get() if self.cat_var.get() in cat_cols else (cat_cols[0] if cat_cols else None)
        num = self.num_var.get() if self.num_var.get() in num_cols else num_cols[0]
        choice = self.chart_var.get()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        try:
            if choice.startswith("1"):
                if not cat:
                    raise ValueError("No categorical column available for a bar chart.")
                data = df.groupby(cat, observed=True)[num].mean().sort_values(ascending=False)
                sns.barplot(x=data.index, y=data.values, ax=ax, hue=data.index,
                            palette="viridis", legend=False)
                ax.set_title(f"Average {num} by {cat}")
                ax.set_xlabel(cat); ax.set_ylabel(f"Average {num}")
                ax.tick_params(axis="x", rotation=30)

            elif choice.startswith("2"):
                q = np.unique(np.percentile(df[num].dropna(), [0, 25, 50, 75, 100]))
                if len(q) < 3:
                    raise ValueError(f"'{num}' does not have enough spread to bin into quartiles.")
                labels = [f"Q{i+1}" for i in range(len(q) - 1)]
                tmp = df.copy()
                tmp["_bin"] = pd.cut(tmp[num], bins=q, labels=labels, include_lowest=True)
                other_num = next((c for c in num_cols if c != num), num)
                data = tmp.groupby("_bin", observed=True)[other_num].mean().reindex(labels)
                ax.plot(data.index, data.values, marker="o", linewidth=2, color="#dc2626")
                ax.set_title(f"{other_num} trend across {num} quartiles")
                ax.set_xlabel(f"{num} (quartile)"); ax.set_ylabel(f"Average {other_num}")
                ax.grid(True, alpha=0.3)

            elif choice.startswith("3"):
                ax.hist(df[num].dropna(), bins=20, color="#2563eb", edgecolor="white")
                ax.set_title(f"Distribution of {num}")
                ax.set_xlabel(num); ax.set_ylabel("Frequency")

            elif choice.startswith("4"):
                if not cat:
                    raise ValueError("No categorical column available for a box plot.")
                sns.boxplot(x=cat, y=num, data=df, ax=ax, hue=cat, palette="Set2", legend=False)
                ax.set_title(f"{num} distribution by {cat}")
                ax.tick_params(axis="x", rotation=30)

            elif choice.startswith("5"):
                if not cat:
                    raise ValueError("No categorical column available for a pie chart.")
                data = df[cat].value_counts()
                if len(data) > 10:
                    data = data.head(10)
                ax.pie(data.values, labels=data.index, autopct="%1.1f%%", startangle=90,
                       colors=sns.color_palette("pastel"))
                ax.set_title(f"Share of records by {cat}")
                ax.axis("equal")

            elif choice.startswith("6"):
                if len(num_cols) < 2:
                    raise ValueError("Need at least two numeric columns for a correlation heatmap.")
                sns.heatmap(df[num_cols].corr(numeric_only=True), annot=True, fmt=".2f",
                            cmap="coolwarm", ax=ax, annot_kws={"size": 8})
                ax.set_title("Correlation Heatmap of Numeric Columns")

            self.figure.tight_layout()
            self.canvas.draw()
            self.app.set_status(f"Rendered: {choice}")
        except Exception as exc:
            # Show the problem inline on the canvas instead of a blocking popup, so switching
            # through chart/column combinations stays fluid even when a combination doesn't apply.
            self.figure.clear()
            ax2 = self.figure.add_subplot(111)
            ax2.axis("off")
            ax2.text(0.5, 0.5, f"Can't draw this chart with the current selection:\n\n{exc}\n\n"
                                f"Try a different Category / Numeric column.",
                      ha="center", va="center", wrap=True, fontsize=11, color="#b91c1c")
            self.canvas.draw()
            self.app.set_status(f"Could not render: {choice} ({exc})")

    def save_chart(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG image", "*.png")])
        if path:
            self.figure.savefig(path, dpi=150, bbox_inches="tight")
            messagebox.showinfo("Saved", f"Chart saved to:\n{path}")


# ==============================================================================
# TAB 5 : WEB DATA COLLECTION USING BEAUTIFULSOUP  (Part F - bonus, generic)
# ==============================================================================
class WebScrapeTab(ttk.Frame):
    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app
        self.scraped_df = None

        top = ttk.Frame(self)
        top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="URL to scrape (public page):").pack(side="left")
        self.url_var = tk.StringVar(value="https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue")
        ttk.Entry(top, textvariable=self.url_var, width=55).pack(side="left", padx=6)
        ttk.Button(top, text="Fetch & Parse with BeautifulSoup", style="Accent.TButton",
                   command=self.scrape).pack(side="left", padx=6)
        ttk.Button(top, text="Save Scraped Data as CSV", command=self.save_scraped).pack(side="left")

        note = ("Note: only public, non-login-protected pages should be scraped. This demo extracts "
                "the first HTML table found on the page into a pandas DataFrame (Part F requirement).")
        ttk.Label(self, text=note, wraplength=1150, foreground="#475569",
                  font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=6)

        self.output = OutputPanel(self, height=30)
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

    def scrape(self):
        url = self.url_var.get().strip()
        if not url:
            return
        self.app.set_status(f"Fetching {url} ...")
        try:
            import requests
            from bs4 import BeautifulSoup

            headers = {"User-Agent": "Mozilla/5.0 (Educational Data Science Project)"}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            page_title = soup.title.text.strip() if soup.title else "(no title found)"

            table = soup.find("table", {"class": "wikitable"}) or soup.find("table")
            if table is None:
                self.output.write(f"Page title: {page_title}\n\nNo <table> element found on this page.")
                return

            rows = []
            headers_row = [th.get_text(strip=True) for th in table.find_all("th")]
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cells:
                    rows.append(cells)
            max_len = max((len(r) for r in rows), default=0)
            rows = [r + [""] * (max_len - len(r)) for r in rows]
            self.scraped_df = pd.DataFrame(rows, columns=headers_row) if (
                headers_row and len(headers_row) == max_len) else pd.DataFrame(rows)

            out = f"Page title : {page_title}\nURL        : {url}\n"
            out += f"Table shape: {self.scraped_df.shape}\n" + "-" * 90 + "\n"
            out += self.scraped_df.head(15).to_string()
            self.output.write(out)
            self.app.set_status(f"Scraped table with {self.scraped_df.shape[0]} rows from {url}")
        except Exception as exc:
            self.output.write(
                "Could not fetch/parse the page (this usually means there is no internet access "
                f"from this machine, or the site structure changed).\n\nError: {exc}\n\n"
                "This tab demonstrates the BeautifulSoup workflow required in Part F; the main "
                "analysis (Parts B-E, G) works fully offline from your loaded CSV."
            )
            self.app.set_status("Web scrape failed - see message for details.")

    def save_scraped(self):
        if self.scraped_df is None:
            messagebox.showwarning("Nothing to save", "Run a scrape first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        if path:
            self.scraped_df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"Scraped data saved to:\n{path}")


# ==============================================================================
# TAB 6 : DASHBOARD  (Part G)  -- column pickers instead of hardcoded names
# ==============================================================================
class DashboardTab(ttk.Frame):
    def __init__(self, parent, app: DataScienceApp):
        super().__init__(parent)
        self.app = app

        top = ttk.Frame(self)
        top.pack(fill="x", padx=6, pady=6)
        ttk.Label(top, text="Category:").pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(top, textvariable=self.cat_var, state="readonly", width=16)
        self.cat_combo.pack(side="left", padx=(4, 14))
        ttk.Label(top, text="Numeric:").pack(side="left")
        self.num_var = tk.StringVar()
        self.num_combo = ttk.Combobox(top, textvariable=self.num_var, state="readonly", width=16)
        self.num_combo.pack(side="left", padx=(4, 14))
        ttk.Button(top, text="Build / Refresh Dashboard", style="Accent.TButton",
                   command=self.build_dashboard).pack(side="left", padx=8)
        ttk.Button(top, text="Export Dashboard as PNG", command=self.export_png).pack(side="left")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=6, pady=6)

        self.kpi_frame = ttk.Frame(container)
        self.kpi_frame.pack(fill="x", pady=(0, 8))

        self.figure = Figure(figsize=(12, 7.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.findings_var = tk.StringVar()
        tk.Label(container, textvariable=self.findings_var, justify="left", anchor="w",
                 bg="#fffbeb", font=("Segoe UI", 10), wraplength=1180, padx=10, pady=8,
                 bd=1, relief="solid").pack(fill="x", pady=8)

    def refresh_columns(self):
        df = self.app.current_df()
        if df is None:
            return
        cats = detect_categorical_columns(df)
        nums = detect_numeric_columns(df)
        self.cat_combo["values"] = cats
        self.num_combo["values"] = nums
        self.cat_var.set(cats[0] if cats else "")
        self.num_var.set(best_default_numeric(df, nums) if nums else "")

    def _kpi_card(self, parent, title, value, color="#2563eb"):
        card = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        tk.Label(card, text=title, bg="white", fg="#64748b", font=("Segoe UI", 9)).pack(pady=(10, 0))
        tk.Label(card, text=value, bg="white", fg=color, font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
        return card

    def build_dashboard(self):
        if not self.app.require_data():
            return
        df = self.app.current_df()
        num_cols = detect_numeric_columns(df)
        if not num_cols:
            messagebox.showwarning("No numeric columns", "This dataset has no usable numeric columns.")
            return
        cat_cols = detect_categorical_columns(df)
        cat = self.cat_var.get() if self.cat_var.get() in cat_cols else (cat_cols[0] if cat_cols else None)
        num = self.num_var.get() if self.num_var.get() in num_cols else num_cols[0]

        for w in self.kpi_frame.winfo_children():
            w.destroy()
        kpis = [
            ("Total Records", f"{len(df):,}"),
            (f"{cat or 'Category'} groups", f"{df[cat].nunique() if cat else '-'}"),
            (f"Avg {num}", f"{df[num].mean():,.1f}"),
            (f"Max {num}", f"{df[num].max():,.1f}"),
            (f"Min {num}", f"{df[num].min():,.1f}"),
        ]
        for title, value in kpis:
            self._kpi_card(self.kpi_frame, title, value).pack(side="left", expand=True, fill="both", padx=4)

        self.figure.clear()
        self.figure.suptitle("DATA SCIENCE DASHBOARD", fontsize=15, fontweight="bold")

        ax1 = self.figure.add_subplot(2, 2, 1)
        if cat:
            data1 = df.groupby(cat, observed=True)[num].mean().sort_values(ascending=False)
            if len(data1) > 12:
                data1 = data1.head(12)
            sns.barplot(x=data1.index, y=data1.values, ax=ax1, hue=data1.index, palette="viridis", legend=False)
            ax1.set_title(f"Average {num} by {cat}", fontsize=10)
            ax1.tick_params(axis="x", rotation=30)
        else:
            ax1.text(0.5, 0.5, "No categorical column available", ha="center", va="center")

        ax2 = self.figure.add_subplot(2, 2, 2)
        try:
            q = np.unique(np.percentile(df[num].dropna(), [0, 25, 50, 75, 100]))
            labels = [f"Q{i+1}" for i in range(len(q) - 1)]
            tmp = df.copy()
            tmp["_bin"] = pd.cut(tmp[num], bins=q, labels=labels, include_lowest=True)
            other_num = next((c for c in num_cols if c != num), num)
            data2 = tmp.groupby("_bin", observed=True)[other_num].mean().reindex(labels)
            ax2.plot(data2.index, data2.values, marker="o", color="#dc2626", linewidth=2)
            ax2.set_title(f"{other_num} across {num} quartiles", fontsize=10)
        except Exception:
            ax2.text(0.5, 0.5, "Not enough spread to bin", ha="center", va="center")

        ax3 = self.figure.add_subplot(2, 2, 3)
        if cat:
            data3 = df[cat].value_counts()
            if len(data3) > 8:
                data3 = data3.head(8)
            ax3.pie(data3.values, labels=data3.index, autopct="%1.1f%%", startangle=90,
                    colors=sns.color_palette("pastel"))
            ax3.set_title(f"Share of records by {cat}", fontsize=10)
        else:
            ax3.text(0.5, 0.5, "No categorical column available", ha="center", va="center")

        ax4 = self.figure.add_subplot(2, 2, 4)
        ax4.hist(df[num].dropna(), bins=20, color="#2563eb", edgecolor="white")
        ax4.set_title(f"Distribution of {num}", fontsize=10)

        self.figure.tight_layout(rect=[0, 0, 1, 0.95])
        self.canvas.draw()

        findings = [f"1. Dataset contains {len(df):,} records and {df.shape[1]} columns "
                    f"after cleaning; {num} ranges from {df[num].min():,.1f} to {df[num].max():,.1f}."]
        if cat:
            grp = df.groupby(cat, observed=True)[num].mean().sort_values(ascending=False)
            counts = df[cat].value_counts()
            findings.append(f"2. '{grp.index[0]}' has the HIGHEST average {num} ({grp.iloc[0]:,.1f}), "
                             f"while '{grp.index[-1]}' has the lowest ({grp.iloc[-1]:,.1f}).")
            findings.append(f"3. '{counts.idxmax()}' is the most common {cat}, "
                             f"accounting for {counts.max():,} of {len(df):,} records "
                             f"({counts.max()/len(df)*100:.1f}%).")
        if len(num_cols) >= 2:
            corr = df[num_cols].corr(numeric_only=True)[num].drop(num).sort_values(ascending=False)
            if len(corr) > 0:
                findings.append(f"4. '{corr.index[0]}' is the numeric column most strongly correlated "
                                 f"with {num} (correlation = {corr.iloc[0]:.2f}).")
        findings.append(f"5. Average {num} across all records is {df[num].mean():,.1f} "
                         f"(median {df[num].median():,.1f}, std dev {df[num].std():,.1f}).")

        self.findings_var.set("KEY FINDINGS\n" + "\n".join(findings))
        self.app.set_status("Dashboard built successfully.")

    def export_png(self):
        if not self.app.require_data():
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", initialfile="dashboard.png",
                                             filetypes=[("PNG image", "*.png")])
        if not path:
            return
        self.build_dashboard()
        self.figure.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        messagebox.showinfo("Exported", f"Dashboard image saved to:\n{path}")


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = DataScienceApp()
    app.mainloop()
