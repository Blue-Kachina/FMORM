# FMORM Function Reference

---

## Table of Contents

### Public builders

| Function | Purpose |
|---|---|
| [QueryNew](#querynew) | Initialise a new query object |
| [QuerySelect](#queryselect) | Set or extend the SELECT column list |
| [QuerySelectSub](#queryselectsub) | Add a subquery expression to the SELECT list |
| [QueryDistinct](#querydistinct) | Add SELECT DISTINCT |
| [QueryWhere](#querywhere) | Append AND WHERE condition |
| [QueryOrWhere](#queryorwhere) | Append OR WHERE condition |
| [QueryWhereIn](#querywherein) | Append AND WHERE column IN (…) |
| [QueryWhereNotIn](#querywherenotin) | Append AND WHERE column NOT IN (…) |
| [QueryOrWhereIn](#queryorwherein) | Append OR WHERE column IN (…) |
| [QueryWhereNull](#querywherenull) | Append AND column IS NULL |
| [QueryWhereNotNull](#querywherenotnull) | Append AND column IS NOT NULL |
| [QueryOrWhereNull](#queryorwherenull) | Append OR column IS NULL |
| [QueryOrWhereNotNull](#queryorwherenotnull) | Append OR column IS NOT NULL |
| [QueryWhereBetween](#querywherebetween) | Append AND column BETWEEN low AND high |
| [QueryWhereNotBetween](#querywherenotbetween) | Append AND column NOT BETWEEN low AND high |
| [QueryOrWhereBetween](#queryorwherebetween) | Append OR column BETWEEN low AND high |
| [QueryOrWhereNotBetween](#queryorwherenotbetween) | Append OR column NOT BETWEEN low AND high |
| [QueryWhereColumn](#querywherecolumn) | Append AND column1 op column2 (column comparison, no binding) |
| [QueryWhereGroup](#querywheregroup) | Append AND (grouped conditions from another query) |
| [QueryOrWhereGroup](#queryorwheregroup) | Append OR (grouped conditions from another query) |
| [QueryWhereRaw](#querywhereraw) | Append AND (raw SQL expression) |
| [QueryOrWhereRaw](#queryorwhereraw) | Append OR (raw SQL expression) |
| [QueryWhereInSubquery](#querywhereinsubquery) | Append AND column IN (subquery) |
| [QueryWhereNotInSubquery](#querywherenotinsubquery) | Append AND column NOT IN (subquery) |
| [QueryWhereExists](#querywhereexists) | Append AND EXISTS (subquery) |
| [QueryWhereNotExists](#querywherenotexists) | Append AND NOT EXISTS (subquery) |
| [QueryFromSubquery](#queryfromsubquery) | Replace FROM table with a derived table (subquery) |
| [QueryJoin](#queryjoin) | Append INNER JOIN |
| [QueryLeftJoin](#queryleftjoin) | Append LEFT JOIN |
| [QueryRightJoin](#queryrightjoin) | Append RIGHT JOIN |
| [QueryCrossJoin](#querycrossjoin) | Append CROSS JOIN |
| [QueryJoinSub](#queryjoinsub) | Append INNER JOIN (subquery) |
| [QueryLeftJoinSub](#queryleftjoinsub) | Append LEFT JOIN (subquery) |
| [QueryOrderBy](#queryorderby) | Append ORDER BY column |
| [QueryOrderByRaw](#queryorderbyraw) | Append ORDER BY raw expression |
| [QueryReorder](#queryreorder) | Clear all ORDER BY clauses |
| [QueryGroupBy](#querygroupby) | Append GROUP BY column |
| [QueryGroupByRaw](#querygroupbyraw) | Append GROUP BY raw expression |
| [QueryHaving](#queryhaving) | Append AND HAVING condition |
| [QueryOrHaving](#queryorhaving) | Append OR HAVING condition |
| [QueryHavingRaw](#queryhavingraw) | Append AND HAVING raw expression |
| [QueryOrHavingRaw](#queryorhavingraw) | Append OR HAVING raw expression |
| [QueryLimit](#querylimit) | Set the row limit |
| [QueryOffset](#queryoffset) | Set the row offset |
| [QueryForPage](#queryforpage) | Set limit and offset for a specific page number |
| [QueryUnion](#queryunion) | Append UNION or UNION ALL |
| [QueryGet](#queryget) | Execute the query and return results |
| [QueryGetResultsAsJson](#querygetresultsasjson) | Execute the query and return results as a JSON array of objects |
| [QueryToSQL](#querytosql) | Return the assembled SQL string (debug) |
| [QueryCount](#querycount) | Execute SELECT COUNT(*) and return the count |
| [QuerySum](#querysum) | Execute SELECT SUM(column) and return the sum |
| [QueryAvg](#queryavg) | Execute SELECT AVG(column) and return the average |
| [QueryMax](#querymax) | Execute SELECT MAX(column) and return the maximum |
| [QueryMin](#querymin) | Execute SELECT MIN(column) and return the minimum |
| [QueryWhen](#querywhen) | Conditionally apply query modifications |

### Utility functions

| Function | Purpose |
|---|---|
| [JSONGetElementNamedLikeField](#jsongetelementnamedlikefield) | Get a JSON element using a FileMaker field reference or field-name string as the property key; optional index for array input |

### Internal helpers

These functions are called by the public builders and are not intended to be called directly.

| Function | Purpose |
|---|---|
| [QueryBuildJoins](#querybuildjoins) | Recursively render JOIN clauses |
| [QueryBuildWheres](#querybuildwheres) | Recursively render WHERE clause body |
| [QueryBuildInPlaceholders](#querybuildinplaceholders) | Render N comma-separated `?` placeholders |
| [QueryBuildGroupBys](#querybuildgroupbys) | Recursively render GROUP BY column list |
| [QueryBuildHavings](#querybuildhavings) | Recursively render HAVING clause body |
| [QueryBuildOrderBys](#querybuildorderbys) | Recursively render ORDER BY column list |
| [QueryBuildUnions](#querybuildunions) | Recursively render UNION / UNION ALL clauses |
| [QueryBuildBindingArgs](#querybuildbindingargs) | Render binding values for Evaluate injection |
| [QueryBuildWhereBooleanPrefix](#querybuildwherebooleanprefix) | Render AND / OR / empty connector |
| [QueryAppendBindings](#queryappendbindings) | Recursively append N values to the bindings array |
| [QueryMergeBindings](#querymergebindings) | Append N bindings from a JSON array into the outer query |
| [QueryPrependBindings](#queryprependbindings) | Rebuild the bindings array with subquery bindings first |
| [QueryBuildSelects](#querybuildselects) | Convert ¶-delimited field names to quoted SQL column list |
| [QueryFieldFormat](#queryfieldformat) | Convert a single `Table::Field` name to quoted dot notation |
| [QueryBuildJsonRow](#querybuildjsonrow) | Build a single JSON object from a row of field values |
| [QueryBuildJsonRows](#querybuildjsonrows) | Recursively build a JSON array from all result rows |
| [QueryBuildSelectKeys](#querybuildselectkeys) | Extract plain key names from the original column input |

---

## Public builders

---

### QueryNew

Initialises a fresh query object for the given table occurrence. All clause arrays are set to empty, `selects` defaults to `*`, and all counts are set to `0`. Pass the returned object as the first argument to every subsequent builder call.

The table name is stored pre-quoted (`"Table"`) so the generated SQL consistently uses double-quoted identifiers throughout.

**Parameters**

| Parameter | Description |
|---|---|
| `table` | Table occurrence name. Accepts a plain string (`"CONTACT"`), a direct FM field reference (`CONTACT::anyField`), or a `GetFieldName()` result. When a `Table::Field` string or field reference is passed, the table part is extracted automatically. |

**Example**

```
// Direct field reference — no GetFieldName() wrapper needed
_query = QueryNew ( CONTACT::__kptID )

// GetFieldName() — rename-safe alternative
_query = QueryNew ( GetFieldName ( CONTACT::__kptID ) )

// Plain string — also valid
_query = QueryNew ( "CONTACT" )
```

---

### QuerySelect

Sets or extends the SELECT column list. The first call after `QueryNew` replaces the default `SELECT *` sentinel. Each subsequent call **appends** to the existing column list.

Accepts a ¶-delimited list (e.g. from `List()` and `GetFieldName()`) or a comma-separated string. `Table::Field` names are converted to `"Table"."Field"`. Expressions without `::` pass through unchanged — `*`, aggregates, `CASE`, raw SQL, etc. No separate `QuerySelectRaw` is needed.

Also stores `selectKeys` in the query object (plain field names, used by `QueryGetResultsAsJson` to name JSON properties).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `columns` | ¶-delimited list from `List()` / `GetFieldName()`, or a comma-separated SQL column string |

**Example**

```
_query = QuerySelect ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreatedBy ) ) )

// Additive — two calls accumulate both columns
_query = QuerySelect ( _query ; GetFieldName ( FMORM::PrimaryKey ) ) ;
_query = QuerySelect ( _query ; "COUNT(*) AS total" )
// → SELECT "FMORM"."PrimaryKey", COUNT(*) AS total
```

---

### QuerySelectSub

Adds a subquery expression to the SELECT list: `(SELECT …) AS alias`. The alias becomes the JSON property name when using `QueryGetResultsAsJson`. The subquery's bindings are prepended to the outer query's bindings (SELECT comes before WHERE in SQL).

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
_inner = QueryNew    ( "LINE_ITEM" ) ;
_inner = QuerySelect ( _inner ; "COUNT(*)" ) ;
_inner = QueryWhereColumn ( _inner ; "LINE_ITEM.invoiceId" ; "=" ; "INVOICE.id" ) ;

_query = QueryNew       ( "INVOICE" ) ;
_query = QuerySelect    ( _query ; GetFieldName ( INVOICE::id ) ) ;
_query = QuerySelectSub ( _query ; _inner ; "lineItemCount" )
// → SELECT "INVOICE"."id", (SELECT COUNT(*) FROM "LINE_ITEM" …) AS "lineItemCount"
```

---

### QueryDistinct

Adds `SELECT DISTINCT` to the query, eliminating duplicate rows from the result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_query = QueryNew    ( "CONTACT" ) ;
_query = QuerySelect ( _query ; GetFieldName ( CONTACT::country ) ) ;
_query = QueryDistinct ( _query )
// → SELECT DISTINCT "CONTACT"."country" FROM "CONTACT"
```

---

### QueryWhere

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
_query = QueryWhere ( _query ; CONTACT::status ; "=" ; "Active" )
// → WHERE "CONTACT"."status" = ?
```

---

### QueryOrWhere

Identical to `QueryWhere` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryWhere   ( _query ; CONTACT::status ; "=" ; "Active" ) ;
_query = QueryOrWhere ( _query ; CONTACT::status ; "=" ; "Prospect" )
// → WHERE "CONTACT"."status" = ? OR "CONTACT"."status" = ?
```

---

### QueryWhereIn

Appends AND column IN (?, ?, …). Each value in the ¶-delimited list becomes its own bound parameter.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhereIn ( _query ; CONTACT::type ; "customer¶prospect¶partner" )
// → WHERE "CONTACT"."type" IN (?, ?, ?)
```

---

### QueryWhereNotIn

Appends AND column NOT IN (?, ?, …). Each value becomes its own bound parameter.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhereNotIn ( _query ; CONTACT::status ; "Archived¶Deleted" )
// → WHERE "CONTACT"."status" NOT IN (?, ?)
```

---

### QueryOrWhereIn

Appends OR column IN (?, ?, …).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `values` | ¶-delimited list of values |

**Example**

```
_query = QueryWhere     ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryOrWhereIn ( _query ; CONTACT::type ; "partner¶reseller" )
// → WHERE "CONTACT"."region" = ? OR "CONTACT"."type" IN (?, ?)
```

---

### QueryWhereNull

Appends AND column IS NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhereNull ( _query ; CONTACT::deletedAt )
// → WHERE "CONTACT"."deletedAt" IS NULL
```

---

### QueryWhereNotNull

Appends AND column IS NOT NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhereNotNull ( _query ; CONTACT::emailWork )
// → WHERE "CONTACT"."emailWork" IS NOT NULL
```

---

### QueryOrWhereNull

Appends OR column IS NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryWhere     ( _query ; CONTACT::status ; "=" ; "Active" ) ;
_query = QueryOrWhereNull ( _query ; CONTACT::status )
// → WHERE "CONTACT"."status" = ? OR "CONTACT"."status" IS NULL
```

---

### QueryOrWhereNotNull

Appends OR column IS NOT NULL. No binding is added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryOrWhereNotNull ( _query ; CONTACT::emailWork )
// → OR "CONTACT"."emailWork" IS NOT NULL
```

---

### QueryWhereBetween

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
_query = QueryWhereBetween ( _query ; INVOICE::amount ; 100 ; 500 )
// → WHERE "INVOICE"."amount" BETWEEN ? AND ?
```

---

### QueryWhereNotBetween

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
_query = QueryWhereNotBetween ( _query ; INVOICE::amount ; 100 ; 500 )
// → WHERE "INVOICE"."amount" NOT BETWEEN ? AND ?
```

---

### QueryOrWhereBetween

Appends OR column BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound |
| `high` | Upper bound |

---

### QueryOrWhereNotBetween

Appends OR column NOT BETWEEN low AND high. Two bindings are added.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `low` | Lower bound |
| `high` | Upper bound |

---

### QueryWhereColumn

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
_query = QueryWhereColumn ( _query ; INVOICE::contactId ; "=" ; CONTACT::id )
// → WHERE "INVOICE"."contactId" = "CONTACT"."id"
```

---

### QueryWhereGroup

Appends AND (grouped conditions) by wrapping the WHERE conditions from `groupedQuery` in parentheses. Build `groupedQuery` using any combination of `QueryWhere`, `QueryOrWhere`, etc. on any query object — only its `wheres` array and bindings are used; its FROM, SELECT, and other clauses are ignored.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object to append to |
| `groupedQuery` | A query object whose WHERE conditions form the group |

**Example**

```
// Build the inner group: (status = ? OR priority = ?)
_g = QueryNew     ( "CONTACT" ) ;
_g = QueryWhere   ( _g ; CONTACT::status ; "=" ; "Active" ) ;
_g = QueryOrWhere ( _g ; CONTACT::priority ; "=" ; "High" ) ;

// Attach the group to the main query
_query = QueryNew       ( "CONTACT" ) ;
_query = QueryWhere     ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryWhereGroup ( _query ; _g )
// → WHERE "CONTACT"."region" = ? AND ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

---

### QueryOrWhereGroup

Identical to `QueryWhereGroup` but joins the group with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `groupedQuery` | A query object whose WHERE conditions form the group |

**Example**

```
_query = QueryOrWhereGroup ( _query ; _g )
// → OR ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

---

### QueryWhereRaw

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
_query = QueryWhereRaw ( _query ; "MONTH(\"INVOICE\".\"date\") = MONTH(CURRENT_DATE)" ; "" )
// → WHERE (MONTH("INVOICE"."date") = MONTH(CURRENT_DATE))

// With bindings
_query = QueryWhereRaw ( _query ; "\"INVOICE\".\"total\" BETWEEN ? AND ?" ; "100¶500" )
// → WHERE ("INVOICE"."total" BETWEEN ? AND ?)
```

---

### QueryOrWhereRaw

Identical to `QueryWhereRaw` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values |

---

### QueryWhereInSubquery

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
_inner = QueryNew    ( "CONTACT" ) ;
_inner = QuerySelect ( _inner ; "CONTACT.id" ) ;
_inner = QueryWhere  ( _inner ; CONTACT::status ; "=" ; "Active" ) ;

_query = QueryNew             ( "INVOICE" ) ;
_query = QueryWhereInSubquery ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" IN (SELECT CONTACT.id FROM "CONTACT" WHERE …)
```

---

### QueryWhereNotInSubquery

Appends AND column NOT IN (SELECT …). Same binding semantics as `QueryWhereInSubquery`.

> **FileMaker compatibility:** Requires FileMaker 17+.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `column` | Column reference |
| `subquery` | A fully-assembled fmorm query object |

**Example**

```
_query = QueryWhereNotInSubquery ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" NOT IN (SELECT … )
```

---

### QueryWhereExists

Appends AND EXISTS (SELECT …). The subquery's bindings are appended.

> **FileMaker compatibility:** Requires FileMaker 17+. Correlated subqueries are not reliably supported.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `subquery` | A fully-assembled fmorm query object |

**Example**

```
_inner = QueryNew   ( "INVOICE" ) ;
_inner = QueryWhere ( _inner ; INVOICE::contactId ; "=" ; "some-id" ) ;

_query = QueryNew        ( "CONTACT" ) ;
_query = QueryWhereExists ( _query ; _inner )
// → WHERE EXISTS (SELECT * FROM "INVOICE" WHERE …)
```

---

### QueryWhereNotExists

Appends AND NOT EXISTS (SELECT …). Same semantics as `QueryWhereExists`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Outer query object |
| `subquery` | A fully-assembled fmorm query object |

---

### QueryFromSubquery

Replaces the FROM table with a derived table: `FROM (SELECT …) alias`. The table name set in `QueryNew` is discarded. The subquery's bindings are prepended automatically.

> **FileMaker compatibility:** Functional in FM 19.x; not formally documented by Claris. Avoid `QueryLimit` / `QueryOffset` on the inner query. See [FileMaker SQL Compatibility Notes](#filemaker-sql-compatibility-notes).

**Parameters**

| Parameter | Description |
|---|---|
| `outerQuery` | Outer query object (its table name is replaced) |
| `subquery` | A fully-assembled fmorm query object to use as the derived table |
| `alias` | Plain SQL identifier for the derived table, e.g. `"sub"` |

**Example**

```
_inner = QueryNew     ( "INVOICE" ) ;
_inner = QuerySelect  ( _inner ; "INVOICE.contactID, MAX(INVOICE.invoiceDate) AS lastDate" ) ;
_inner = QueryGroupBy ( _inner ; "INVOICE.contactID" ) ;

_query = QueryNew          ( "CONTACT" ) ;
_query = QueryFromSubquery ( _query ; _inner ; "recent" ) ;
_query = QueryWhere        ( _query ; "recent.lastDate" ; ">" ; Get ( CurrentDate ) - 30 )
```

---

### QueryJoin

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
_query = QueryJoin ( _query ; invoice__ITEM::__kptID ; CONTACT::_kftItemID ; "=" ; invoice__ITEM::__kptID )
// → INNER JOIN "invoice__ITEM" ON "CONTACT"."_kftItemID" = "invoice__ITEM"."__kptID"
```

---

### QueryLeftJoin

Appends a LEFT JOIN clause. Same parameters as `QueryJoin`.

**Example**

```
_query = QueryLeftJoin ( _query ; contact__INVOICE::__kptID ; CONTACT::_kftInvoiceID ; "=" ; contact__INVOICE::__kptID )
// → LEFT JOIN "contact__INVOICE" ON "CONTACT"."_kftInvoiceID" = "contact__INVOICE"."__kptID"
```

---

### QueryRightJoin

Appends a RIGHT JOIN clause. Same parameters as `QueryJoin`.

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
_query = QueryRightJoin ( _query ; "INVOICE" ; CONTACT::id ; "=" ; "INVOICE.contactId" )
// → RIGHT JOIN "INVOICE" ON "CONTACT"."id" = INVOICE.contactId
```

---

### QueryCrossJoin

Appends a CROSS JOIN (cartesian product). No ON condition.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `table` | Table to join — field reference, `GetFieldName()`, or plain string |

**Example**

```
_query = QueryCrossJoin ( _query ; "SIZE" )
// → CROSS JOIN "SIZE"
```

---

### QueryJoinSub

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
_inner = QueryNew    ( "LINE_ITEM" ) ;
_inner = QuerySelect ( _inner ; "LINE_ITEM.invoiceId, SUM(LINE_ITEM.amount) AS total" ) ;
_inner = QueryGroupBy ( _inner ; "LINE_ITEM.invoiceId" ) ;

_query = QueryNew    ( "INVOICE" ) ;
_query = QueryJoinSub ( _query ; _inner ; "totals" ; "INVOICE.id" ; "=" ; "totals.invoiceId" )
// → INNER JOIN (SELECT … FROM "LINE_ITEM" GROUP BY …) totals ON INVOICE.id = totals.invoiceId
```

---

### QueryLeftJoinSub

Appends LEFT JOIN (SELECT …) alias ON condition. Same semantics as `QueryJoinSub` but uses a LEFT JOIN.

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

### QueryOrderBy

Appends an ORDER BY column. Call multiple times to sort by multiple columns in order.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |
| `direction` | `ASC` or `DESC` — defaults to `ASC` when empty |

**Example**

```
_query = QueryOrderBy ( _query ; CONTACT::lastName ; "ASC" ) ;
_query = QueryOrderBy ( _query ; CONTACT::firstName ; "ASC" )
// → ORDER BY "CONTACT"."lastName" ASC, "CONTACT"."firstName" ASC
```

---

### QueryOrderByRaw

Appends a raw SQL expression to the ORDER BY clause. Useful for `RAND()`, `CASE` expressions, or function-based ordering not supported by `QueryOrderBy`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression emitted verbatim in the ORDER BY list |

**Example**

```
_query = QueryOrderByRaw ( _query ; "RAND()" )
// → ORDER BY RAND()
```

---

### QueryReorder

Clears all existing ORDER BY clauses from the query, allowing a fresh ordering to be applied.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_query = QueryOrderBy ( _query ; CONTACT::lastName ; "ASC" ) ;
_query = QueryReorder ( _query ) ;
_query = QueryOrderBy ( _query ; CONTACT::createdAt ; "DESC" )
// Previous ORDER BY discarded; now sorts by createdAt DESC only
```

---

### QueryGroupBy

Appends a GROUP BY column. Call multiple times for multiple grouping columns.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column reference |

**Example**

```
_query = QueryGroupBy ( _query ; CONTACT::type )
// → GROUP BY "CONTACT"."type"
```

---

### QueryGroupByRaw

Appends a raw SQL expression to the GROUP BY clause. Useful for function-based grouping.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression emitted verbatim in the GROUP BY list |

**Example**

```
_query = QueryGroupByRaw ( _query ; "YEAR(\"INVOICE\".\"date\")" )
// → GROUP BY YEAR("INVOICE"."date")
```

---

### QueryHaving

Appends an AND HAVING condition with a bound parameter. Must be used after `QueryGroupBy`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column or aggregate expression |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryGroupBy ( _query ; "CONTACT.type" ) ;
_query = QueryHaving  ( _query ; "COUNT(*)" ; ">" ; 5 )
// → GROUP BY CONTACT.type HAVING COUNT(*) > ?
```

---

### QueryOrHaving

Identical to `QueryHaving` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `column` | Column or aggregate expression |
| `operator` | SQL comparison operator |
| `value` | Bound value |

**Example**

```
_query = QueryHaving   ( _query ; "COUNT(*)" ; ">" ; 5 ) ;
_query = QueryOrHaving ( _query ; "SUM(amount)" ; ">" ; 1000 )
// → HAVING COUNT(*) > ? OR SUM(amount) > ?
```

---

### QueryHavingRaw

Appends AND (rawSql) to the HAVING clause verbatim.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values for `?` placeholders. Pass `""` when there are none. |

**Example**

```
_query = QueryHavingRaw ( _query ; "COUNT(*) BETWEEN ? AND ?" ; "5¶20" )
// → HAVING (COUNT(*) BETWEEN ? AND ?)
```

---

### QueryOrHavingRaw

Identical to `QueryHavingRaw` but joins with OR.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `rawSql` | Raw SQL expression |
| `bindings` | *(Optional)* ¶-delimited bound values |

---

### QueryLimit

Sets the maximum number of rows to return. Emits `FETCH FIRST n ROWS ONLY` (FileMaker's SQL dialect — `LIMIT` is not valid).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `value` | Maximum number of rows |

**Example**

```
_query = QueryLimit ( _query ; 50 )
// → FETCH FIRST 50 ROWS ONLY
```

---

### QueryOffset

Sets the number of rows to skip. Emits `OFFSET n ROWS`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `value` | Number of rows to skip |

**Example**

```
_query = QueryOffset ( _query ; 100 )
// → OFFSET 100 ROWS
```

---

### QueryForPage

Convenience function: sets both limit and offset for a specific 1-based page number. Equivalent to calling `QueryLimit` and `QueryOffset` with `offset = (page - 1) * perPage`.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `page` | Page number (1-based) |
| `perPage` | Number of rows per page |

**Example**

```
_query = QueryForPage ( _query ; 3 ; 25 )
// → FETCH FIRST 25 ROWS ONLY OFFSET 50 ROWS   (page 3 of 25)
```

---

### QueryUnion

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
_q1 = QueryNew    ( "CONTACT" ) ;
_q1 = QuerySelect ( _q1 ; "CONTACT.name, CONTACT.email" ) ;
_q1 = QueryWhere  ( _q1 ; CONTACT::type ; "=" ; "customer" ) ;

_q2 = QueryNew    ( "PROSPECT" ) ;
_q2 = QuerySelect ( _q2 ; "PROSPECT.name, PROSPECT.email" ) ;

_q1 = QueryUnion ( _q1 ; _q2 ; 0 )
// → SELECT … FROM "CONTACT" WHERE … UNION SELECT … FROM "PROSPECT"
```

---

### QueryGet

Executes the assembled query via `ExecuteSQL`. Bound values are injected using `Evaluate ( ExecuteSQL ( … ) )`. Returns `""` on error (when `ExecuteSQL` returns a value beginning with `?`).

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |
| `fieldSeparator` | Character(s) placed between field values within a row |
| `rowSeparator` | Character(s) placed between rows |

**Example**

```
_result = QueryGet ( _query ; "," ; "¶" )
```

---

### QueryGetResultsAsJson

Executes the query and returns results as a JSON array of objects, one object per row. Property names come from `selectKeys` stored by `QuerySelect`. Returns `"[]"` on no rows or error. All values are stored as JSON strings.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Fully assembled query object |

**Example**

```
_result = QueryGetResultsAsJson ( _query )
// → [{"PrimaryKey":"1","FullName":"Jane Smith","Status":"Active"},…]
```

---

### QueryToSQL

Returns the assembled SQL string without executing it. Bound parameters appear as `?`. Output is pretty-printed. Useful during development for verifying query structure.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |

**Example**

```
_sql = QueryToSQL ( _query )
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

### QueryCount

Executes `SELECT COUNT(*)` for the assembled query and returns the count as a number. The original query object is not modified. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object (FROM, WHERE, JOINs already set) |

**Example**

```
_count = QueryCount ( _query )
// Executes: SELECT COUNT(*) FROM … WHERE …
// Returns: 42
```

---

### QuerySum

Executes `SELECT SUM(column)` and returns the sum as a number. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference — field reference, `GetFieldName()`, or SQL expression |

**Example**

```
_total = QuerySum ( _query ; INVOICE::amount )
// Executes: SELECT SUM("INVOICE"."amount") FROM … WHERE …
```

---

### QueryAvg

Executes `SELECT AVG(column)` and returns the average as a number. Returns `0` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_avg = QueryAvg ( _query ; INVOICE::amount )
```

---

### QueryMax

Executes `SELECT MAX(column)` and returns the maximum value as a string. Returns `""` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_latest = QueryMax ( _query ; INVOICE::invoiceDate )
```

---

### QueryMin

Executes `SELECT MIN(column)` and returns the minimum value as a string. Returns `""` on error or empty result.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Assembled query object |
| `column` | Column reference |

**Example**

```
_earliest = QueryMin ( _query ; INVOICE::invoiceDate )
```

---

### QueryWhen

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
_query = QueryNew ( "CONTACT" ) ;
_query = QueryWhen (
    _query ;
    not IsEmpty ( $$filterStatus ) ;
    QueryWhere ( _query ; CONTACT::status ; "=" ; $$filterStatus )
)
// Adds the WHERE clause only when $$filterStatus is non-empty
```

---

## Internal helpers

These functions are called automatically by the public builders and are marked `visible = False` in FileMaker. They are not intended for direct use.

---

### QueryBuildJoins

Recursively walks the `joins` array and renders the full JOIN clause string. Supports types: `inner`, `left`, `right`, `cross`, `subJoin`, `leftSubJoin`.

**Parameters**

| Parameter | Description |
|---|---|
| `joins` | Raw JSON array from the query object |
| `joinCount` | Number of join objects |
| `index` | Current position — call with `0` |

---

### QueryBuildWheres

Recursively walks the `wheres` array and renders the WHERE clause body (excluding the `WHERE` keyword). Supports types: `basic`, `in`, `notIn`, `null`, `notNull`, `between`, `notBetween`, `column`, `raw`, `group`, `exists`, `notExists`, `inSubquery`, `notInSubquery`.

**Parameters**

| Parameter | Description |
|---|---|
| `wheres` | Raw JSON array from the query object |
| `whereCount` | Number of where objects |
| `index` | Current position — call with `0` |

---

### QueryBuildInPlaceholders

Recursively produces N comma-separated `?` placeholders for IN clauses.

**Parameters**

| Parameter | Description |
|---|---|
| `count` | Total number of placeholders |
| `index` | Current position — call with `0` |

**Example**

```
QueryBuildInPlaceholders ( 3 ; 0 )
// → "?, ?, ?"
```

---

### QueryBuildGroupBys

Recursively walks the `groupBys` array. Regular columns are plain JSON strings; raw expressions are JSON objects `{"type":"raw","sql":"…"}` identified by `Left(item;1)="{"`.

**Parameters**

| Parameter | Description |
|---|---|
| `groupBys` | Raw JSON array from the query object |
| `groupByCount` | Number of entries |
| `index` | Current position — call with `0` |

---

### QueryBuildHavings

Recursively walks the `havings` array. Supports types: default (basic column/operator), `raw`. Handles AND/OR boolean prefix.

**Parameters**

| Parameter | Description |
|---|---|
| `havings` | Raw JSON array from the query object |
| `havingCount` | Number of having objects |
| `index` | Current position — call with `0` |

---

### QueryBuildOrderBys

Recursively walks the `orderBys` array. Supports default (column + direction) and `raw` type entries.

**Parameters**

| Parameter | Description |
|---|---|
| `orderBys` | Raw JSON array from the query object |
| `orderByCount` | Number of orderBy objects |
| `index` | Current position — call with `0` |

---

### QueryBuildUnions

Recursively walks the `unions` array and renders the UNION / UNION ALL clause string. Each union item stores `{sql, all}` where `all` is a boolean.

**Parameters**

| Parameter | Description |
|---|---|
| `unions` | Raw JSON array from the query object |
| `unionCount` | Number of union objects |
| `index` | Current position — call with `0` |

---

### QueryBuildBindingArgs

Recursively walks the `bindings` array and renders the bound values as a text fragment for insertion into an `Evaluate` expression. Each value is wrapped in `Quote()`.

**Parameters**

| Parameter | Description |
|---|---|
| `bindings` | Raw JSON array from the query object |
| `bindingCount` | Number of binding values |
| `index` | Current position — call with `0` |

---

### QueryBuildWhereBooleanPrefix

Returns the boolean connector that precedes a WHERE or HAVING clause. Returns `""` for the first clause, `" AND "` or `" OR "` for subsequent ones.

**Parameters**

| Parameter | Description |
|---|---|
| `boolean` | `"and"` or `"or"` |
| `index` | Position of the clause — `0` suppresses the connector |

---

### QueryAppendBindings

Recursively appends values from a ¶-delimited list to the `bindings` array, incrementing `bindingCount` with each addition.

**Parameters**

| Parameter | Description |
|---|---|
| `query` | Query object |
| `values` | ¶-delimited list of values |
| `valueCount` | Total number of values |
| `index` | Current position — call with `1` (`GetValue` is 1-based) |

---

### QueryMergeBindings

Recursively appends binding values from a JSON array into the outer query's `bindings` array.

**Parameters**

| Parameter | Description |
|---|---|
| `outerQuery` | Query object to append bindings into |
| `sourceBindings` | JSON array of binding values |
| `sourceCount` | Number of values |
| `index` | Current position — call with `0` |

---

### QueryPrependBindings

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

### QueryBuildSelects

Recursively converts a ¶-delimited column list to a SQL column expression string. Delegates to `QueryFieldFormat`.

**Parameters**

| Parameter | Description |
|---|---|
| `columns` | ¶-delimited list of column expressions |
| `columnCount` | Total number of columns |
| `index` | Current position — call with `1` |

---

### QueryFieldFormat

Converts a `Table::Field` string to `"Table"."Field"`. Expressions without `::` pass through unchanged. Called by all public builders that accept column references.

**Parameters**

| Parameter | Description |
|---|---|
| `field` | A `Table::Field` string, direct FM field reference, or plain SQL expression |

**Example**

```
QueryFieldFormat ( FMORM::PrimaryKey )                  // → "FMORM"."PrimaryKey"
QueryFieldFormat ( "*" )                                // → *  (pass-through)
QueryFieldFormat ( "COUNT(*)" )                         // → COUNT(*)  (pass-through)
```

---

### QueryBuildJsonRow

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

### QueryBuildJsonRows

Recursively appends row objects to a JSON array. Called by `QueryGetResultsAsJson`.

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

### QueryBuildSelectKeys

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

### JSONGetElementNamedLikeField

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
JSONGetElementNamedLikeField ( _json ; GetFieldName ( CONTACT::firstName ) ; "" )
// → value of "firstName" property

// Array — index 0
JSONGetElementNamedLikeField ( _jsonArray ; GetFieldName ( CONTACT::firstName ) ; 0 )

// Path 2 — qualified string
JSONGetElementNamedLikeField ( _json ; "CONTACT::firstName" ; "" )

// Path 3 — plain property name
JSONGetElementNamedLikeField ( _json ; "firstName" ; "" )
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
| `FETCH FIRST` / `OFFSET` inside a subquery | Unreliable; avoid `QueryLimit` / `QueryOffset` on inner queries |
| RIGHT JOIN | Supported in standard FileMaker SQL |
| CROSS JOIN | Supported in standard FileMaker SQL |
| Window functions / CTEs | Not supported by FileMaker's ExecuteSQL |

**Binding order** is handled automatically. `QueryFromSubquery` and `QuerySelectSub` prepend the subquery's bindings. `QueryWhereInSubquery`, `QueryJoinSub`, and similar functions append bindings. For `QueryJoinSub` and `QueryLeftJoinSub`, call before adding WHERE conditions to preserve left-to-right binding order.

**Testing:** Use `QueryToSQL` to inspect the assembled SQL before executing. If `QueryGet` returns `""`, the SQL contains an error — inspect the SQL string and verify it against your FM version's supported syntax.
