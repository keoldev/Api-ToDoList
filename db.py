import boto3
import uuid
from decouple import config

db_client = boto3.client('dynamodb')


def insert_task(user_id: str, task: str):
    task_id= str(uuid.uuid4())
    db_client.put_item(
        TableName=config('DDB_TABLE_NAME'),
        Item={
            "user_id": {"S": user_id},
            "task_id": {"S": task_id},
            "task": {"S": task},
            "status": {"S": 'incomplete'}
        }
    )
    return task_id

def get_tasks(user_id: str):
    response = db_client.query(
        TableName=config('DDB_TABLE_NAME'),
        KeyConditionExpression='user_id= :user_id',
        ExpressionAttributeValues={
            ":user_id": {"S": user_id}
        }
    )
    return response['Items']

def update_status(user_id: str, task_id: str, status: str ):
    response=db_client.update_item(
        TableName=config('DDB_TABLE_NAME'),
        Key={
            "user_id": {"S": user_id} ,
            "task_id": {"S": task_id}
        },
        UpdateExpression= 'SET #st = :status',
        ExpressionAttributeNames={
            '#st': "status"
        },
        ExpressionAttributeValues={
            ':status' : {"S": status}
        }
    )

def delete_task(user_id: str, task_id: str):
    response=db_client.delete_item(
        TableName=config('DDB_TABLE_NAME'),
        Key={
            "user_id": {"S": user_id} ,
            "task_id": {"S": task_id}
        }
    )



