import pandas as pd
import duckdb

from log import get_logger
logger = get_logger()

logger.info("connecting to enron.db ...")

con = duckdb.connect("enron.db")

# Data Quality Checks
logger.info("checking data quality...")

con.sql("""
WITH quality_check AS (
    SELECT
        CAST(COUNT(*) AS VARCHAR) AS total_emails,
        CAST(MIN(parsed_date) AS VARCHAR) AS min_date,
        CAST(MAX(parsed_date) AS VARCHAR) AS max_date,
        CAST(SUM(CASE WHEN MessageID IS NULL OR TRIM(MessageID) = '' THEN 1 ELSE 0 END) AS VARCHAR) AS missing_or_empty_message_id,
        CAST(SUM(CASE WHEN parsed_date IS NULL THEN 1 ELSE 0 END) AS VARCHAR) AS missing_date,
        CAST(SUM(CASE WHEN "From" IS NULL OR TRIM("From") = '' THEN 1 ELSE 0 END) AS VARCHAR) AS missing_or_empty_from,
        CAST(SUM(CASE WHEN "To" IS NULL OR TRIM("To") = '' THEN 1 ELSE 0 END) AS VARCHAR) AS missing_or_empty_to,
        CAST(SUM(CASE WHEN Subject IS NULL OR TRIM(Subject) = '' THEN 1 ELSE 0 END) AS VARCHAR) AS missing_or_empty_subject,
        CAST(SUM(CASE WHEN Body IS NULL OR TRIM(Body) = '' THEN 1 ELSE 0 END) AS VARCHAR) AS missing_or_empty_body
    FROM emails_parsed
)
SELECT Metric, Value
FROM quality_check
UNPIVOT (
    Value
    FOR Metric IN (
        total_emails,
        min_date,
        max_date,
        missing_or_empty_message_id,
        missing_date,
        missing_or_empty_from,
        missing_or_empty_to,
        missing_or_empty_subject,
        missing_or_empty_body
    )
)
ORDER BY Metric;
""").show()
