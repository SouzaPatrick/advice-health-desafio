# advice-health-desafio
Project created for Advice Health's selection process

###### PS: It was not requested in the challenge but I thought it would be interesting to sell the car only to those who have a driver's license

## Requirements to run the project
- The project was created in a linux environment, POP OS 22.04. The commands follow this system, and may vary if you use another OS
- Python 3.10
- Possibility to run make commands (Makefile)

## Start project
##### Just enter the command below in the terminal
```bash
make install
```
###### The command above: start the container, install the dependencies and generate the populated database

###### [Run project with venv](docs/start_project_venv.md)

## Rotes
PS: To make it easier, I exported the [Postman collection](https://drive.google.com/drive/folders/1R-cfzdaI3WSPLX3GcxRHXrELBrQPkv2w?usp=sharing), just use the Flask API
In the login route, I used the ```Basic Auth```, sent in the ```header```. The body is sent empty
#### Header
```json
{
  "Authorization": "Basic YWR2aWNlaGVhbHRoOmFkdmljZWhlYWx0aA==",
  "Content-Type": "application/json"
}
```
```
POST http://localhost:5000/api/login/
```
#### Response
```json
{
    "exp": "Thu, 09 Feb 2023 03:09:42 GMT",
    "message": "Validated successfully",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkdmljZWhlYWx0aCIsImV4cCI6MTY3NTkxMjE4Mn0.jMHP3hkefzprW5VP5mCr3ZlJ6y8Y3jdLgWYIzzOZLLs"
}
```

---

After login, you will have access to the token and just send it also in the Header in Authorization, but now as Bearer Token
```bash
POST http://localhost:5000/api/car
```
#### Header
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkdmljZWhlYWx0aCIsImV4cCI6MTY3NTkxMjE4Mn0.jMHP3hkefzprW5VP5mCr3ZlJ6y8Y3jdLgWYIzzOZLLs",
  "Content-Type": "application/json"
}
```
#### Body
```json
{
  "owner": {
    "name": "Augusto",
    "cpf": "68175541016"
  },
  "cars": [
    {
      "model": "hatch",
      "color": "blue"
    }
  ]
}
```
#### Response [status_code: 201]
```json
{
    "message": "success"
}
```

---

### TODO
- Principal
- [x] A car without an owner cannot be registered
- [x] Can register owner without car
- [x] Validate car color. Cars can only have 3 colors ('yellow', 'blue' or 'gray')
- [x] Validate car types. Cars can only be of 3 types ('hatch', 'sedan' or 'convertible')
- [x] Create authentication
- [x] Use docker
- [x] Add unit tests
- [x] Validate max of cars per inhabitant/owner, maximum of 3

Bonus
- [x] Run it all in just one command
- [x] Popular database (test user)
