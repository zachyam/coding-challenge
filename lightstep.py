import json
import operator
import sys
import datetime

class Solution:
    def __init__(self, input_data):
        self.input_data = input_data
        # store a mapping of operation to their ERROR count
        self.operation_to_error_count = {}
        # store a mapping of transaction_ids to their earliest start and end time
        self.transaction_times = {}

    # This method returns the operation that has the most ERROR counts
    # If there is more than 1 operation with the highest count, return
    # the first operation that has the most error count
    def get_operation_with_highest_error_count(self):
        for data in self.input_data:
            operation = data['operation']
            error_type = data['level']
            if error_type != 'ERROR':
                continue
            self.operation_to_error_count[operation] = self.operation_to_error_count.get(operation, 0) + 1
        operation = max(self.operation_to_error_count.items(), key=operator.itemgetter(1))[0]
        error_count = max(self.operation_to_error_count.items(), key=operator.itemgetter(1))[1]

        print('Operation ' + operation + ' has the highest error count totalling ' + str(error_count))
        return (max(self.operation_to_error_count.items(), key=operator.itemgetter(1))[0],
                max(self.operation_to_error_count.items(), key=operator.itemgetter(1))[1])

    # This method returns the transaction that has the biggest difference
    # between the earliest START and latest END in its messages
    def get_longest_transaction_process(self):
        cur_longest_time = float('-inf')
        for data in self.input_data:
            transaction_id = data['transaction_id']
            if transaction_id not in self.transaction_times:
                current_start, current_end = (float('inf'), float('-inf'))
            else:
                current_start, current_end = self.transaction_times[transaction_id]
            message = data['message']
            timestamp = self.parse_timestamp(data['timestamp'])

            # if message contains START, update the earliest timestamp
            if 'START' in message:
                if timestamp < current_start:
                    current_start = timestamp
            # if message contains END, update the latest timestamp
            else:
                if timestamp > current_end:
                    current_end = timestamp
            # put into map
            self.transaction_times[transaction_id] = (current_start, current_end)

        # retrieve the transaction_id with the longest time difference
        for transaction_id, time_tuple in self.transaction_times.items():
            start_time = time_tuple[0]
            end_time = time_tuple[1]
            if (end_time - start_time) > cur_longest_time:
                cur_longest_time = end_time - start_time
                transaction = transaction_id
        print('Transaction ID: ' + transaction + ' has the longest transaction time with duration of ' + str(cur_longest_time))
        return (transaction, cur_longest_time)

    def parse_timestamp(self, timestamp):
        date_time_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        return date_time_obj.timestamp()

input_logs = open('input.json')
log_string = input_logs.read()
data = Solution(json.loads(log_string))
data.get_operation_with_highest_error_count()
data.get_longest_transaction_process()
