import boto3
import uuid

db_client = boto3.client('dynamodb')


def insert_task(user_id: str, task: str, task_id: str = str(uuid.uuid4()), status: str = 'incomplete'):
    db_client.put_item(
        TableName='users-tasks',
        Item={
            "user_id": {"S": user_id},
            "task_id": {"S": task_id},
            "task": {"S": task},
            "status": {"S": status}
        }
    )


def get_tasks(user_id: str):
    response = db_client.query(
        TableName='users-tasks',
        KeyConditionExpression='user_id= :user_id',
        ExpressionAttributeValues={
            ":user_id": {"S": user_id}
        }
    )
    return response['Items']

def update_status(user_id: str, task_id: str, status: str ):
    response=db_client.update_item(
        TableName='users-tasks',
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
        TableName='users-tasks',
        Key={
            "user_id": {"S": user_id} ,
            "task_id": {"S": task_id}
        }
    )



