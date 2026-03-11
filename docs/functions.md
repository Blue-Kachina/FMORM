# fmorm Function Reference

---

## Table of Contents

### Public builders

| Function | Purpose |
|---|---|
| [QueryNew\_cf](#querynew_cf) | Initialise a new query object |
| [QuerySelect\_cf](#queryselect_cf) | Set or extend the SELECT column list |
| [QuerySelectSub\_cf](#queryselectsub_cf) | Add a subquery expression to the SELECT list |
| [QueryDistinct\_cf](#querydistinct_cf) | Add SELECT DISTINCT |
| [QueryWhere\_cf](#querywhere_cf) | Append AND WHERE condition |
| [QueryOrWhere\_cf](#queryorwhere_cf) | Append OR WHERE condition |
| [QueryWhereIn\_cf](#querywherein_cf) | Append AND WHERE column IN (…) |
| [QueryWhereNotIn\_cf](#querywherenotin_cf) | Append AND WHERE column NOT IN (…) |
| [QueryOrWhereIn\_cf](#queryorwherein_cf) | Append OR WHERE column IN (…) |
| [QueryWhereNull\_cf](#querywherenull_cf) | Append AND column IS NULL |
| [QueryWhereNotNull\_cf](#querywherenotnull_cf) | Append AND column IS NOT NULL |
| [QueryOrWhereNull\_cf](#queryorwherenull_cf) | Append OR column IS NULL |
| [QueryOrWhereNotNull\_cf](#queryorwherenotnull_cf) | Append OR column IS NOT NULL |
| [QueryWhereBetween\_cf](#querywherebetween_cf) | Append AND column BETWEEN low AND high |
| [QueryWhereNotBetween\_cf](#querywherenotbetween_cf) | Append AND column NOT BETWEEN low AND high |
| [QueryOrWhereBetween\_cf](#queryorwherebetween_cf) | Append OR column BETWEEN low AND high |
| [QueryOrWhereNotBetween\_cf](#queryorwherenotbetween_cf) | Append OR column NOT BETWEEN low AND high |
| [QueryWhereColumn\_cf](#querywherecolumn_cf) | Append AND column1 op column2 (column comparison, no binding) |
| [QueryWhereGroup\_cf](#querywheregroup_cf) | Append AND (grouped conditions from another query) |
| [QueryOrWhereGroup\_cf](#queryorwheregroup_cf) | Append OR (grouped conditions from another query) |
| [QueryWhereRaw\_cf](#querywhereraw_cf) | Append AND (raw SQL expression) |
| [QueryOrWhereRaw\_cf](#queryorwhereraw_cf) | Append OR (raw SQL expression) |
| [QueryWhereInSubquery\_cf](#querywhereinsubquery_cf) | Append AND column IN (subquery) |
| [QueryWhereNotInSubquery\_cf](#querywherenotinsubquery_cf) | Append AND column NOT IN (subquery) |
| [QueryWhereExists\_cf](#querywhereexists_cf) | Append AND EXISTS (subquery) |
| [QueryWhereNotExists\_cf](#querywherenotexists_cf) | Append AND NOT EXISTS (subquery) |
| [QueryFromSubquery\_cf](#queryfromsubquery_cf) | Replace FROM table with a derived table (subquery) |
| [QueryJoin\_cf](#queryjoin_cf) | Append INNER JOIN |
| [QueryLeftJoin\_cf](#queryleftjoin_cf) | Append LEFT JOIN |
| [QueryRightJoin\_cf](#queryrightjoin_cf) | Append RIGHT JOIN |
| [QueryCrossJoin\_cf](#querycrossjoin_cf) | Append CROSS JOIN |
| [QueryJoinSub\_cf](#queryjoinsub_cf) | Append INNER JOIN (subquery) |
| [QueryLeftJoinSub\_cf](#queryleftjoinsub_cf) | Append LEFT JOIN (subquery) |
| [QueryOrderBy\_cf](#queryorderby_cf) | Append ORDER BY column |
| [QueryOrderByRaw\_cf](#queryorderbyraw_cf) | Append ORDER BY raw expression |
| [QueryReorder\_cf](#queryreorder_cf) | Clear all ORDER BY clauses |
| [QueryGroupBy\_cf](#querygroupby_cf) | Append GROUP BY column |
| [QueryGroupByRaw\_cf](#querygroupbyraw_cf) | Append GROUP BY raw expression |
| [QueryHaving\_cf](#queryhaving_cf) | Append AND HAVING condition |
| [QueryOrHaving\_cf](#queryorhaving_cf) | Append OR HAVING condition |
| [QueryHavingRaw\_cf](#queryhavingraw_cf) | Append AND HAVING raw expression |
| [QueryOrHavingRaw\_cf](#queryorhavingraw_cf) | Append OR HAVING raw expression |
| [QueryLimit\_cf](#querylimit_cf) | Set the row limit |
| [QueryOffset\_cf](#queryoffset_cf) | Set the row offset |
| [QueryForPage\_cf](#queryforpage_cf) | Set limit and offset for a specific page number |
| [QueryUnion\_cf](#queryunion_cf) | Append UNION or UNION ALL |
| [QueryGet\_cf](#queryget_cf) | Execute the query and return results |
| [QueryGetResultsAsJson\_cf](#querygetresultsasjson_cf) | Execute the query and return results as a JSON array of objects |
| [QueryToSQL\_cf](#querytosql_cf) | Return the assembled SQL string (debug) |
| [QueryCount\_cf](#querycount_cf) | Execute SELECT COUNT(*) and return the count |
| [QuerySum\_cf](#querysum_cf) | Execute SELECT SUM(column) and return the sum |
| [QueryAvg\_cf](#queryavg_cf) | Execute SELECT AVG(column) and return the average |
| [QueryMax\_cf](#querymax_cf) | Execute SELECT MAX(column) and return the maximum |
| [QueryMin\_cf](#querymin_cf) | Execute SELECT MIN(column) and return the minimum |
| [QueryWhen\_cf](#querywhen_cf) | Conditionally apply query modifications |

### Utility functions

| Function | Purpose |
|---|---|
| [JSONGetElementLikeField\_cf](#jsongetelementlikefield_cf) | Get a JSON element using a FileMaker field reference or field-name string as the property key; optional index for array input |

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
| [QueryBuildUnions\_cf](#querybuildunions_cf) | Recursively render UNION / UNION ALL clauses |
| [QueryBuildBindingArgs\_cf](#querybuildbindingargs_cf) | Render binding values for Evaluate injection |
| [QueryBuildWhereBooleanPrefix\_cf](#querybuildwherebooleanprefix_cf) | Render AND / OR / empty connector |
| [QueryAppendBindings\_cf](#queryappendbindings_cf) | Recursively append N values to the bindings array |
| [QueryMergeBindings\_cf](#querymergebindings_cf) | Append N bindings from a JSON array into the outer query |
| [QueryPrependBindings\_cf](#queryprependbindings_cf) | Rebuild the bindings array with subquery bindings first |
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
| `table` | Table occurrence name. Accepts a plain string (`"CONTACT"`), a direct FM field reference (`CONTACT::anyField`), or a `GetFieldName()` result. When a `Table::Field` string or field reference is passed, the table part is extracted automatically. |

**Example**

```
// Direct field reference — no GetFieldName() wrapper needed
_query = QueryNew_cf ( CONTACT::__kptID )

// GetFieldName() — rename-safe alternative
_query = QueryNew_cf ( GetFieldName ( CONTACT::__kptID ) )

// Plain string — also valid
_query = QueryNew_cf ( "CONTACT" )
```

---

### QuerySelect_cf

Sets or extends the SELECT column list. The first call after `QueryNew_cf` replaces the default `SELECT *` sentinel. Each subsequent call **appends** to the existing column list.

Accepts a ¶-delimited list (e.g. from `List()` and `GetFieldName()`) or a comma-separated string. `Table::Field` names are converted to `"Table"."Field"`. Expressions without `::` pass through unchanged — `*`, aggregates, `CASE`, raw SQL, etc. No separate `QuerySelectRaw_cf` is needed.

Also stores `selectKeys` in the query object (plain field names, used by `QueryGetResultsAsJson_cf` to name JSON properties).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `columns` | ¶-delimited list from `List()` / `GetFieldName()`, or a comma-separated SQL column string |

**Example**

```
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreatedBy ) ) )

// Additive — two calls accumulate both columns
_query = QuerySelect_cf ( _query ; GetFieldName ( FMORM::PrimaryKey ) ) ;
_query = QuerySelect_cf ( _query ; "COUNT(*) AS total" )
// → SELECT "FMORM"."PrimaryKey", COUNT(*) AS total
```

---

### QuerySelectSub_cf

Adds a subquery expression to the SELECT list: `(SELECT …) AS alias`. The alias becomes the JSON property name when using `QueryGetResultsAsJson_cf`. The subquery's bindings are prepended to the outer query's bindings (SELECT comes before WHERE in SQL).

> **FileMaker compatibility:** Subqueries in SELECT require FileMaker 17+.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `subquery` | A fully-assembled fmorm query object |
| `alias` | Plain SQL identifier for the subquery column, e.g. `"totalAmount"` — stored as the JSON key |

**Example**

```
// Subquery: count of line items per invoice
_inner = QueryNew_cf    ( "LINE_ITEM" ) ;
_inner = QuerySelect_cf ( _inner ; "COUNT(*)" ) ;
_inner = QueryWhereColumn_cf ( _inner ; "LINE_ITEM.invoiceId" ; "=" ; "INVOICE.id" ) ;

_query = QueryNew_cf       ( "INVOICE" ) ;
_query = QuerySelect_cf    ( _query ; GetFieldName ( INVOICE::id ) ) ;
_query = QuerySelectSub_cf ( _query ; _inner ; "lineItemCount" )
// → SELECT "INVOICE"."id", (SELECT COUNT(*) FROM "LINE_ITEM" …) AS "lineItemCount"
```

---

### QueryDistinct_cf

Adds `SELECT DISTINCT` to the query, eliminating duplicate rows from the result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_query = QueryNew_cf    ( "CONTACT" ) ;
_query = QuerySelect_cf ( _query ; GetFieldName ( CONTACT::country ) ) ;
_query = QueryDistinct_cf ( _query )
// → SELECT DISTINCT "CONTACT"."country" FROM "CONTACT"
```

---

### QueryWhere_cf

Appends an AND WHERE condition with a bound parameter.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference — a direct FM field reference, `GetFieldName()` result, or plain SQL expression |
| `operator` | SQL comparison operator (`=`, `<>`, `<`, `>`, `<=`, `>=`, `LIKE`, etc.) |
| `value` | Bound value |

**Example**

```
_query = QueryWhere_cf ( _query ; CONTACT::status ; "=" ; "Active" )
// → WHERE "CONTACT"."status" = ?
```

---

### QueryOrWhere_cf

Identical to `QueryWhere_cf` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryWhere_cf   ( _query ; CONTACT::status ; "=" ; "Active" ) ;
_query = QueryOrWhere_cf ( _query ; CONTACT::status ; "=" ; "Prospect" )
// → WHERE "CONTACT"."status" = ? OR "CONTACT"."status" = ?
```

---

### QueryWhereIn_cf

Appends AND column IN (?, ?, …). Each value in the ¶-delimited list becomes its own bound parameter.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhereIn_cf ( _query ; CONTACT::type ; "customer¶prospect¶partner" )
// → WHERE "CONTACT"."type" IN (?, ?, ?)
```

---

### QueryWhereNotIn_cf

Appends AND column NOT IN (?, ?, …). Each value becomes its own bound parameter.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhereNotIn_cf ( _query ; CONTACT::status ; "Archived¶Deleted" )
// → WHERE "CONTACT"."status" NOT IN (?, ?)
```

---

### QueryOrWhereIn_cf

Appends OR column IN (?, ?, …).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhere_cf     ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryOrWhereIn_cf ( _query ; CONTACT::type ; "partner¶reseller" )
// → WHERE "CONTACT"."region" = ? OR "CONTACT"."type" IN (?, ?)
```

---

### QueryWhereNull_cf

Appends AND column IS NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhereNull_cf ( _query ; CONTACT::deletedAt )
// → WHERE "CONTACT"."deletedAt" IS NULL
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
_query = QueryWhereNotNull_cf ( _query ; CONTACT::emailWork )
// → WHERE "CONTACT"."emailWork" IS NOT NULL
```

---

### QueryOrWhereNull_cf

Appends OR column IS NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhere_cf     ( _query ; CONTACT::status ; "=" ; "Active" ) ;
_query = QueryOrWhereNull_cf ( _query ; CONTACT::status )
// → WHERE "CONTACT"."status" = ? OR "CONTACT"."status" IS NULL
```

---

### QueryOrWhereNotNull_cf

Appends OR column IS NOT NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryOrWhereNotNull_cf ( _query ; CONTACT::emailWork )
// → OR "CONTACT"."emailWork" IS NOT NULL
```

---

### QueryWhereBetween_cf

Appends AND column BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound (bound parameter) |
| `high` | Upper bound (bound parameter) |

**Example**

```
_query = QueryWhereBetween_cf ( _query ; INVOICE::amount ; 100 ; 500 )
// → WHERE "INVOICE"."amount" BETWEEN ? AND ?
```

---

### QueryWhereNotBetween_cf

Appends AND column NOT BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound |
| `high` | Upper bound |

**Example**

```
_query = QueryWhereNotBetween_cf ( _query ; INVOICE::amount ; 100 ; 500 )
// → WHERE "INVOICE"."amount" NOT BETWEEN ? AND ?
```

---

### QueryOrWhereBetween_cf

Appends OR column BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound |
| `high` | Upper bound |

---

### QueryOrWhereNotBetween_cf

Appends OR column NOT BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound |
| `high` | Upper bound |

---

### QueryWhereColumn_cf

Appends AND first operator second comparing two columns directly. No binding is added — both sides are SQL identifiers. Both `first` and `second` accept the same field reference formats as other column parameters.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `first` | Left-hand column reference |
| `operator` | SQL comparison operator (`=`, `<>`, `<`, `>`, etc.) |
| `second` | Right-hand column reference |

**Example**

```
_query = QueryWhereColumn_cf ( _query ; INVOICE::contactId ; "=" ; CONTACT::id )
// → WHERE "INVOICE"."contactId" = "CONTACT"."id"
```

---

### QueryWhereGroup_cf

Appends AND (grouped conditions) by wrapping the WHERE conditions from `groupedQuery` in parentheses. Build `groupedQuery` using any combination of `QueryWhere_cf`, `QueryOrWhere_cf`, etc. on any query object — only its `wheres` array and bindings are used; its FROM, SELECT, and other clauses are ignored.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object to append to |
| `groupedQuery` | A query object whose WHERE conditions form the group |

**Example**

```
// Build the inner group: (status = ? OR priority = ?)
_g = QueryNew_cf     ( "CONTACT" ) ;
_g = QueryWhere_cf   ( _g ; CONTACT::status ; "=" ; "Active" ) ;
_g = QueryOrWhere_cf ( _g ; CONTACT::priority ; "=" ; "High" ) ;

// Attach the group to the main query
_query = QueryNew_cf       ( "CONTACT" ) ;
_query = QueryWhere_cf     ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryWhereGroup_cf ( _query ; _g )
// → WHERE "CONTACT"."region" = ? AND ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

---

### QueryOrWhereGroup_cf

Identical to `QueryWhereGroup_cf` but joins the group with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `groupedQuery` | A query object whose WHERE conditions form the group |

**Example**

```
_query = QueryOrWhereGroup_cf ( _query ; _g )
// → OR ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

---

### QueryWhereRaw_cf

Appends AND (rawSql) inserting a raw SQL fragment verbatim into the WHERE clause. Useful for expressions that no builder covers (e.g. `CASE`, vendor functions, complex predicates).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression — emitted verbatim inside parentheses |
| `bindings` | *(Optional)* ¶-delimited list of bound values for `?` placeholders in `rawSql`. Pass `""` when there are none. |

**Example**

```
// No bindings
_query = QueryWhereRaw_cf ( _query ; "MONTH(\"INVOICE\".\"date\") = MONTH(CURRENT_DATE)" ; "" )
// → WHERE (MONTH("INVOICE"."date") = MONTH(CURRENT_DATE))

// With bindings
_query = QueryWhereRaw_cf ( _query ; "\"INVOICE\".\"total\" BETWEEN ? AND ?" ; "100¶500" )
// → WHERE ("INVOICE"."total" BETWEEN ? AND ?)
```

---

### QueryOrWhereRaw_cf

Identical to `QueryWhereRaw_cf` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values |

---

### QueryWhereInSubquery_cf

Appends AND column IN (SELECT …) using a fully-assembled fmorm subquery object. The subquery's bindings are appended after the outer query's existing WHERE bindings.

> **FileMaker compatibility:** IN subqueries require FileMaker 17+. Correlated subqueries are not reliably supported.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `column` | Column reference in the outer query |
| `subquery` | A fully-assembled fmorm query object |

**Example**

```
_inner = QueryNew_cf    ( "CONTACT" ) ;
_inner = QuerySelect_cf ( _inner ; "CONTACT.id" ) ;
_inner = QueryWhere_cf  ( _inner ; CONTACT::status ; "=" ; "Active" ) ;

_query = QueryNew_cf             ( "INVOICE" ) ;
_query = QueryWhereInSubquery_cf ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" IN (SELECT CONTACT.id FROM "CONTACT" WHERE …)
```

---

### QueryWhereNotInSubquery_cf

Appends AND column NOT IN (SELECT …). Same binding semantics as `QueryWhereInSubquery_cf`.

> **FileMaker compatibility:** Requires FileMaker 17+.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `column` | Column reference |
| `subquery` | A fully-assembled fmorm query object |

**Example**

```
_query = QueryWhereNotInSubquery_cf ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" NOT IN (SELECT … )
```

---

### QueryWhereExists_cf

Appends AND EXISTS (SELECT …). The subquery's bindings are appended.

> **FileMaker compatibility:** Requires FileMaker 17+. Correlated subqueries are not reliably supported.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `subquery` | A fully-assembled fmorm query object |

**Example**

```
_inner = QueryNew_cf   ( "INVOICE" ) ;
_inner = QueryWhere_cf ( _inner ; INVOICE::contactId ; "=" ; "some-id" ) ;

_query = QueryNew_cf        ( "CONTACT" ) ;
_query = QueryWhereExists_cf ( _query ; _inner )
// → WHERE EXISTS (SELECT * FROM "INVOICE" WHERE …)
```

---

### QueryWhereNotExists_cf

Appends AND NOT EXISTS (SELECT …). Same semantics as `QueryWhereExists_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `subquery` | A fully-assembled fmorm query object |

---

### QueryFromSubquery_cf

Replaces the FROM table with a derived table: `FROM (SELECT …) alias`. The table name set in `QueryNew_cf` is discarded. The subquery's bindings are prepended automatically.

> **FileMaker compatibility:** Functional in FM 19.x; not formally documented by Claris. Avoid `QueryLimit_cf` / `QueryOffset_cf` on the inner query. See [FileMaker SQL Compatibility Notes](#filemaker-sql-compatibility-notes).

**Parameters**

| Parameter | Description |
|---|---|
| `outerQuery` | Outer query object (its table name is replaced) |
| `subquery` | A fully-assembled fmorm query object to use as the derived table |
| `alias` | Plain SQL identifier for the derived table, e.g. `"sub"` |

**Example**

```
_inner = QueryNew_cf     ( "INVOICE" ) ;
_inner = QuerySelect_cf  ( _inner ; "INVOICE.contactID, MAX(INVOICE.invoiceDate) AS lastDate" ) ;
_inner = QueryGroupBy_cf ( _inner ; "INVOICE.contactID" ) ;

_query = QueryNew_cf          ( "CONTACT" ) ;
_query = QueryFromSubquery_cf ( _query ; _inner ; "recent" ) ;
_query = QueryWhere_cf        ( _query ; "recent.lastDate" ; ">" ; Get ( CurrentDate ) - 30 )
```

---

### QueryJoin_cf

Appends an INNER JOIN clause with an ON condition.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table to join — field reference, `GetFieldName()`, or plain string |
| `first` | Left-hand side of the ON condition |
| `operator` | Join operator (typically `=`) |
| `second` | Right-hand side of the ON condition |

**Example**

```
_query = QueryJoin_cf ( _query ; invoice__ITEM::__kptID ; CONTACT::_kftItemID ; "=" ; invoice__ITEM::__kptID )
// → INNER JOIN "invoice__ITEM" ON "CONTACT"."_kftItemID" = "invoice__ITEM"."__kptID"
```

---

### QueryLeftJoin_cf

Appends a LEFT JOIN clause. Same parameters as `QueryJoin_cf`.

**Example**

```
_query = QueryLeftJoin_cf ( _query ; contact__INVOICE::__kptID ; CONTACT::_kftInvoiceID ; "=" ; contact__INVOICE::__kptID )
// → LEFT JOIN "contact__INVOICE" ON "CONTACT"."_kftInvoiceID" = "contact__INVOICE"."__kptID"
```

---

### QueryRightJoin_cf

Appends a RIGHT JOIN clause. Same parameters as `QueryJoin_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table to join |
| `first` | Left-hand side of the ON condition |
| `operator` | Join operator |
| `second` | Right-hand side of the ON condition |

**Example**

```
_query = QueryRightJoin_cf ( _query ; "INVOICE" ; CONTACT::id ; "=" ; "INVOICE.contactId" )
// → RIGHT JOIN "INVOICE" ON "CONTACT"."id" = INVOICE.contactId
```

---

### QueryCrossJoin_cf

Appends a CROSS JOIN (cartesian product). No ON condition.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table to join — field reference, `GetFieldName()`, or plain string |

**Example**

```
_query = QueryCrossJoin_cf ( _query ; "SIZE" )
// → CROSS JOIN "SIZE"
```

---

### QueryJoinSub_cf

Appends INNER JOIN (SELECT …) alias ON condition. The subquery's bindings are appended after the outer query's existing bindings.

> **Important:** Call before adding WHERE conditions to ensure correct binding order — JOIN bindings must precede WHERE bindings in the SQL.
>
> **FileMaker compatibility:** Requires FileMaker 17+.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `subquery` | A fully-assembled fmorm query object |
| `alias` | Plain SQL identifier for the derived table |
| `first` | Left-hand ON column |
| `operator` | Join operator |
| `second` | Right-hand ON column |

**Example**

```
_inner = QueryNew_cf    ( "LINE_ITEM" ) ;
_inner = QuerySelect_cf ( _inner ; "LINE_ITEM.invoiceId, SUM(LINE_ITEM.amount) AS total" ) ;
_inner = QueryGroupBy_cf ( _inner ; "LINE_ITEM.invoiceId" ) ;

_query = QueryNew_cf    ( "INVOICE" ) ;
_query = QueryJoinSub_cf ( _query ; _inner ; "totals" ; "INVOICE.id" ; "=" ; "totals.invoiceId" )
// → INNER JOIN (SELECT … FROM "LINE_ITEM" GROUP BY …) totals ON INVOICE.id = totals.invoiceId
```

---

### QueryLeftJoinSub_cf

Appends LEFT JOIN (SELECT …) alias ON condition. Same semantics as `QueryJoinSub_cf` but uses a LEFT JOIN.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `subquery` | A fully-assembled fmorm query object |
| `alias` | Plain SQL identifier for the derived table |
| `first` | Left-hand ON column |
| `operator` | Join operator |
| `second` | Right-hand ON column |

---

### QueryOrderBy_cf

Appends an ORDER BY column. Call multiple times to sort by multiple columns in order.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `direction` | `ASC` or `DESC` — defaults to `ASC` when empty |

**Example**

```
_query = QueryOrderBy_cf ( _query ; CONTACT::lastName ; "ASC" ) ;
_query = QueryOrderBy_cf ( _query ; CONTACT::firstName ; "ASC" )
// → ORDER BY "CONTACT"."lastName" ASC, "CONTACT"."firstName" ASC
```

---

### QueryOrderByRaw_cf

Appends a raw SQL expression to the ORDER BY clause. Useful for `RAND()`, `CASE` expressions, or function-based ordering not supported by `QueryOrderBy_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression emitted verbatim in the ORDER BY list |

**Example**

```
_query = QueryOrderByRaw_cf ( _query ; "RAND()" )
// → ORDER BY RAND()
```

---

### QueryReorder_cf

Clears all existing ORDER BY clauses from the query, allowing a fresh ordering to be applied.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_query = QueryOrderBy_cf ( _query ; CONTACT::lastName ; "ASC" ) ;
_query = QueryReorder_cf ( _query ) ;
_query = QueryOrderBy_cf ( _query ; CONTACT::createdAt ; "DESC" )
// Previous ORDER BY discarded; now sorts by createdAt DESC only
```

---

### QueryGroupBy_cf

Appends a GROUP BY column. Call multiple times for multiple grouping columns.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryGroupBy_cf ( _query ; CONTACT::type )
// → GROUP BY "CONTACT"."type"
```

---

### QueryGroupByRaw_cf

Appends a raw SQL expression to the GROUP BY clause. Useful for function-based grouping.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression emitted verbatim in the GROUP BY list |

**Example**

```
_query = QueryGroupByRaw_cf ( _query ; "YEAR(\"INVOICE\".\"date\")" )
// → GROUP BY YEAR("INVOICE"."date")
```

---

### QueryHaving_cf

Appends an AND HAVING condition with a bound parameter. Must be used after `QueryGroupBy_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column or aggregate expression |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryGroupBy_cf ( _query ; "CONTACT.type" ) ;
_query = QueryHaving_cf  ( _query ; "COUNT(*)" ; ">" ; 5 )
// → GROUP BY CONTACT.type HAVING COUNT(*) > ?
```

---

### QueryOrHaving_cf

Identical to `QueryHaving_cf` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column or aggregate expression |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryHaving_cf   ( _query ; "COUNT(*)" ; ">" ; 5 ) ;
_query = QueryOrHaving_cf ( _query ; "SUM(amount)" ; ">" ; 1000 )
// → HAVING COUNT(*) > ? OR SUM(amount) > ?
```

---

### QueryHavingRaw_cf

Appends AND (rawSql) to the HAVING clause verbatim.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values for `?` placeholders. Pass `""` when there are none. |

**Example**

```
_query = QueryHavingRaw_cf ( _query ; "COUNT(*) BETWEEN ? AND ?" ; "5¶20" )
// → HAVING (COUNT(*) BETWEEN ? AND ?)
```

---

### QueryOrHavingRaw_cf

Identical to `QueryHavingRaw_cf` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values |

---

### QueryLimit_cf

Sets the maximum number of rows to return. Emits `FETCH FIRST n ROWS ONLY` (FileMaker's SQL dialect — `LIMIT` is not valid).

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

Sets the number of rows to skip. Emits `OFFSET n ROWS`.

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

### QueryForPage_cf

Convenience function: sets both limit and offset for a specific 1-based page number. Equivalent to calling `QueryLimit_cf` and `QueryOffset_cf` with `offset = (page - 1) * perPage`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `page` | Page number (1-based) |
| `perPage` | Number of rows per page |

**Example**

```
_query = QueryForPage_cf ( _query ; 3 ; 25 )
// → FETCH FIRST 25 ROWS ONLY OFFSET 50 ROWS   (page 3 of 25)
```

---

### QueryUnion_cf

Appends a UNION or UNION ALL clause, combining the results of two queries. The union query's bindings are appended after the main query's bindings.

> **FileMaker compatibility:** Requires FileMaker 17+. Both queries must SELECT the same number of columns. ORDER BY on the combined result is not supported in all FM versions.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Main query object |
| `unionQuery` | A fully-assembled fmorm query object to union |
| `all` | Pass `1` for UNION ALL (keeps duplicates), `0` for UNION (removes duplicates) |

**Example**

```
_q1 = QueryNew_cf    ( "CONTACT" ) ;
_q1 = QuerySelect_cf ( _q1 ; "CONTACT.name, CONTACT.email" ) ;
_q1 = QueryWhere_cf  ( _q1 ; CONTACT::type ; "=" ; "customer" ) ;

_q2 = QueryNew_cf    ( "PROSPECT" ) ;
_q2 = QuerySelect_cf ( _q2 ; "PROSPECT.name, PROSPECT.email" ) ;

_q1 = QueryUnion_cf ( _q1 ; _q2 ; 0 )
// → SELECT … FROM "CONTACT" WHERE … UNION SELECT … FROM "PROSPECT"
```

---

### QueryGet_cf

Executes the assembled query via `ExecuteSQL`. Bound values are injected using `Evaluate ( ExecuteSQL ( … ) )`. Returns `""` on error (when `ExecuteSQL` returns a value beginning with `?`).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |
| `fieldSeparator` | Character(s) placed between field values within a row |
| `rowSeparator` | Character(s) placed between rows |

**Example**

```
_result = QueryGet_cf ( _query ; "," ; "¶" )
```

---

### QueryGetResultsAsJson_cf

Executes the query and returns results as a JSON array of objects, one object per row. Property names come from `selectKeys` stored by `QuerySelect_cf`. Returns `"[]"` on no rows or error. All values are stored as JSON strings.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |

**Example**

```
_result = QueryGetResultsAsJson_cf ( _query )
// → [{"PrimaryKey":"1","FullName":"Jane Smith","Status":"Active"},…]
```

---

### QueryToSQL_cf

Returns the assembled SQL string without executing it. Bound parameters appear as `?`. Output is pretty-printed. Useful during development for verifying query structure.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_sql = QueryToSQL_cf ( _query )
// →
// SELECT
//     "CONTACT"."id",
//     "CONTACT"."firstName"
// FROM
//     "CONTACT"
// WHERE
//     "CONTACT"."status" = ?
// ORDER BY
//     "CONTACT"."lastName" ASC
```

---

### QueryCount_cf

Executes `SELECT COUNT(*)` for the assembled query and returns the count as a number. The original query object is not modified. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object (FROM, WHERE, JOINs already set) |

**Example**

```
_count = QueryCount_cf ( _query )
// Executes: SELECT COUNT(*) FROM … WHERE …
// Returns: 42
```

---

### QuerySum_cf

Executes `SELECT SUM(column)` and returns the sum as a number. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference — field reference, `GetFieldName()`, or SQL expression |

**Example**

```
_total = QuerySum_cf ( _query ; INVOICE::amount )
// Executes: SELECT SUM("INVOICE"."amount") FROM … WHERE …
```

---

### QueryAvg_cf

Executes `SELECT AVG(column)` and returns the average as a number. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_avg = QueryAvg_cf ( _query ; INVOICE::amount )
```

---

### QueryMax_cf

Executes `SELECT MAX(column)` and returns the maximum value as a string. Returns `""` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_latest = QueryMax_cf ( _query ; INVOICE::invoiceDate )
```

---

### QueryMin_cf

Executes `SELECT MIN(column)` and returns the minimum value as a string. Returns `""` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_earliest = QueryMin_cf ( _query ; INVOICE::invoiceDate )
```

---

### QueryWhen_cf

Conditionally applies query modifications. Returns `queryIfTrue` when `condition` is truthy (non-zero, non-empty), otherwise returns the original `query` unchanged.

Because FileMaker evaluates all parameters before calling the function, both branches are always computed. `queryIfTrue` should therefore be built from the same `query` object passed as the first argument.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Base query object |
| `condition` | Any FileMaker expression that evaluates to truthy/falsy |
| `queryIfTrue` | The modified query to use when `condition` is true — typically built from `query` |

**Example**

```
_query = QueryNew_cf ( "CONTACT" ) ;
_query = QueryWhen_cf (
    _query ;
    not IsEmpty ( $$filterStatus ) ;
    QueryWhere_cf ( _query ; CONTACT::status ; "=" ; $$filterStatus )
)
// Adds the WHERE clause only when $$filterStatus is non-empty
```

---

## Internal helpers

These functions are called automatically by the public builders and are marked `visible = False` in FileMaker. They are not intended for direct use.

---

### QueryBuildJoins_cf

Recursively walks the `joins` array and renders the full JOIN clause string. Supports types: `inner`, `left`, `right`, `cross`, `subJoin`, `leftSubJoin`.

**Parameters**

| Parameter | Description |
|---|---|
| `joins` | Raw JSON array from the query object |
| `joinCount` | Number of join objects |
| `index` | Current position — call with `0` |

---

### QueryBuildWheres_cf

Recursively walks the `wheres` array and renders the WHERE clause body (excluding the `WHERE` keyword). Supports types: `basic`, `in`, `notIn`, `null`, `notNull`, `between`, `notBetween`, `column`, `raw`, `group`, `exists`, `notExists`, `inSubquery`, `notInSubquery`.

**Parameters**

| Parameter | Description |
|---|---|
| `wheres` | Raw JSON array from the query object |
| `whereCount` | Number of where objects |
| `index` | Current position — call with `0` |

---

### QueryBuildInPlaceholders_cf

Recursively produces N comma-separated `?` placeholders for IN clauses.

**Parameters**

| Parameter | Description |
|---|---|
| `count` | Total number of placeholders |
| `index` | Current position — call with `0` |

**Example**

```
QueryBuildInPlaceholders_cf ( 3 ; 0 )
// → "?, ?, ?"
```

---

### QueryBuildGroupBys_cf

Recursively walks the `groupBys` array. Regular columns are plain JSON strings; raw expressions are JSON objects `{"type":"raw","sql":"…"}` identified by `Left(item;1)="{"`.

**Parameters**

| Parameter | Description |
|---|---|
| `groupBys` | Raw JSON array from the query object |
| `groupByCount` | Number of entries |
| `index` | Current position — call with `0` |

---

### QueryBuildHavings_cf

Recursively walks the `havings` array. Supports types: default (basic column/operator), `raw`. Handles AND/OR boolean prefix.

**Parameters**

| Parameter | Description |
|---|---|
| `havings` | Raw JSON array from the query object |
| `havingCount` | Number of having objects |
| `index` | Current position — call with `0` |

---

### QueryBuildOrderBys_cf

Recursively walks the `orderBys` array. Supports default (column + direction) and `raw` type entries.

**Parameters**

| Parameter | Description |
|---|---|
| `orderBys` | Raw JSON array from the query object |
| `orderByCount` | Number of orderBy objects |
| `index` | Current position — call with `0` |

---

### QueryBuildUnions_cf

Recursively walks the `unions` array and renders the UNION / UNION ALL clause string. Each union item stores `{sql, all}` where `all` is a boolean.

**Parameters**

| Parameter | Description |
|---|---|
| `unions` | Raw JSON array from the query object |
| `unionCount` | Number of union objects |
| `index` | Current position — call with `0` |

---

### QueryBuildBindingArgs_cf

Recursively walks the `bindings` array and renders the bound values as a text fragment for insertion into an `Evaluate` expression. Each value is wrapped in `Quote()`.

**Parameters**

| Parameter | Description |
|---|---|
| `bindings` | Raw JSON array from the query object |
| `bindingCount` | Number of binding values |
| `index` | Current position — call with `0` |

---

### QueryBuildWhereBooleanPrefix_cf

Returns the boolean connector that precedes a WHERE or HAVING clause. Returns `""` for the first clause, `" AND "` or `" OR "` for subsequent ones.

**Parameters**

| Parameter | Description |
|---|---|
| `boolean` | `"and"` or `"or"` |
| `index` | Position of the clause — `0` suppresses the connector |

---

### QueryAppendBindings_cf

Recursively appends values from a ¶-delimited list to the `bindings` array, incrementing `bindingCount` with each addition.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `values` | ¶-delimited list of values |
| `valueCount` | Total number of values |
| `index` | Current position — call with `1` (`GetValue` is 1-based) |

---

### QueryMergeBindings_cf

Recursively appends binding values from a JSON array into the outer query's `bindings` array.

**Parameters**

| Parameter | Description |
|---|---|
| `outerQuery` | Query object to append bindings into |
| `sourceBindings` | JSON array of binding values |
| `sourceCount` | Number of values |
| `index` | Current position — call with `0` |

---

### QueryPrependBindings_cf

Rebuilds the outer query's `bindings` array as `[prefixBindings…][suffixBindings…]`, ensuring subquery bindings appear before outer-query WHERE bindings when the subquery is in FROM or SELECT position.

**Parameters**

| Parameter | Description |
|---|---|
| `outerQuery` | Query object whose `bindings` array is being rebuilt |
| `prefixBindings` | JSON array to write first (subquery bindings) |
| `prefixCount` | Number of prefix values |
| `suffixBindings` | JSON array to write second (outer query's existing bindings) |
| `suffixCount` | Number of suffix values |
| `index` | Current position — call with `0` |

---

### QueryBuildSelects_cf

Recursively converts a ¶-delimited column list to a SQL column expression string. Delegates to `QueryConvertField_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `columns` | ¶-delimited list of column expressions |
| `columnCount` | Total number of columns |
| `index` | Current position — call with `1` |

---

### QueryConvertField_cf

Converts a `Table::Field` string to `"Table"."Field"`. Expressions without `::` pass through unchanged. Called by all public builders that accept column references.

**Parameters**

| Parameter | Description |
|---|---|
| `field` | A `Table::Field` string, direct FM field reference, or plain SQL expression |

**Example**

```
QueryConvertField_cf ( FMORM::PrimaryKey )                  // → "FMORM"."PrimaryKey"
QueryConvertField_cf ( "*" )                                // → *  (pass-through)
QueryConvertField_cf ( "COUNT(*)" )                         // → COUNT(*)  (pass-through)
```

---

### QueryBuildJsonRow_cf

Builds a single JSON object from parallel ¶-delimited lists of field values and key names.

**Parameters**

| Parameter | Description |
|---|---|
| `obj` | Accumulating JSON object — call with `"{}"` |
| `fields` | ¶-delimited field values for the current row |
| `keys` | ¶-delimited JSON property names |
| `keyCount` | Total number of keys |
| `index` | Current position — call with `1` |

---

### QueryBuildJsonRows_cf

Recursively appends row objects to a JSON array. Called by `QueryGetResultsAsJson_cf`.

**Parameters**

| Parameter | Description |
|---|---|
| `result` | Accumulating JSON array — call with `"[]"` |
| `rawResult` | Full ExecuteSQL output (`Char(28)` field sep, `¶` row sep) |
| `rowCount` | Total number of rows |
| `keys` | ¶-delimited JSON property names |
| `keyCount` | Total number of keys |
| `rowIndex` | Current row position — call with `1` |

---

### QueryBuildSelectKeys_cf

Extracts plain key names from the original column input for use as JSON property names.

Rules: `Table::Field` → `Field`, `Table.field` → `field`, anything else → as-is.

**Parameters**

| Parameter | Description |
|---|---|
| `columns` | ¶-delimited column expressions (original input, before SQL conversion) |
| `columnCount` | Total number of columns |
| `index` | Current position — call with `1` |

---

## Utility functions

---

### JSONGetElementLikeField_cf

Retrieves a value from a JSON object by deriving the property name from a FileMaker field reference or field-name string.

Property name resolution (priority order):
1. `GetFieldName( field )` — strips the table prefix if the result contains `::`
2. `field` contains `::` — strips the table prefix from the string
3. Fallback — uses `field` as-is

When `index` is non-empty, `JSONGetElement( json ; index )` is called first to extract an array element, then the property lookup runs on that result. Returns `"?"` if the working JSON is invalid.

**Parameters**

| Parameter | Description |
|---|---|
| `json` | A valid JSON object or array string |
| `field` | A FileMaker field reference, `"Table::Field"` string, or plain property name |
| `index` | *(Optional — pass `""` to omit)* 0-based array index |

**Examples**

```
// Plain object
JSONGetElementLikeField_cf ( _json ; GetFieldName ( CONTACT::firstName ) ; "" )
// → value of "firstName" property

// Array — index 0
JSONGetElementLikeField_cf ( _jsonArray ; GetFieldName ( CONTACT::firstName ) ; 0 )

// Path 2 — qualified string
JSONGetElementLikeField_cf ( _json ; "CONTACT::firstName" ; "" )

// Path 3 — plain property name
JSONGetElementLikeField_cf ( _json ; "firstName" ; "" )
```

---

## FileMaker SQL Compatibility Notes

FileMaker's `ExecuteSQL` uses a restricted subset of SQL-92.

| Feature | Support |
|---|---|
| IN / NOT IN subqueries — `WHERE col IN (SELECT …)` | FileMaker 17+ |
| EXISTS / NOT EXISTS subqueries | FileMaker 17+ |
| Subqueries in SELECT — `(SELECT …) AS alias` | FileMaker 17+ |
| JOIN subqueries — `JOIN (SELECT …) AS alias` | FileMaker 17+ |
| UNION / UNION ALL | FileMaker 17+ |
| Derived tables — `FROM (SELECT …) AS alias` | Functional in FM 19.x; not formally documented by Claris |
| Correlated subqueries | Not reliably supported — avoid |
| `FETCH FIRST` / `OFFSET` inside a subquery | Unreliable; avoid `QueryLimit_cf` / `QueryOffset_cf` on inner queries |
| RIGHT JOIN | Supported in standard FileMaker SQL |
| CROSS JOIN | Supported in standard FileMaker SQL |
| Window functions / CTEs | Not supported by FileMaker's ExecuteSQL |

**Binding order** is handled automatically. `QueryFromSubquery_cf` and `QuerySelectSub_cf` prepend the subquery's bindings. `QueryWhereInSubquery_cf`, `QueryJoinSub_cf`, and similar functions append bindings. For `QueryJoinSub_cf` and `QueryLeftJoinSub_cf`, call before adding WHERE conditions to preserve left-to-right binding order.

**Testing:** Use `QueryToSQL_cf` to inspect the assembled SQL before executing. If `QueryGet_cf` returns `""`, the SQL contains an error — inspect the SQL string and verify it against your FM version's supported syntax.
