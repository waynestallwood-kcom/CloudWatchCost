# Simple function to import run cost metrics into Cloudwatch for dashboards
# wayne.stallwood@kcom.com




from datetime import datetime, timedelta
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logging.info('Received event: ' + json.dumps(event))


    ONEDAYAGO = datetime.now() - timedelta(days=1)
    FOURDAYAGO = datetime.now() - timedelta(days=4)
    
    
    COSTEXPLORER = boto3.client('ce')
    CLOUDWATCH = boto3.client('cloudwatch')
    
    RESPONSE = COSTEXPLORER.get_cost_and_usage(
        TimePeriod={
            'Start': FOURDAYAGO.strftime("%Y-%m-%d"),
            'End': ONEDAYAGO.strftime("%Y-%m-%d")
        },
        Granularity='DAILY',
        Metrics=[
            'UnblendedCost',
        ],
    )
    
    #print(RESPONSE)
    
    COST1DAYAGO = float(RESPONSE["ResultsByTime"][2]["Total"]["UnblendedCost"]["Amount"])
    COST2DAYAGO = float(RESPONSE["ResultsByTime"][1]["Total"]["UnblendedCost"]["Amount"])
    COST3DAYAGO = float(RESPONSE["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])
    
    logging.info("1 day ago: $"+(str('{0:.2f}'.format(COST1DAYAGO))))
    logging.info("2 days ago: $"+(str('{0:.2f}'.format(COST2DAYAGO))))
    logging.info("3 days ago: $"+(str('{0:.2f}'.format(COST3DAYAGO))))
    
    TREND = (((COST3DAYAGO + COST2DAYAGO) / 2) - COST1DAYAGO)
    logging.info("TREND: $"+(str('{0:.2f}'.format(TREND))))
    
    
    # Let's put some custom metrics
    
    def putcloudwatch(name, value):
        CLOUDWATCH.put_metric_data(
            MetricData=[
                {
                    'MetricName': name,
                    'Dimensions': [
                        {
                            'Name': name,
                            'Value': 'Dollars'
                        },
                    ],
                    'Unit': 'None',
                    'Value': (float('{0:.2f}'.format(value)))
                },
                ],
            Namespace='Env/Runcost'
            )
            
            
    
    
    putcloudwatch('Yesterday', COST1DAYAGO)
    putcloudwatch('Trend', TREND)
    return

