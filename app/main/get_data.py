import os

from google.cloud import bigquery

from datetime import datetime
# from google.auth import default
import google.auth

credentials, project_id = google.auth.default()


# creds, project_id = default()

client = bigquery.Client()

def get_summary_data(start_date, end_date, desiredPage):
    start_date = datetime.strftime(start_date, '%Y%m%d')
    end_date = datetime.strftime(end_date, '%Y%m%d')

    summary_sql = f"""
    DECLARE first_date STRING DEFAULT '{start_date}';
    DECLARE final_date STRING DEFAULT '{end_date}';
    DECLARE filtered_urls_for STRING DEFAULT '{desiredPage}';
    
    WITH sessions AS
    (
      SELECT DISTINCT fullVisitorId, visitId
      FROM `govuk-bigquery-analytics.87773428.ga_sessions_*`, UNNEST(hits) AS hits
      WHERE _table_suffix between first_date AND final_date
      AND
      REGEXP_CONTAINS(hits.page.pagePath, filtered_urls_for)
    )

  SELECT
    cast(TIMESTAMP_MILLIS(CAST(hits.time+(visitStartTime*1000) AS INT64)) as STRING) AS datetime,
    hits.page.pagePath,
    hits.eventInfo.eventCategory,
    hits.eventInfo.eventAction,
    hits.eventInfo.eventLabel,
  FROM `govuk-bigquery-analytics.87773428.ga_sessions_*`, unnest(hits) AS hits
  INNER JOIN sessions USING(fullVisitorId, visitId)
  WHERE _table_suffix between first_date AND final_date
  AND hits.page.pagePath NOT LIKE '/print%'
    """
    return client.query(summary_sql).to_dataframe()


def get_csv_data(start_date, end_date, desiredPage):
    start_date = datetime.strftime(start_date, '%Y%m%d')
    end_date = datetime.strftime(end_date, '%Y%m%d')

    csv_sql = f"""
    DECLARE first_date STRING DEFAULT '{start_date}';
    DECLARE final_date STRING DEFAULT '{end_date}';
    DECLARE filtered_urls_for STRING DEFAULT '{desiredPage}';

    WITH sessions AS
    (
      SELECT DISTINCT fullVisitorId, visitId
      FROM `govuk-bigquery-analytics.87773428.ga_sessions_*`, UNNEST(hits) AS hits
      WHERE _table_suffix between first_date AND final_date
      AND
      REGEXP_CONTAINS(hits.page.pagePath, filtered_urls_for)
    )

  SELECT
    'DataLabs' AS tablesource,
    _table_suffix AS tabledate,
    fullVisitorId,
    visitId,
    cast(TIMESTAMP_MILLIS(CAST(hits.time+(visitStartTime*1000) AS INT64)) as STRING) AS datetime,
    hits.hitNumber,
    hits.page.pagePath,
    hits.type,
    hits.eventInfo.eventCategory,
    hits.eventInfo.eventAction,
    hits.eventInfo.eventLabel,
    (SELECT value FROM hits.customDimensions WHERE index=4) AS content_id,
    (SELECT value FROM hits.customDimensions WHERE index=2) AS document_type,
    device.isMobile,
    CONCAT(fullVisitorId, '-', visitId) AS SessionId,
    hits.page.pagePath as page_path_copy,
    hits.eventInfo.eventCategory as event_category_copy,
    hits.eventInfo.eventAction as event_action_copy,
    hits.eventInfo.eventLabel as event_label_copy,

  FROM `govuk-bigquery-analytics.87773428.ga_sessions_*`, unnest(hits) AS hits
  INNER JOIN sessions USING(fullVisitorId, visitId)
  WHERE _table_suffix between first_date AND final_date
  AND hits.page.pagePath NOT LIKE '/print%'
    """
    return client.query(csv_sql).to_dataframe()