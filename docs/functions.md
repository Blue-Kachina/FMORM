# fmorm Function Reference

---

## Table of Contents

### Public builders

| Function | Purpose |
|---|---|
| [QueryNew\_cf](#querynew_cf) | Initialise a new query object |
| [QuerySelect\_cf](#queryselect_cf) | Set the SELECT column list |
| [QueryWhere\_cf](#querywhere_cf) | Append an AND WHERE condition |
| [QueryOrWhere\_cf](#queryorwhere_cf) | Append an OR WHERE condition |
| [QueryWhereIn\_cf](#querywherein_cf) | Append an AND WHERE … IN (…) condition |
| [QueryWhereNull\_cf](#querywherenull_cf) | Append AND column IS NULL |
| [QueryWhereNotNull\_cf](#querywherenotnull_cf) | Append AND column IS NOT NULL |
| [QueryJoin\_cf](#queryjoin_cf) | Append an INNER JOIN |
| [QueryLeftJoin\_cf](#queryleftjoin_cf) | Append a LEFT JOIN |
| [QueryOrderBy\_cf](#queryorderby_cf) | Append an ORDER BY column |
| [QueryGroupBy\_cf](#querygroupby_cf) | Append a GROUP BY column |
| [QueryHaving\_cf](#queryhaving_cf) | Append an AND HAVING condition |
| [QueryLimit\_cf](#querylimit_cf) | Set the row limit |
| [QueryOffset\_cf](#queryoffset_cf) | Set the row offset |
| [QueryGet\_cf](#queryget_cf) | Execute the query and return results |
| [QueryGetResultsAsJson\_cf](#querygetresultsasjson_cf) | Execute the query and return results as a JSON array of objects |
| [QueryToSQL\_cf](#querytosql_cf) | Return the assembled SQL string (debug) |

### Utility functions

| Function | Purpose |
|---|---|
| [JSONGetElementLikeField\_cf](#jsongetelementlikefield_cf) | Get a JSON element using a FileMaker field reference or field-name string as the property key |

### Internal helpers

These functions are called by the public builders and are not intended to be called directly.

| Function | Purpose |
|---|---|
| [QueryBuildJoins\_cf](#querybuildjoins_cf) | Recursively render JOIN clauses |
| [QueryBuildWheres\_cf](#querybuildwheres_cf) | Recursively render WHERE clause body |
| [QueryBuildInPlaceholders\_cf](#querybuildinplaceholders_cf) | Render N comma-separated `?` placeholders |
| [QueryBuildGroupBys\_cf](#querybuildgroupbys_cf) | Recursively render GROUP BY column list |
| [QueryBuildHavings\_cf](#querybuildhavings_cf) | Recursively render HAVING clause body |
| [QueryBuildOrderBys\_cf](#querybuildorderbys_cf) | Recursively render ORDER BY column list |
| [QueryBuildBindingArgs\_cf](#querybuildbindingargs_cf) | Render binding values for Evaluate injection |
| [QueryBuildWhereBooleanPrefix\_cf](#querybuildwherebooleanprefix_cf) | Render AND / OR / empty connector |
| [QueryAppendBindings\_cf](#queryappendbindings_cf) | Recursively append N values to the bindings array |
| [QueryBuildSelects\_cf](#querybuildselects_cf) | Convert ¶-delimited field names to quoted SQL column list |
| [QueryConvertField\_cf](#queryconvertfield_cf) | Convert a single `Table::Field` name to quoted dot notation |
| [QueryBuildJsonRow\_cf](#querybuildjsonrow_cf) | Build a single JSON object from a row of field values |
| [QueryBuildJsonRows\_cf](#querybuildjsonrows_cf) | Recursively build a JSON array from all result rows |
| [QueryBuildSelectKeys\_cf](#querybuildselectkeys_cf) | Extract plain key names from the original column input |

---

## Public builders

---

### QueryNew_cf

Initialises a fresh query object for the given table occurrence. All clause arrays are set to empty, `selects` defaults to `*`, and all counts are set to `0`. Pass the returned object as the first argument to every subsequent builder call.

The table name is stored pre-quoted (`"Table"`) so the generated SQL consistently uses double-quoted identifiers throughout.

**Parameters**

| Parameter | Description |
|---|---|
| `table` | Table occurrence name as a plain string (`"CONTACT"`), or any `GetFieldName()` result from that table (`GetFieldName ( CONTACT::anyField )`). When a `Table::Field` string is passed the table part is extracted automatically. |

**Example**

```
Let
(
[
_query = QueryNew_cf ( GetFieldName ( CONTACT::__kptID ) )
];
_query
)
```

---

### QuerySelect_cf

Replaces the SELECT column list. By default all columns are selected (`*`). Call once — the entire list is replaced wholesale, not appended.

Accepts either a ¶-delimited list (e.g. from FileMaker's `List()` and `GetFieldName()`) or a plain comma-separated string. FileMaker fully-qualified field names in `Table::Field` format are automatically converted to quoted SQL dot notation (`"Table"."Field"`). Expressions that do not contain `::` — such as `*`, `COUNT(*)`, or already-dotted names — pass through unchanged.

Also stores a `selectKeys` field in the query object: a ¶-delimited list of plain field names extracted from the original input (e.g. `PrimaryKey¶FullName`), which `QueryGetResultsAsJson_cf` uses to name the properties of each result object.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object returned by a previous builder call |
| `columns` | ¶-delimited list from `List()` / `GetFieldName()`, or a comma-separated SQL column string |

**Example**

```
// Using GetFieldName() — recommended; survives field renames
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreatedBy ) ) )

// Using a plain SQL string — also valid
_query = QuerySelect_cf ( _query ; "CONTACT.id, CONTACT.firstName, CONTACT.lastName" )
```

---

### QueryWhere_cf

Appends an AND WHERE condition. The value is stored as a bound parameter and emitted as a `?` placeholder in the SQL — no manual quoting required.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `operator` | SQL comparison operator (`=`, `<>`, `<`, `>`, `<=`, `>=`, `LIKE`, etc.) |
| `value` | Bound value |

**Example**

```
_query = QueryWhere_cf ( _query ; "CONTACT.status" ; "=" ; "Active" )
```

---

### QueryOrWhere_cf

Identical to `QueryWhere_cf` but joins the condition to the previous clause with OR rather than AND.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryWhere_cf   ( _query ; "CONTACT.status" ; "=" ; "Active" ) ;
_query = QueryOrWhere_cf ( _query ; "CONTACT.status" ; "=" ; "Prospect" )
// → WHERE CONTACT.status = ? OR CONTACT.status = ?
```

---

### QueryWhereIn_cf

Appends an AND WHERE … IN (…) condition. Each value in the ¶-delimited list is stored as its own bound parameter, so the number of `?` placeholders in the generated SQL matches the number of values exactly.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhereIn_cf ( _query ; "CONTACT.type" ; "customer¶prospect¶partner" )
// → WHERE CONTACT.type IN (?, ?, ?)
```

---

### QueryWhereNull_cf

Appends AND column IS NULL. No binding is added because the test is against SQL NULL, not a parameterised value.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhereNull_cf ( _query ; "CONTACT.deletedAt" )
// → WHERE CONTACT.deletedAt IS NULL
```

---

### QueryWhereNotNull_cf

Appends AND column IS NOT NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhereNotNull_cf ( _query ; "CONTACT.emailWork" )
// → WHERE CONTACT.emailWork IS NOT NULL
```

---

### QueryJoin_cf

Appends an INNER JOIN clause. The join condition is specified as a three-part ON expression: `first operator second`.

The join table name is stored pre-quoted. `first` and `second` accept `Table::Field` format and are converted to quoted dot notation automatically, identical to `QueryWhere_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table occurrence name to join — plain string or `GetFieldName()` result from that table |
| `first` | Left-hand side of the ON condition — `Table::Field` or plain SQL expression |
| `operator` | Join condition operator (typically `=`) |
| `second` | Right-hand side of the ON condition — `Table::Field` or plain SQL expression |

**Example**

```
_query = QueryJoin_cf ( _query ; GetFieldName ( invoice__ITEM::__kptID ) ; GetFieldName ( CONTACT::_kftItemID ) ; "=" ; GetFieldName ( invoice__ITEM::__kptID ) )
// → INNER JOIN "invoice__ITEM" ON "CONTACT"."_kftItemID" = "invoice__ITEM"."__kptID"
```

---

### QueryLeftJoin_cf

Identical to `QueryJoin_cf` but produces a LEFT JOIN, returning all rows from the left table even when no matching row exists in the joined table.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table occurrence name to join — plain string or `GetFieldName()` result from that table |
| `first` | Left-hand side of the ON condition — `Table::Field` or plain SQL expression |
| `operator` | Join condition operator |
| `second` | Right-hand side of the ON condition — `Table::Field` or plain SQL expression |

**Example**

```
_query = QueryLeftJoin_cf ( _query ; GetFieldName ( contact__INVOICE::__kptID ) ; GetFieldName ( CONTACT::_kftInvoiceID ) ; "=" ; GetFieldName ( contact__INVOICE::__kptID ) )
// → LEFT JOIN "contact__INVOICE" ON "CONTACT"."_kftInvoiceID" = "contact__INVOICE"."__kptID"
```

---

### QueryOrderBy_cf

Appends an ORDER BY column. Call multiple times to sort by multiple columns — they are emitted in the order added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `direction` | `ASC` or `DESC` — defaults to `ASC` when empty |

**Example**

```
_query = QueryOrderBy_cf ( _query ; "CONTACT.lastName" ; "ASC" ) ;
_query = QueryOrderBy_cf ( _query ; "CONTACT.firstName" ; "ASC" )
// → ORDER BY CONTACT.lastName ASC, CONTACT.firstName ASC
```

---

### QueryGroupBy_cf

Appends a GROUP BY column. Call multiple times to group by multiple columns — they are emitted in the order added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryGroupBy_cf ( _query ; "CONTACT.type" )
// → GROUP BY CONTACT.type
```

---

### QueryHaving_cf

Appends an AND HAVING condition. The value is stored as a bound parameter. Must be used after `QueryGroupBy_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference or aggregate expression (e.g. `COUNT(*)`) |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryGroupBy_cf ( _query ; "CONTACT.type" ) ;
_query = QueryHaving_cf  ( _query ; "COUNT(*)" ; ">" ; 5 )
// → GROUP BY CONTACT.type HAVING COUNT(*) > ?
```

---

### QueryLimit_cf

Sets the maximum number of rows to return. Translates to `FETCH FIRST n ROWS ONLY` in FileMaker's SQL dialect — `LIMIT` is not valid syntax.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `value` | Maximum number of rows |

**Example**

```
_query = QueryLimit_cf ( _query ; 50 )
// → FETCH FIRST 50 ROWS ONLY
```

---

### QueryOffset_cf

Sets the number of rows to skip before returning results. Translates to `OFFSET n ROWS`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `value` | Number of rows to skip |

**Example**

```
_query = QueryOffset_cf ( _query ; 100 )
// → OFFSET 100 ROWS
```

---

### QueryGet_cf

Executes the assembled query and returns the result. Bound values are injected at execution time using `Evaluate ( ExecuteSQL ( ... ) )`, so the number of parameters is determined dynamically regardless of how many were added.

Returns an empty string if `ExecuteSQL` signals an error (i.e. when its result begins with `?`).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |
| `fieldSeparator` | Character(s) placed between field values within a row |
| `rowSeparator` | Character(s) placed between rows |

**Example**

```
Let
(
[
_query  = QueryNew_cf    ( "CONTACT" ) ;
_query  = QueryWhere_cf  ( _query ; "CONTACT.status" ; "=" ; "Active" ) ;
_query  = QueryLimit_cf  ( _query ; 25 ) ;
_result = QueryGet_cf    ( _query ; "," ; "¶" )
];
_result
)
```

---

### QueryGetResultsAsJson_cf

Executes the query and returns the results as a JSON array of objects, one object per row. Property names are derived automatically from the column input originally passed to `QuerySelect_cf` — no separate key list is required.

`QuerySelect_cf` stores a `selectKeys` field alongside `selects` in the query object. For each column, the key is extracted from the original (pre-conversion) expression: the part after `::` for `Table::Field` names, the part after `.` for dot-notation, or the expression as-is for anything else (e.g. `*`, `COUNT(*)`).

Uses `Char(28)` as the internal field separator (safe for typical data) and `¶` as the row separator. Returns `"[]"` when the query produces no rows or an error.

> **Note:** All field values are stored as JSON strings. If you need numeric types in the output, parse the string values after receiving the result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |

**Example**

```
Let
(
[
_query  = QueryNew_cf    ( "CONTACT" ) ;
_query  = QuerySelect_cf ( _query ; List ( GetFieldName ( CONTACT::PrimaryKey ) ; GetFieldName ( CONTACT::FullName ) ; GetFieldName ( CONTACT::Status ) ) ) ;
_query  = QueryWhere_cf  ( _query ; CONTACT::Status ; "=" ; "Active" ) ;
_result = QueryGetResultsAsJson_cf ( _query )
];
_result
// → [{"PrimaryKey":"1","FullName":"Jane Smith","Status":"Active"},{"PrimaryKey":"2",...}]
)
```

---

### QueryToSQL_cf

Returns the assembled SQL string without executing it. Bound parameters appear as `?` placeholders. Useful for verifying query structure during development.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
Let
(
[
_query = QueryNew_cf    ( "CONTACT" ) ;
_query = QuerySelect_cf ( _query ; "CONTACT.id, CONTACT.firstName" ) ;
_query = QueryWhere_cf  ( _query ; "CONTACT.status" ; "=" ; "Active" ) ;
_query = QueryOrderBy_cf ( _query ; "CONTACT.lastName" ; "ASC" ) ;
_sql   = QueryToSQL_cf  ( _query )
];
_sql
)
// → SELECT CONTACT.id, CONTACT.firstName FROM CONTACT
//   WHERE CONTACT.status = ? ORDER BY CONTACT.lastName ASC
```

---

## Internal helpers

These functions are called automatically by the public builders and by `QueryToSQL_cf` / `QueryGet_cf`. They are marked `visible = False` in FileMaker's function list and are not intended for direct use.

---

### QueryBuildJoins_cf

Recursively walks the `joins` array and renders the full JOIN clause string.

**Parameters**

| Parameter | Description |
|---|---|
| `joins` | Raw JSON array extracted from the query object |
| `joinCount` | Number of join objects in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildJoins_cf ( JSONGetElement ( _query ; "joins" ) ; JSONGetElement ( _query ; "joinCount" ) ; 0 )
// → "INNER JOIN invoice__ITEM ON CONTACT.id = invoice__ITEM.idContact"
```

---

### QueryBuildWheres_cf

Recursively walks the `wheres` array and renders the WHERE clause body (excluding the `WHERE` keyword). Delegates to `QueryBuildWhereBooleanPrefix_cf` for AND/OR connectors and to `QueryBuildInPlaceholders_cf` for IN placeholders.

**Parameters**

| Parameter | Description |
|---|---|
| `wheres` | Raw JSON array extracted from the query object |
| `whereCount` | Number of where objects in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildWheres_cf ( JSONGetElement ( _query ; "wheres" ) ; JSONGetElement ( _query ; "whereCount" ) ; 0 )
// → "CONTACT.status = ? AND CONTACT.type IN (?, ?)"
```

---

### QueryBuildInPlaceholders_cf

Recursively produces N comma-separated `?` placeholders for use in an IN clause.

**Parameters**

| Parameter | Description |
|---|---|
| `count` | Total number of placeholders to produce |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildInPlaceholders_cf ( 3 ; 0 )
// → "?, ?, ?"
```

---

### QueryBuildGroupBys_cf

Recursively walks the `groupBys` array and renders the GROUP BY column list.

**Parameters**

| Parameter | Description |
|---|---|
| `groupBys` | Raw JSON array extracted from the query object |
| `groupByCount` | Number of column strings in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildGroupBys_cf ( JSONGetElement ( _query ; "groupBys" ) ; JSONGetElement ( _query ; "groupByCount" ) ; 0 )
// → "CONTACT.type, CONTACT.status"
```

---

### QueryBuildHavings_cf

Recursively walks the `havings` array and renders the HAVING clause body (excluding the `HAVING` keyword).

**Parameters**

| Parameter | Description |
|---|---|
| `havings` | Raw JSON array extracted from the query object |
| `havingCount` | Number of having objects in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildHavings_cf ( JSONGetElement ( _query ; "havings" ) ; JSONGetElement ( _query ; "havingCount" ) ; 0 )
// → "COUNT(*) > ?"
```

---

### QueryBuildOrderBys_cf

Recursively walks the `orderBys` array and renders the ORDER BY column list.

**Parameters**

| Parameter | Description |
|---|---|
| `orderBys` | Raw JSON array extracted from the query object |
| `orderByCount` | Number of orderBy objects in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildOrderBys_cf ( JSONGetElement ( _query ; "orderBys" ) ; JSONGetElement ( _query ; "orderByCount" ) ; 0 )
// → "CONTACT.lastName ASC, CONTACT.firstName ASC"
```

---

### QueryBuildBindingArgs_cf

Recursively walks the `bindings` array and renders the bound values as a text fragment for insertion into an `Evaluate` expression. Each value is wrapped in `Quote()` so special characters are safely escaped.

**Parameters**

| Parameter | Description |
|---|---|
| `bindings` | Raw JSON array extracted from the query object |
| `bindingCount` | Number of binding values in the array |
| `index` | Current position — always call with `0` |

**Example**

```
QueryBuildBindingArgs_cf ( JSONGetElement ( _query ; "bindings" ) ; JSONGetElement ( _query ; "bindingCount" ) ; 0 )
// → "\"Active\" ; \"customer\" ; \"prospect\""
// (inserted into the Evaluate expression as literal FM string arguments)
```

---

### QueryBuildWhereBooleanPrefix_cf

Returns the boolean connector that precedes a WHERE or HAVING clause at a given position. Returns an empty string for the first clause (`index = 0`), `" AND "` for subsequent AND clauses, and `" OR "` for OR clauses.

**Parameters**

| Parameter | Description |
|---|---|
| `boolean` | The stored boolean value for the clause — `"and"` or `"or"` |
| `index` | Position of the clause in its array — `0` suppresses the connector |

**Example**

```
QueryBuildWhereBooleanPrefix_cf ( "and" ; 0 )   // → ""
QueryBuildWhereBooleanPrefix_cf ( "and" ; 1 )   // → " AND "
QueryBuildWhereBooleanPrefix_cf ( "or" ; 2 )    // → " OR "
```

---

### QueryAppendBindings_cf

Recursively appends values from a ¶-delimited list to the `bindings` array inside the query object, incrementing `bindingCount` with each addition. Called by `QueryWhereIn_cf` to add N bindings in a single pass.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `values` | ¶-delimited list of values to append |
| `valueCount` | Total number of values in the list |
| `index` | Current position — always call with `1` (`GetValue` is 1-based) |

**Example**

```
// Appends "customer", "prospect", "partner" to the bindings array
QueryAppendBindings_cf ( _query ; "customer¶prospect¶partner" ; 3 ; 1 )
```

---

### QueryBuildSelects_cf

Recursively converts a ¶-delimited column list to a SQL column expression string. FileMaker fully-qualified names in `Table::Field` format are converted to quoted dot notation (`"Table"."Field"`) using `Char(34)` for the double-quote character. Expressions without `::` pass through unchanged. Called by `QuerySelect_cf`; do not call directly.

**Parameters**

| Parameter | Description |
|---|---|
| `columns` | ¶-delimited list of column expressions |
| `columnCount` | Total number of columns |
| `index` | Current position (call with `1`; `GetValue` is 1-based) |

**Example**

```
// Input:  "FMORM::PrimaryKey¶FMORM::CreatedBy"
// Output: "\"FMORM\".\"PrimaryKey\", \"FMORM\".\"CreatedBy\""
QueryBuildSelects_cf ( "FMORM::PrimaryKey¶FMORM::CreatedBy" ; 2 ; 1 )
```

---

### QueryConvertField_cf

Converts a single FileMaker fully-qualified field name (`Table::Field`) to a quoted SQL dot-notation identifier (`"Table"."Field"`). Uses `Quote()` for readability and automatic escaping. Expressions that do not contain `::` pass through unchanged — `*`, `COUNT(*)`, and already-converted strings are safe to pass in. Called by `QueryBuildSelects_cf` and by all public builders that accept column references.

You can also call this directly when building complex SQL expressions (aggregate functions, arithmetic) that the builder functions can't assemble automatically. The recommended pattern is `QueryConvertField_cf ( GetFieldName ( TABLE::field ) )` — the `GetFieldName()` call produces a `Table::Field` string that survives field renames.

**Parameters**

| Parameter | Description |
|---|---|
| `field` | A `Table::Field` string (e.g. from `GetFieldName()`), or any plain SQL expression — anything without `::` passes through unchanged |

**Example**

```
QueryConvertField_cf ( GetFieldName ( FMORM::PrimaryKey ) )   // → "FMORM"."PrimaryKey"
QueryConvertField_cf ( "CONTACT.status" )                     // → CONTACT.status  (pass-through)
QueryConvertField_cf ( "*" )                                  // → *               (pass-through)

// Hand-building an aggregate expression — each component rename-safe:
"SUM( "
& QueryConvertField_cf ( GetFieldName ( BUDGET_HISTORY::originalBudgetTotalCost ) ) & " * "
& QueryConvertField_cf ( GetFieldName ( BUDGET_HISTORY::contingencyRundown ) )
& " )"
// → SUM( "BUDGET_HISTORY"."originalBudgetTotalCost" * "BUDGET_HISTORY"."contingencyRundown" )
```

---

### QueryBuildJsonRow_cf

Recursively builds a single JSON object from a row of field values and a parallel list of key names. Both `fields` and `keys` are ¶-delimited; `fields` comes from splitting a raw result row on `Char(28)`. Called by `QueryBuildJsonRows_cf`; do not call directly.

**Parameters**

| Parameter | Description |
|---|---|
| `obj` | Accumulating JSON object — call with `"{}"` |
| `fields` | ¶-delimited field values for the current row |
| `keys` | ¶-delimited JSON property names |
| `keyCount` | Total number of keys/fields |
| `index` | Current position (call with `1`; `GetValue` is 1-based) |

**Example**

```
// Input fields: "42¶Jane Smith¶Active"
// Input keys:   "id¶name¶status"
QueryBuildJsonRow_cf ( "{}" ; "42¶Jane Smith¶Active" ; "id¶name¶status" ; 3 ; 1 )
// → {"id":"42","name":"Jane Smith","status":"Active"}
```

---

### QueryBuildJsonRows_cf

Recursively appends row objects to a JSON array. Splits each raw row on `Char(28)` to recover individual field values, delegates object construction to `QueryBuildJsonRow_cf`, then inserts the result into the accumulating array at the correct 0-based index. Called by `QueryGetResultsAsJson_cf`; do not call directly.

**Parameters**

| Parameter | Description |
|---|---|
| `result` | Accumulating JSON array — call with `"[]"` |
| `rawResult` | Full ExecuteSQL output (`Char(28)` field sep, `¶` row sep) |
| `rowCount` | Total number of rows |
| `keys` | ¶-delimited JSON property names |
| `keyCount` | Total number of keys/fields |
| `rowIndex` | Current row position (call with `1`; `GetValue` is 1-based) |

**Example**

```
// Typically called internally by QueryGetResultsAsJson_cf:
QueryBuildJsonRows_cf ( "[]" ; _rawResult ; _rowCount ; "id¶name" ; 2 ; 1 )
// → [{"id":"1","name":"Alice"},{"id":"2","name":"Bob"}]
```

---

### QueryBuildSelectKeys_cf

Recursively extracts a plain key name from each column expression in a ¶-delimited list, for use as JSON object property names. Operates on the **original** input to `QuerySelect_cf` before SQL conversion, so it sees `Table::Field` or `Table.field` strings rather than quoted SQL identifiers. Called by `QuerySelect_cf` to populate `selectKeys` in the query object; do not call directly.

Extraction rules:
- `Table::Field` → `Field` (take the part after `::`)
- `Table.field` → `field` (take the part after `.`)
- Anything else → as-is (e.g. `*`, `COUNT(*)`)

**Parameters**

| Parameter | Description |
|---|---|
| `columns` | ¶-delimited list of column expressions (original input, before SQL conversion) |
| `columnCount` | Total number of columns |
| `index` | Current position (call with `1`; `GetValue` is 1-based) |

**Example**

```
// Input: "CONTACT::PrimaryKey¶CONTACT::FullName¶CONTACT::Status"
QueryBuildSelectKeys_cf ( "CONTACT::PrimaryKey¶CONTACT::FullName¶CONTACT::Status" ; 3 ; 1 )
// → "PrimaryKey¶FullName¶Status"
```

---

## Utility functions

---

### JSONGetElementLikeField_cf

Retrieves a value from a JSON object by deriving the property name from a FileMaker field reference or field-name string. This bridges the gap between FileMaker's `Table::Field` naming convention and JSON property keys — you can pass the same field reference you use elsewhere in your calculation and the function resolves the key automatically.

Property name resolution happens in this priority order:

1. **Real FM field reference** — if `GetFieldName( field )` returns a non-empty value, the table occurrence prefix (everything before `::`) is stripped and the bare field name is used as the key.
2. **String containing `::`** — if the `field` value contains `::` (e.g. `"CONTACT::firstName"`), the part after `::` is used.
3. **Fallback** — the `field` value is used as-is, assumed to already be the target property name.

Returns `"?"` if `json` does not pass JSON validation (i.e. `JSONFormatElements` signals an error).

> **Note on path 1:** FileMaker evaluates CF parameters before passing them in, so a bare `Table::Field` reference becomes the field's *value* inside the function. Path 1 is most useful when the caller explicitly passes `GetFieldName( Table::Field )` as the `field` argument — the resulting `"Table::Field"` string then also satisfies path 2. In practice, paths 2 and 3 are the most commonly triggered.

**Parameters**

| Parameter | Description |
|---|---|
| `json` | A valid JSON object string |
| `field` | A FileMaker field reference, a `"Table::Field"` string, or a plain property name string |

**Examples**

```
// Path 2 — passing GetFieldName() result as a string
JSONGetElementLikeField_cf ( _json ; GetFieldName ( CONTACT::firstName ) )
// field = "CONTACT::firstName" → property resolved to "firstName"

// Path 2 — passing a qualified string literal
JSONGetElementLikeField_cf ( _json ; "CONTACT::firstName" )
// → same result

// Path 3 — plain property name
JSONGetElementLikeField_cf ( _json ; "firstName" )
// → JSONGetElement( _json ; "firstName" )

// Invalid JSON — returns "?"
JSONGetElementLikeField_cf ( "not json" ; "firstName" )
// → "?"
```
