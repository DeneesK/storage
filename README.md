### To launch:
- `cp env.sample .env`
- `docker-compose up`
#### then:
`http://127.0.0.1:8080/api/openapi`

File storage that allows you to store various types of files - documents, photos, other data.

<details>
<summary> Endpoints List: </summary>

1.Activity status of related services

```
GET /ping
```
Get information about the access time to all related services, for example, to databases, caches, mounted disks, etc.

**Response**
```json
{
    "db": 1.27,
    "cache": 1.89,
    ...
    "service-N": 0.56
}
```

2. User registration.

```
POST /register
```
New User Registration. The request accepts a login and password to create a new account.


3. User authorization.

```
POST /auth
```
The request takes the username and password of the account as input and returns an authorization token. Further, all requests check for the presence of a token in the headers - `Authorization: Bearer <token>`


4. Information about uploaded files

```
GET /files/
```
Return information about previously downloaded files. Available only to an authorized user.

**Response**
```json
{
    "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
    "files": [
          {
            "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
            "name": "notes.txt",
            "created_ad": "2020-09-11T17:22:05Z",
            "path": "/homework/test-fodler/notes.txt",
            "size": 8512,
            "is_downloadable": true
          },
        ...
          {
            "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
            "name": "tree-picture.png",
            "created_ad": "2019-06-19T13:05:21Z",
            "path": "/homework/work-folder/environment/tree-picture.png",
            "size": 1945,
            "is_downloadable": true
          }
    ]
}
```


5. Upload file to storage

```
POST /files/upload
```
Method for uploading a file to storage. Available only to an authorized user.
For downloading, the full path to the file is filled in, into which the downloaded file will be loaded / overwritten. If the required directories do not exist, they should be created automatically.
Also, it is possible to specify only the path to the directory. In this case, the name of the created file will be created in accordance with the file name passed.

**Request**
```
{
    "path": <full-path-to-file>||<path-to-folder>,
}
```

**Response**
```json
{
    "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
    "name": "notes.txt",
    "created_ad": "2020-09-11T17:22:05Z",
    "path": "/homework/test-fodler/notes.txt",
    "size": 8512,
    "is_downloadable": true
}
```


6. Download uploaded file

```
GET /files/download
```
Downloading a previously uploaded file. Available only to an authorized user.

**Path parameters**
```
/?path=<path-to-file>||<file-meta-id>
```
The possibility of downloading is both by the passed path to the file, and by the identifier.

</details>

