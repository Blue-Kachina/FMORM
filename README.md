# fmorm

A fluent, Eloquent-inspired SQL query builder for FileMaker Pro, implemented entirely as Custom Functions on top of `ExecuteSQL`.

---

## How it works

Each builder function accepts a JSON **query object** as its first argument, adds or modifies one clause, and returns the updated object. The terminal function `QueryGet_cf` assembles the final SQL string and executes it via `ExecuteSQL`.

```
_query = QueryNew_cf ( "CONTACT" )
_query = QueryWhere_cf ( _query ; "CONTACT.status" ; "=" ; "Active" )
_query = QueryLimit_cf ( _query ; 50 )
_result = QueryGet_cf ( _query ; "," ; "¶" )
```

Bound values are stored inside the query object and injected at execution time using `Evaluate`. This means every value is safely parameterised — no manual quoting or SQL injection risk.

---

## Installation

Import `fmorm-all.xml` into your FileMaker file via the Custom Function manager:

1. Open **File > Manage > Custom Functions…**
2. Click the gear icon and choose **Import…** (or paste via clipboard in the PHPStorm workflow)
3. Select or paste `fmorm-all.xml`
4. Import all 25 functions

Alternatively, import individual functions from `src/` or `src/internal/` as needed.

---

## Quick start

```
Let
(
[
_query = QueryNew_cf ( "CONTACT" ) ;
_query = QuerySelect_cf ( _query ; "CONTACT.id, CONTACT.firstName, CONTACT.lastName" ) ;
_query = QueryLeftJoin_cf ( _query ; "contact__INVOICE" ; "CONTACT.id" ; "=" ; "contact__INVOICE.idContact" ) ;
_query = QueryWhere_cf ( _query ; "CONTACT.status" ; "=" ; "Active" ) ;
_query = QueryWhereIn_cf ( _query ; "CONTACT.type" ; "customer¶prospect" ) ;
_query = QueryWhereNotNull_cf ( _query ; "CONTACT.emailWork" ) ;
_query = QueryOrderBy_cf ( _query ; "CONTACT.lastName" ; "ASC" ) ;
_query = QueryLimit_cf ( _query ; 50 ) ;
_result = QueryGet_cf ( _query ; "," ; "¶" )
];
_result
)
```

Use `QueryToSQL_cf` at any point to inspect the SQL string that would be produced without executing it — useful during development.

---

## FileMaker SQL dialect notes

- **Table occurrence names** are used everywhere, not base table names. These are the names shown in the relationship graph.
- **No `LIMIT`** — fmorm emits `FETCH FIRST n ROWS ONLY` (use `QueryLimit_cf`).
- **Offset** is expressed as `OFFSET n ROWS` (use `QueryOffset_cf`).
- **No `NULL`** — FileMaker stores empty values, not SQL `NULL`. `IS NULL` / `IS NOT NULL` behaviour may differ from standard SQL.
- `ExecuteSQL` returns a literal `?` on error. `QueryGet_cf` detects this and returns an empty string instead.
- `ExecuteSQL` is **read-only** — no INSERT, UPDATE, or DELETE.

---

## Function reference

See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.
