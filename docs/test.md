# Тестування працездатності системи

*В цьому розділі необхідно вказати засоби тестування, навести вихідні коди тестів та результати тестування.*

## POST
### *Create Role*
```bash
{
  "name": "Stas",
  "description": "Info1"
}
```
![image](https://github.com/user-attachments/assets/96a0499a-b76c-482c-873c-7b6050e61771)
### *Create User*
```bash
{
  "email": "stastokaruk@gmail.com",
  "password": "admin",
  "name": "admin",
  "surname": "Stanislav",
  "nickname": "Tokariuk"
}
```
![image](https://github.com/user-attachments/assets/a3ac4746-5b1e-4731-b5ec-c1e6a6f7a629)
### *Create Expertise Category*
```bash
{
  "name": "category1",
  "description": "Info1"
}
```
![image](https://github.com/user-attachments/assets/9bdb6f28-00b5-4b5f-8d80-211a5581ca57)

### *Create User Expertise*
```bash
{
  "User_id": 2,
  "ExpertiseCategory_id": 1
}
```
![image](https://github.com/user-attachments/assets/3e868a13-7fff-4c3f-bef2-9775426050b5)

### *Create Quiz*
```bash
{
  "name": "quiz1",
  "description": "opys",
  "User_id": 2
}
```
![image](https://github.com/user-attachments/assets/1cfd42c8-0018-4119-9a9a-0fbdb78598eb)

### *Create Question*
```bash
{
  "Quiz_id": 1,
  "number": 1,
  "description": "question1",
  "type": "easy"
}
```
![image](https://github.com/user-attachments/assets/96a0499a-b76c-482c-873c-7b6050e61771)
### *Create Option*
```bash
{
  "Question_id": 1,
  "number": 1,
  "description": "info"
}
```
![image](https://github.com/user-attachments/assets/a067a046-d057-43c6-80ee-98a45c6a5793)


## GET

## DELETE
