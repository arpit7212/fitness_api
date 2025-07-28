# Fitness API with FastAPI with python

What it does - 
Here is a sample fitness studio API. It contains all the required scripting for handling a fitness studio database. Here is what you can do with this once you get the swagger UI started

 - Create subjects that can have slots. 
 - Create slots for each subject with start and end time
 - Create clients that can enroll for these subjects
 - Change timezone for a slot and it will change respectively for each slot of that subject
 - Inbuilt functionality to handle overbooking ( as slot can be booked at max by 5 students)




Steps to get started with the project

step 1 - Create a virtual Environment and activate (optional) 
    - python -m venv <env name>
    - .\bin\Scripts\Activate

step 2 - Install the required modules used in the project
    - pip install -r requirements.txt

step 3 -  run seed_data.py to create a sample database
    - python .\seed_data.py

step 4 - run the app 
    - uvicorn main:app --reload
    - open in any browser - http://127.0.0.1:8000/docs for swagger UI



Steps to run Tests module 

step 1 - go to project root directory
    - cd .\omnify_fitness_api\app
step 2 - Run pytest
    - pytest
