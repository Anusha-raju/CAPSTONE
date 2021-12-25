<h1> CAPSTONE PROJECT</h1>                                            

Author: *ANUSHA*



The app is deployed in Heroku ***[amazingforms](https://amazingforms.herokuapp.com/)***

The guiding video is   ***[YOUTUBE](https://youtu.be/t5i_N2-EMVc)***



***Additional feature added email token validation*** 

An email is sent with timed token when the user is signing in for the first time to validate the email_id.

Edit the existing form to create a new form.



<b>TASK GIVEN</b>

create a typeform clone:

The features that you need to implement are:

- Must be hosted on HEROKU (at least) or AWS (if you are comfortable or have time).

- The backend must be Flask

- Simple login (username: tsai, password: tsai99!) and logout

  - There is only 1 user (so no separate database for each user, there is only 1 database)

- Simple set up for the user (as [described ](https://www.youtube.com/watch?v=OcWbNM4hDsc) in this video)

- Templates are not required.

- Workspace to see forms already created, and a button to create a new form.

- Need to have Editor and Logic (Design is optional)

- You must implement 2 options is the layout (question on top of image, or image is on side of the question)

- Connect is not required.

- Share is required (gives a public url that can be used to fill in the form)

- Results is required.

- Focus is not on UI/Tabs, etc, but features. So it is OK to have buttons and NOT TABS.

- Kinds of Question Elements that are available:

  - Multiple Choice
  - Multiple Answers
  - Phone Number (with validation)
  - Short Text (min 10, max 144 characters)
  - Long Text (min 50, max 500 characters)
  - Picture Multiple Choice
  - Picture Multiple Answers
  - Statement (not a question, but a text that you want to share as a message)
  - Yes/No
  - Email (with validation)
  - Likert
    ![img](https://techcommunity.microsoft.com/t5/image/serverpage/image-id/36960i4A8911CF72BCE12D/image-size/medium?v=v2&px=400)
    - Should be able to add row names (for whatever we are asking to rate)
    - Should be able to add 2-10 columns along with the names (Satisfied/Neutral, etc)
  - Rating (out of 5)
  - Date (with validation)
  - Number (with validation)
    - 0.50, 1/2, SPACES0.5SPACES, etc are all equal
  - Fill in **A** Blank
    - answer, ANSWER, Answer, SPACEanswerSPACES, etc, are all equal
  - Fill in the **Blanks**:
    - answer, ANSWER, Answer, SPACEanswerSPACES, etc, are all equal
  - Dropdown
  - File Upload:
    - With [Plagiarism ](https://dev.to/kalebu/how-to-detect-plagiarism-in-text-using-python-dpk) detector! (only for markdown or txt file)
    - For file format Validation (support for PDF, markdown, txt)
  - Website Link (with validation)

- All the Question elements must have these options:

  - Required or Not
  - Score attached for correct answers (think what you'd do in case 3/5 are correct)

  - It is OK to implement a custom log schema (above we mentioned binary logic). 
  - You must implement Results, and each form/test result (final) must be available as future logs to be seen
    - If the form/test was taken 10 times, then 10 separate scores must be visible
    - Results must also show the [Plagiarism (Links to an external site.)](https://dev.to/kalebu/how-to-detect-plagiarism-in-text-using-python-dpk) score for the uploaded document (if any)
  - You must implement the "timed" feature (quiz to be closed after 10 minutes, etc)
  - Data/results/questions/etc everything is persistent (stored for eternity, and not deleted once application closes)
  - **Allow a user to download the made quiz (as txt/json/etc), and change something inside, and upload it back to make a new quiz automatically!**

