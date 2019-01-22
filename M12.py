
# coding: utf-8

# In[1]:



#引用套件
import boto3
#用boto3 套件與sqs作連結
sqs = boto3.resource(
    'sqs',
    endpoint_url='http://cc104.sqs.local:9324',
    region_name='dummy_region',
    aws_access_key_id='dummy_access_key',
    aws_secret_access_key='dummy_secret_key',
    verify=False) 


# In[2]:



#創建一個queue，Queue名為test，屬性(延遲時間為5秒)
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '5'})
# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))
print("===============================")
#開啟並展示已存在之queue
for queue in sqs.queues.all():
    print(1, queue.url)


# In[3]:



# Get the queue 名稱為 test
queue = sqs.get_queue_by_name(QueueName='test')

# Create a new message 創建訊息 內容為 apple
response2 = queue.send_message(MessageBody='apple')

# The response is NOT a resource, but gives you a message ID and MD5
print(response2.get('MessageId'))
print(response2.get('MD5OfMessageBody'))

#==================================================
#一次丟多個訊息進去queue
response3 = queue.send_messages(Entries=[
    {
        'Id': '1',
        'MessageBody': 'world',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel1',
                'DataType': 'String'
            }
        }
        
    },
    {
        'Id': '2',
        'MessageBody': 'boto3',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel2',
                'DataType': 'String'
            }
        }
    }
])
# Print out any failures
print(response3.get('Failed'))


# In[27]:



# Process messages by printing out body and optional(屬性名稱為"Author") author name
#把message從queue 拉出來
for message in queue.receive_messages(MessageAttributeNames=['Author']):
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)
            print(author_text)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))
    # Let the queue know that the message is processed
    message.delete()  #刪除message

