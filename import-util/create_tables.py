# boto3 is official AWS SDK for python
import boto3

# Dynamo DB connection local connection
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


# The Following data will be inserted in their respective tables
BOARDS = [
    {"board_id": 1, "name": 'CIE'},
    {"board_id": 2, "name": 'Edexel'},
    {"board_id": 3, "name": 'IB'},
]

LEVELS = [
    {"level_id": 1, "level_name": 'A Levels'},
    {"level_id": 2, "level_name": 'GCE O Levels'},
    {"level_id": 3, "level_name": 'IG'},
]

QUESTION_TYPES = [
    {"question_type_id": 1, "type": 'MCQ'},
    {"question_type_id": 2, "type": 'Descriptive'},
]

SUBJECTS = [
    {"subject_id": 1, "subject_name": 'Chemistry'},
    {"subject_id": 2, "subject_name": 'Biology'},
    {"subject_id": 3, "subject_name": 'Physics'},
    {"subject_id": 4, "subject_name": 'cord_sci'},
]

# Creating Board Table
board_table = dynamodb.create_table(
    TableName='boards',
    KeySchema=[
        {
            'AttributeName': 'board_id',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'board_id',
            'AttributeType': 'N'
        }
    ],
    # ProvisionedThroughput is ignored in Local Dynamo DB instance
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Boards Table Created!")

# Board table data insertion
for i in range(len(BOARDS)):
    board_table.put_item(
        Item={
            "board_id": BOARDS[i]["board_id"],
            "name":     BOARDS[i]["name"],
        }
    )
    pass

print("Data inserted in Boards Table")

# Creating Level Table
level_table = dynamodb.create_table(
    TableName='levels',
    KeySchema=[
        {
            'AttributeName': 'level_id',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'level_id',
            'AttributeType': 'N'
        }
    ],
    # ProvisionedThroughput is ignored in Local Dynamo DB instance
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Levels Table Created!")

# Level table data insertion
for i in range(len(LEVELS)):
    level_table.put_item(
        Item={
            "level_id":   LEVELS[i]["level_id"],
            "level_name": LEVELS[i]["level_name"],
        }
    )
    pass

print("Data inserted in Levels Table")

# Creating Level Table
subject_table = dynamodb.create_table(
    TableName='subjects',
    KeySchema=[
        {
            'AttributeName': 'subject_id',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'subject_id',
            'AttributeType': 'N'
        }
    ],
    # ProvisionedThroughput is ignored in Local Dynamo DB instance
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Levels Table Created!")

# Level table data insertion
for i in range(len(SUBJECTS)):
    subject_table.put_item(
        Item={
            "subject_id":   SUBJECTS[i]["subject_id"],
            "subject_name": SUBJECTS[i]["subject_name"],
        }
    )
    pass

print("Data inserted in Subjects Table")

# Creating Question_Types Table
question_type_table = dynamodb.create_table(
    TableName='question_types',
    KeySchema=[
        {
            'AttributeName': 'question_type_id',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'question_type_id',
            'AttributeType': 'N'
        }
    ],
    # ProvisionedThroughput is ignored in Local Dynamo DB instance
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Levels Table Created!")

# Level table data insertion
for i in range(len(QUESTION_TYPES)):
    question_type_table.put_item(
        Item={
            "question_type_id": QUESTION_TYPES[i]["question_type_id"],
            "type":             QUESTION_TYPES[i]["type"],
        }
    )

print("Data inserted in QUESTION_TYPES Table")

# Creating Questions Table
questions_table = dynamodb.create_table(
    TableName='questions',
    KeySchema=[
        {
            'AttributeName': 'question_id',
            'KeyType': 'HASH'  # Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'question_id',
            'AttributeType': 'N'
        }
    ],
    # ProvisionedThroughput is ignored in Local Dynamo DB instance
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Questions Table Created!")
