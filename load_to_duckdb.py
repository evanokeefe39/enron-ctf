import pandas as pd
import duckdb

from log import get_logger
logger = get_logger()

logger.info("loading raw emails csv ...")

df = pd.read_csv('./sample_data/emails.csv')

logger.info("connecting to enron.db ...")

con = duckdb.connect("enron.db")

con.register("df", df)

logger.info("loading into duckdb ...")
con.execute("""
    DROP TABLE IF EXISTS emails_raw;
    CREATE TABLE emails_raw AS SELECT * FROM df;""")

# Parse and Pre-Process
logger.info("parsing emails...")

con.sql("""
-- Drop the existing table if it exists (optional)
DROP TABLE IF EXISTS emails_parsed;

-- Create the updated emails_parsed table with both Date and parsed_date
CREATE TABLE emails_parsed AS
SELECT
    regexp_extract(message, '^Message-ID: ([^\n]*)\n', 1) AS MessageID,
    regexp_extract(message, '\nDate: ([^\n]*)\n', 1) AS Date,
    STRPTIME(REGEXP_REPLACE(regexp_extract(message, '\nDate: ([^\n]*)\n', 1), '\s*\([A-Z]+\)', ''), '%a, %d %b %Y %H:%M:%S %z') AS parsed_date,
    regexp_extract(message, '\nFrom: ([^\n]*)\n', 1) AS "From",
    REGEXP_REPLACE(regexp_extract(message, '\nTo: ([^\n]*)\n', 1), ',+$', '') AS "To",
    regexp_extract(message, '\nSubject: ([^\n]*)\n', 1) AS Subject,
    regexp_extract(message, '\nMime-Version: ([^\n]*)\n', 1) AS MimeVersion,
    regexp_extract(message, '\nContent-Type: ([^\n]*)\n', 1) AS ContentType,
    regexp_extract(message, '\nContent-Transfer-Encoding: ([^\n]*)\n', 1) AS ContentTransferEncoding,
    regexp_extract(message, '\nX-From: ([^\n]*)\n', 1) AS XFrom,
    REGEXP_REPLACE(regexp_extract(message, '\nX-To: ([^\n]*)\n', 1), ',+$', '') AS XTo,
    regexp_extract(message, '\nX-cc: ([^\n]*)\n', 1) AS Xcc,
    regexp_extract(message, '\nX-bcc: ([^\n]*)\n', 1) AS Xbcc,
    regexp_extract(message, '\nX-Folder: ([^\n]*)\n', 1) AS XFolder,
    regexp_extract(message, '\nX-Origin: ([^\n]*)\n', 1) AS XOrigin,
    regexp_extract(message, '\nX-FileName: ([^\n]*)\n\n', 1) AS XFileName,
    regexp_extract(message, '\n\n(.*)$', 1, 's') AS Body
FROM emails_raw;
""")


logger.info("loading complete!")

