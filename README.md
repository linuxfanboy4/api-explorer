# API Explorer - Advanced Terminal API Testing Tool

## Overview

API Explorer is a powerful command-line interface (CLI) tool designed for comprehensive API testing directly from your terminal. Built with Python and featuring a rich terminal interface, this tool provides developers with an efficient way to test, debug, and interact with RESTful APIs without leaving the command line.

## Key Features

- **Multi-Method Support**: Test GET, POST, PUT, and DELETE requests with ease
- **Authentication Options**: Supports Basic Auth, Bearer Tokens, and OAuth2
- **Custom Headers**: Add any custom headers required by your API
- **Response Visualization**: Beautifully formatted JSON responses with syntax highlighting
- **Pagination Handling**: Automatically handle paginated API responses
- **Request Retries**: Configurable retry logic for failed requests
- **Response Caching**: Cache responses to avoid redundant requests
- **Mock Responses**: Test with mock responses without hitting real endpoints
- **Scripting Integration**: Create and execute test scripts in Python or JavaScript
- **Comprehensive Logging**: Detailed logging of all API interactions

## Installation

Install API Explorer with a single command:

```bash
wget https://raw.githubusercontent.com/linuxfanboy4/api-explorer/refs/heads/main/src/main.py && python3 main.py
```

## Requirements

- Python 3.6 or higher
- `requests` library
- `rich` library for terminal formatting

The required dependencies will be automatically installed when you first run the tool.

## Usage

1. **Start the tool**: Run `python3 main.py` in your terminal
2. **Set Base URL**: Enter the base URL of the API you want to test
3. **Configure Authentication**: Set up any required authentication
4. **Add Custom Headers**: Include any necessary headers
5. **Choose HTTP Method**: Select from GET, POST, PUT, or DELETE
6. **Enter Endpoint**: Specify the API endpoint to test
7. **Send Request**: The tool will execute the request and display formatted results

## Advanced Features

### Mock Responses

API Explorer allows you to create mock responses for endpoints:

```python
tester.mock_api_response(
    endpoint="/mock",
    response_data={"key": "value"},
    status_code=200,
    headers={"Content-Type": "application/json"}
)
```

### Scripting Integration

Create and execute test scripts directly within the tool:

1. Choose between Python or JavaScript
2. Write your test script interactively
3. Save and execute immediately

### Pagination Handling

For APIs that implement pagination, API Explorer can automatically handle:

- Page parameter detection
- Sequential request execution
- Consolidated response viewing

## Configuration Options

- **Timeout Settings**: Adjust request timeout duration
- **Retry Logic**: Configure number of retries and delay between attempts
- **Logging**: Detailed request/response logging to file
- **Caching**: Enable/disable response caching

## Examples

### Basic GET Request

```bash
$ python3 main.py
Enter the base URL of the API [https://jsonplaceholder.typicode.com]: 
Choose the HTTP method [GET]: 
Enter the endpoint [/posts]: 
```

### POST Request with JSON Body

```bash
$ python3 main.py
Enter the base URL of the API [https://jsonplaceholder.typicode.com]: 
Choose the HTTP method [POST]: 
Enter the endpoint [/posts]: 
Enter the request body as JSON [{}]: {"title": "foo", "body": "bar", "userId": 1}
```

## Best Practices

1. **Start with Mock Responses**: Test your logic with mock data before hitting real endpoints
2. **Use Scripting for Complex Flows**: Chain multiple requests together using the scripting feature
3. **Review Logs**: Check the log file for complete request/response details
4. **Cache Responsibly**: Clear cache when testing dynamic endpoints

## Troubleshooting

- **Connection Errors**: Verify your network connection and base URL
- **Authentication Failures**: Double-check credentials and auth type
- **JSON Parsing Errors**: Ensure your request body is valid JSON
- **Timeout Issues**: Increase timeout value for slow APIs

## License

API Explorer is released under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.

## Support

For issues or feature requests, please open an issue on the GitHub repository.
