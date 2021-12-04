Backend Members:
Name: Luke Bowsher, Sean Wiesner
NetID: Lcb98, Saw336

outFIT Hack Challenge Final Submission
Group no: 14

Backend using SQL Alchemy creates 3 tables called users, outfits, and clothes. 
Implements 17 routes across 3 tables, including dealing with images in the tops and bottoms routes. 

Uploaded to Heroku https://outfithackchallenge.herokuapp.com/api/bottoms/
Please note that uploading images to heroku only works with png and jpeg images only, once they have been converted to base 64.
We use https://www.base64-image.de/ as our image converter, then copy paste the text into our POST request body with the "image_name" key

If this is not December 2021 the heroku and AWS accounts may be deactivated since this is for a school project.

Tables:
This is what each object will look like from their given table. The return type for all the routes will be a json object with these key: value pairs, or possibly a list of them.
- Users
    - id: int 
    - username: text
    - outfits: list of outfit objects
- Outfits
    - id: int
    - user_id: int (foreign key to Users.id)
    - top_id: int (refers to top in Clothes.id)
    - bottom_id: int (refers to bottom in Clothes.id)
- Clothes
    - id: int
    - url: string of a link to download the image
    - top: Bool (True for top, False for bottom)

Routes:
Users:
Get /api/users/
    Returns a list of all user objects
Get /api/users/id/
    Returns the one user object with id=id
Post /api/users/
    Needs json input in request body: {“username”: “username string here”}
    Returns the new bottom object created
Delete /api/users/id/
    Deletes the user with id=id
    Returns the deleted user object

Outfits:
Get /api/outfits/
    Returns a list of all outfits objects
Get /api/outfits/id/
    Returns the one outfit object with id=id
Get /api/outfits/user/id/
    Returns the list of all outfits for a given user with user_id=id
Post /api/outfits/
    Needs json input in request body: 
    {“user_id”: user_id, 
    “top_id”: top_id, 
    “bottom_id”: bottom_id}
    Returns the new bottom object created
Delete /api/outfits/id/
    Deletes the outfit with id=id
    Returns the deleted outfit object

Tops:
Get /api/tops/
    Returns a list of all top objects
Get /api/tops/id/
    Returns the one top object with id=id
Post /api/tops/
    Needs json input in request body: {“image_data”: "base 64 image here"}
    Returns the new bottom object created
Delete /api/tops/id/
    Deletes the top with id=id
    Returns the deleted top object

Bottoms:
Get /api/bottoms/
    Returns a list of all bottoms objects
Get /api/bottoms/id/
    Returns the one bottom object with id=id
Post /api/bottoms/
    Needs json input in request body: {“image_data”: "base 64 image here"}
    Returns the new bottom object created
Delete /api/bottoms/id/
    Deletes the bottom with id=id
    Returns the deleted bottom object

