Types
=====

Simple types:
----------------
`text` - sends text
```json
{
  "type": "text",
  "message": "Привет!"
}
```

---

`image` - sends image
```json
{
  "type": "image",
  "url": "http://risovach.ru/thumb/upload/240c240/2017/02/generator/oo_136389863_orig_.jpg?ejv9p"
},
```

---

`video` - sends video
```json
{
  "type": "image",
  "url": "link_to_video"
},
```

---

`location` - sends location
```json
{
  "type": "location",
  "location":
    {
      "lat": 55.799921,
      "long": 37.786375
    }
},
```

Types wait\_for\_\*
----------------
Every wait\_for\_\* type can have `mistake` field with message of simple type which sends when user fails wait\_for\_\* condition.
```json
{
  "type": "wait_for_text",
  "text": "ответ",
  "mistake":
    {
        "type": "text",
        "message": "Нет, это не ответ!"
    }
}
```
---

`wait_for_location` - waits for user's location to be `distance` or less closer to location (in meters).

If `location` is not specified - waits for any location.

If `distance` is not specified - `distance` is 15.
```json
{
  "type": "wait_for_location",
  "location":
    {
      "lat": 55.799921,
      "long": 37.786375
    },
  "distance": 15
},
```
---

`wait_for_text` - waits for user's text to become `text`. If `strict` is true, check is case sensitive.

If `strict` is not specified - `strict` is false.
```json
{
  "type": "wait_for_text",
  "text": "Подушка",
  "strict": false
},
```
