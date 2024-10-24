# vct-hackathon
## Author: Louis Ton
## Submission: Individual

### Setup

#### Installations
Ensure that you install all the required packages through the `requirements.txt` via command line 
```
pip install -r requirements.txt
```
This can be done in a virtual environemnt if you do not want these packages installed globally.

Ensure you have node installed as well to be able to boot up a local react server

####
Create a `.env` file at the root of the repository. Create two variables, "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY", and "
set them to the guest user role with permission to use the model: id: "AKIA4AQ3TYI2TC7U4JK5", key: "1vL+AEeDJWgUfuiqMUKDr7eeaWQkfgBv33lV6cAz"
### Start Frontend
`cd` into `frontend/vct-chat` and enter `npm start` in the command line.
You can view the page through your local host on port 300 or "localhost://3000"

### Start Backend
Run the command `flask --app app run`

Interact with the model as you want!

