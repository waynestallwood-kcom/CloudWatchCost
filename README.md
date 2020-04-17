# CloudWatchCost
Simple Python Lambda Function to push daily AWS run cost into a custom CloudWatch metric for use in Cloudwatch Dashboards.

Ensure your Lambda Execution role has sufficent rights to push metric data into CloudWatch and get billing data from the Cost Explorer Service.

Set alarms on the trend data to get daily billing alerts if your environments run cost rises sharply, or simply incorporate the metrics into a Cloudwatch Dashboard. 


